
from numpy  import *
import threading, socket, sys, os, math, time

__author__ =  'Ethan Genz, Jordan Haber, Eduardo Mello'
__version__=  '1.0'

'''
Client-side for our SuperComputer program.
'''
class Client(threading.Thread):

	def __init__(self, _host, _port):

		threading.Thread.__init__(self)

		self.port = _port
		self.host = _host

		self.rank = -1
		self.rank_max = 1

		self.connected = False

		self.slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.slave.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                       
		self.slave.bind((self.host, self.port))
		self.slave.listen(1)
		
			
	'''
	Listen to master commands
	'''
	def run(self):

		self.connect()

		while True:
			
			msg = self.conn.recv(128)

			if not msg:
				self.connected = False
				self.connect()

			if msg.startswith("#broadcast") or msg.startswith('#send'):

				data = msg[msg.find('$')+1:]

				while True:
					msg = self.conn.recv(1024)
					data += msg.strip()
					if '#end' in data:
						break

				data = data[:data.find('#end')]		

				self.e = Executioner(self.rank, self.rank_max, data)
				self.e.start()

				#run new program
				#print 'new data: ' + data

			elif msg.startswith("#revolution"):
				self.rank = int(msg[msg.find('$')+1:msg.rfind('$')])
				print 'new rank: '+ str(self.rank)
				self.rank_max = int(msg[msg.rfind('$')+1:])

			elif msg.startswith("#status"):
				self.conn.send(self.e.status)
				if self.e.status == 'ready':
					self.conn.send(str(self.e.solution))
			else:
				pass
				#self.conn.send("Client is busy or invalid command.")       
        

	def connect(self):
		while not self.connected:
			self.conn, conn_address = self.slave.accept()
			self.connected = True



class Executioner(threading.Thread):

	def __init__(self, _rank, _rank_max, _data):
		
		threading.Thread.__init__(self)
		self.rank = _rank
		self.rank_max = _rank_max
		self.data = _data
		self.status = 'waiting'
		self.solution = []
	
	def run(self):		
		
		try:
			exec self.data
		except Exception, e:
			print 'unable to run program'
			print 'Error: ' + str(e)
		self.status = 'ready'

	



if __name__ == '__main__':

	host = ''
	port = 0

	if len(sys.argv) == 2:
		try:
			port = sys.argv[1]
		except:
			print "Usage 'python client.py <host> <port>'"
			os._exit(1)
	else:
		try:
			host = sys.argv[1]
			port = sys.argv[2]
		except:
			print "Usage 'python client.py <host> <port>'"
			os._exit(1)

	c = Client(host, int(port))
	c.start()
	while True:
		i = raw_input('\n[r] to get rank\n[s] to get status\n[q] to quit\n')
		if i == 'r':
			print str(c.rank) + '/'  + str(c.rank_max)
		elif i == 's':
			print c.e.status
		elif i == 'q':
			c.slave.close()
			os._exit(1)


	


