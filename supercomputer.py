import socket, threading, sys, os

class Slavery(threading.Thread):

    def __init__(self, _port):

        self.port = _port

        self.master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master.bind((socket.gethostname(), self.port))
        self.master.listen(200)

        self.nodes = []

        threading.Thread.__init__(self)


    def run(self):
        #self.readConnections()
        pass


    def readConnections(self):

        self.nodes = []
        
        f = open('nodes.txt', 'r')

        for line in f:
            #Slave node: host, port, rank, status
            self.nodes.append([line.strip(), self.port, len(self.nodes)+1, 'waiting'])


    def revolution(self):
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        for slave in self.nodes:
            try:
                conn.connect((slave[0], slave[1]))
                conn.send('#revolution')
                conn.send(str(slave[2]))
            except Exception, e:
                print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                print 'Error: ' + str(e)
        
        conn.close()


    def send(self, _rank, _data):
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for slave in self.nodes:
            print type(slave[2])
            print type(_rank)
            if slave[2] == int(_rank):
                try:
                    conn.connect((slave[0], slave[1]))
                    conn.send('#send')
                    conn.send(_data)
                except Exception, e:
                    print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                    print 'Error: ' + str(e)

        conn.close()


    def broadcast(self, _data):

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for slave in self.nodes:
            try:
                conn.connect((slave[0], slave[1]))
                conn.send('#broadcast')
                conn.send(_data)
            except Exception, e:
                print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                print 'Error: ' + str(e)

        conn.close()


    def gather(self):

        for slave in self.nodes:
            slave[3] = 'waiting'

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        
        waiting = True

        while waiting:

            for slave in self.nodes:

                msg = ''

                if slave[3] == 'waiting':

                    try:
                        conn.send('#status')
                        msg = self.master.recv(128)
                    except Exception, e:
                        print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                        print 'Error: ' + str(e)

                    if msg == 'ready':
                        slave[3] = msg
                        print 'Slave ' + str(slave[0]) + ' on port ' + str(slave[1]) + ' is ready'
                    else:
                        print 'Waiting on slave ' + str(slave[0]) + ' on port ' + str(slave[1])

            waiting = False

            for slave in self.slaves:
                if slave[3] == 'waiting':
                    waiting = True
                    break            
            
        conn.close()



if __name__ == '__main__':
    
    port = int(sys.argv[1])

    supercomputer = Slavery(port)
    supercomputer.start()

    while True:
        i = raw_input('\n[c] to read connections\n[r] to assign rank\n[s] to send\n[b] to broadcast\n[g] to gather\n[q] to quit\n')
        if i == 'c':
            supercomputer.readConnections()
        if i == 'r':
            supercomputer.revolution()
        if i == 's':
            rank = raw_input('\nenter rank\n')
            data = raw_input('\nenter data\n')            
            supercomputer.send(rank, data)
        if i == 'b':
            data = raw_input('\nenter data\n')            
            supercomputer.broadcast(data)
        if i == 'g':
            supercomputer.gather()
        if i == 'q':
            supercomputer.master.close()
            os._exit(1)
