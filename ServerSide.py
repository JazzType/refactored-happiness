import serverThread
import serverGame
import sys


class PokerServer:
	def __init__(self):
		# Obtain a thread for the server room
		self.serverRoom = serverThread.ServerThread()
		self.setupFinished = False
		# Print room information to allow clients to connect
		print 'Room {0}:{1}'.format(self.serverRoom.get_ip(), self.serverRoom.get_port())

		while not self.setupFinished:
			print '\r{:2} clients connected | [q]uit, [u]pdate or [s]tart > '.format(self.serverRoom.get_num_of_clients())
			choice = raw_input().strip()
			if choice == 'q' or choice == 'Q':
				sys.exit()
			if choice == 's' or choice == 'S':
				self.setupFinished = True

		serverGame.main(self.serverRoom.clients)


if __name__ == "__main__":
	PokerServer()
