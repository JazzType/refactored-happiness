import clientThread
import clientGame
import sys
import socket


class PokerClient:
		def __init__(self):
			serIP = raw_input("Enter IP (defaults to 0.0.0.0): ")  # Enter IP and port on CLI
			serPort = raw_input("Enter port (defaults to 1221): ")
			if serPort == "":
				serPort = "1221"
			if serIP == "":
				serIP = "0.0.0.0"

			print "Connecting to {}:{}..".format(serIP, serPort),

			try:
				cliObj = clientThread.ClientThread(str(serIP), int(serPort))
			except Exception:
				print("Failed.\nUnable to establish connection to server, please try again.")
				sys.exit()

			try:
				begin = cliObj.sock.recv(1024)
			except socket.error:
				print 'Failed. Is the server running?'
				sys.exit()
			print("Done.\nPlease wait for the game to start.")
			if begin == "begin":
				clientGame.ClientGame(cliObj.sock)
