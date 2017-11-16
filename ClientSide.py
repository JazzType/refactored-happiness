import clientThread
import clientGame


class PokerClient:
		def __init__(self):
			serIP = raw_input("Enter IP (defaults to 0.0.0.0): ")  # Enter IP and port on CLI
			serPort = raw_input("Enter port (defaults to 1221): ")
			if serPort == "":
				serPort = "1221"
			if serIP == "":
				serIP = "0.0.0.0"

			print "Connecting to {}:{}..".format(serIP, serPort),

			cliObj = clientThread.ClientThread(str(serIP), int(serPort))
			print("Done.\nPlease wait for the game to start.")
			begin = cliObj.sock.recv(1024)
			if begin == "begin":
				clientGame.ClientGame(cliObj.sock)
