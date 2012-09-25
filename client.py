import threading, sys, os
from socket import *

__author__ =  'Ethan Genz, Jordan Haber, Eduardo Mello'
__version__=  '1.0'

'''
Client-side for our SuperComputer program.
'''

class Client(threading.Thread):

	status = "waiting"
	rank = 1
	
    def __init__(self, _host, _port):
        threading.Thread.__init__(self)
        
        try:
            self.client = socket(AF_INET, SOCK_STREAM)
            self.client.connect((_host, _port))
        except:
            print 'Broadcast server is unreachable'
            os._exit(1)
            



    def run(self):
	'''
	Execute the part of the problem this slave has been assigned
	'''
        


class listener(threading.Thread):

    def __init__(self, _client, _stream):
        threading.Thread.__init__(self)
        self.c = _client
        self.m = _stream

    	while True:
            data = self.client.recv(128)
            if data == "#broadcast" and self.client.status == "ready":
            	total_data=[]
				while True:
					data = self.client.recv(8192)
					if not data: break
					total_data.append(data)
					data = ''.join(total_data)
					self.client.run(data)
            elif data == "#revolution" and self.client.status== "ready":
            	self.rank = self.client.recv(128)
            elif data == "#status":
            	self.client.send(self.client.status)
           	else:
           		self.client.send("Client is busy or invalid command.")       



if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    c = Client(HOST, PORT)
#    s = Streamer(c)
	l = listener(c, s)
    c.start()
#    s.start()
	l.start()
