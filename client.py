import threading, socket, sys, os

__author__ =  'Ethan Genz, Jordan Haber, Eduardo Mello'
__version__=  '1.0'

'''
Client-side for our SuperComputer program.
'''
class Client(threading.Thread):

	def __init__(self, _host, _port):

		threading.Thread.__init__(self)
		self.port = _port
		self.status = "waiting"
		self.rank = 1
		self.connected = False

		self.slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.slave.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                       
		self.slave.bind(('localhost', self.port))
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


				f = open('run.py', 'w')
				f.write(data)
				f.close()
				
				self.status = 'waiting'
				#run new program
				print 'new data: ' + data

			elif msg.startswith("#revolution"):
				self.rank = int(msg[msg.find('$')+1:])
				print 'new rank: '+ str(self.rank)

			elif msg.startswith("#status"):
				self.conn.send(self.status)
			else:
				pass
				#self.conn.send("Client is busy or invalid command.")       
        

	def connect(self):
		while not self.connected:
			self.conn, conn_address = self.slave.accept()
			self.connected = True



class Executioner(threading.Thread):

	def __init__(self, _client):
		
		threading.Thread.__init__(self)
		self.c = _client

	



if __name__ == '__main__':

	host = sys.argv[1]
	port = sys.argv[2]

	c = Client(host, int(port))
	c.start()

	while True:
		i = raw_input('\n[r] to get rank\n[s] to get status\n[q] to quit\n')
		if i == 'r':
			print c.rank
		if i == 's':
			print c.status
		if i == 'q':
			c.slave.close()
			os._exit(1)
