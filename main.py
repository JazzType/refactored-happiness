import ServerSide
import ClientSide
import sys


class Begin:
	def __init__(self):
		quit = False
		while not quit:
			print "Are you a Server or Client?"
			ch = raw_input()
			if ch == "Server" or ch == "server":
				state = 1
				break
			elif ch == "Client" or ch == "client":
				state = 2
				break
			elif ch == "quit":
				exit()

		if state == 1:
			ServerSide.PokerServer()
		elif state == 2:
			ClientSide.PokerClient()


if __name__ == '__main__':
	if len(sys.argv) == 1:
		Begin()
	elif sys.argv[1] == '--server':
		ServerSide.PokerServer()
	elif sys.argv[1] == '--client':
		ClientSide.PokerClient()
