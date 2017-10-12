from socket import *
from thread import *
import time


class ClientThread(object):
	def __init__(self, host, port):

			self.sock = socket()

			try:
					# Connecting to socket
					self.sock.connect((host, port))
			except Exception as msg:
					print "Could not connect to server.\nError msg : ", msg

	def client_thread(self):
			# Infinite loop to keep client running.
			while True:
					text = raw_input("Enter Text : ")
					self.sock.send(text)
			sock.close()

	def get_socket_handle():
		return self.socket


def main():
	host = raw_input("Enter the host IP: ")
	port = 1234

	obj = ClientThread(host, port)
	obj.client_thread()
	time.sleep(60)


if __name__ == '__main__':
	main()
