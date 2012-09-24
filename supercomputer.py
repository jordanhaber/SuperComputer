import socket, threading, sys, os

class Slavery(threading.Thread):

    def __init__(self, _port):

        self.port = _port

        self.master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master.bind((socket.gethostname(), self.port))
        self.master.listen(200)

        self.nodes = []
        self.slaves = []

        threading.Thread.__init__(self)


    def run(self):
        #self.readConnections()
        pass


    def readConnections(self):

        f = open('nodes.txt', 'r')

        for line in f:
            self.nodes.append((line.strip(), self.port, len(self.nodes)+1))


    def revolution(self):
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        for slave in self.nodes:
            try:
                conn.connect((slave[0], slave[1]))
                conn.send('revolution:')
                conn.send(str(slave[2]))
            except Exception, e:
                print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                print 'Error: ' + str(e)
        
        conn.close()


    def broadcast(self, _data):

        self.slaves = []

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for slave in self.nodes:
            try:
                conn.connect((slave[0], slave[1]))
                conn.send('broadcast msg:')
                conn.send(_data)
                self.slaves.append((slave[0], slave[1], slave[2], 'waiting'))
            except Exception, e:
                print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                print 'Error: ' + str(e)

        conn.close()


    def gather(self):
        pass


if __name__ == '__main__':
    
    port = int(sys.argv[1])

    supercomputer = Slavery(port)
    supercomputer.start()

    while True:
        i = raw_input('\n[c] to read connections\n[r] to assign rank\n[b] to broadcast\n[q] to quit\n')
        if i == 'c':
            supercomputer.readConnections()
        if i == 'r':
            supercomputer.revolution()
        if i == 'b':
            data = raw_input('\nenter data to broadcast\n')            
            supercomputer.broadcast(data)
        if i == 'q':
            os._exit(1)
