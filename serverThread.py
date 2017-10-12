from socket import *
from thread import *
import time
import main


class ServerThread(object):
	def __init__(self):
			self.num_of_clients = 0
			self.clients = []

			# Defining server address and port
			# 'localhost' or '127.0.0.1' or '' are all same
			self.host = '127.0.0.1'
			self.host = self.get_ip()
			# Use port > 1024, below it all are reserved
			self.port = 1234

			# Creating socket object
			sock = socket()

			# Binding socket to a address. bind() takes tuple of host and port.
			try:
				sock.bind((self.host, self.port))
			except Exception as msg:
					print "Could not start server.\n", msg
					print "Restarting the game."
					main.Begin()
					sys.exit()

		# Listening at the address, 5 denotes the number of clients can queue
			sock.listen(5)

			start_new_thread(self.server_thread, (sock, ))

	def server_thread(self, sock):

			while True:
					# Accepting incoming connections
					conn, addr = sock.accept()

					self.clients.append(conn)
					self.num_of_clients = self.num_of_clients + 1

			sock.close()

	def get_ip(self):
			s = socket(AF_INET, SOCK_DGRAM)
			s.connect(('8.8.8.8', 0))
			return s.getsockname()[0]

	def get_port(self):
			return self.port

	def get_num_of_clients(self):
			return self.num_of_clients

	def client_thread(self, conn, addr):
		# infinite loop so that function do not terminate and thread do not end.
			while True:

					# Receiving from client, 1024 stands for bytes of data to be received
					data = conn.recv(1024)
					if not data:
							self.num_of_clients -= 1
							break
					print str(addr) + ' : ' + data
			conn.close()


if __name__ == '__main__':
	obj = ServerThread()
	print obj.get_ip()
	time.sleep(60)
