import socket, threading, sys, os

class Slavery(threading.Thread):

    def __init__(self, _port):

        self.port = _port

        self.nodes = []

        threading.Thread.__init__(self)


    def run(self):
       pass
        #self.readConnections()


    def readConnections(self):

        self.nodes = []
        
        f = open('nodes.txt', 'r')

        for line in f:
            tmp = line.strip()
            tmp = tmp.split(' ')
            #Slave node: host, port, rank, status
            self.nodes.append([tmp[0], int(tmp[1]), len(self.nodes)+1, 'waiting'])


    def revolution(self):
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = ''

        for slave in self.nodes:
            try:
                conn.connect((slave[0], slave[1]))
                data += '#revolution$'
                data += str(slave[2])
                conn.send(data)
            except Exception, e:
                print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                print 'Error: ' + str(e)
        
        conn.close()


    def send(self, _rank, _data):
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = ''
        try:
	  with open(_data) as f:
	    _data = f.read()
	except IOError as e:
	  print 'Sendind comand'
        for slave in self.nodes:
            if slave[2] == int(_rank):
                try:
                    conn.connect((slave[0], slave[1]))
                    data += '#send$'
                    data += _data
                    data += '#end'
                    conn.send(data)
                except Exception, e:
                    print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                    print 'Error: ' + str(e)

        conn.close()


    def broadcast(self, _data):

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = ''

        for slave in self.nodes:
            try:
                conn.connect((slave[0], slave[1]))
                data += '#broadcast$'
                data += _data
                data += '#end'
                conn.send(data)
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
                        conn.connect((slave[0], slave[1]))
                        conn.send('#status')
                        msg = conn.recv(64)
                        conn.close()
                    except Exception, e:
                        print 'Unable to connect to ' + str(slave[0]) + ' on port ' + str(slave[1])
                        print 'Error: ' + str(e)

                    if msg == 'ready':
                        slave[3] = msg
                        print 'Slave ' + str(slave[0]) + ' on port ' + str(slave[1]) + ' is ready'
                    else:
                        print 'Waiting on slave ' + str(slave[0]) + ' on port ' + str(slave[1])

            waiting = False

            for slave in self.nodes:
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
            data = raw_input('\nenter data or file path\n')            
            supercomputer.send(rank, data)
        if i == 'b':
            data = raw_input('\nenter data\n')            
            supercomputer.broadcast(data)
        if i == 'g':
            supercomputer.gather()
        if i == 'q':
            os._exit(1)
