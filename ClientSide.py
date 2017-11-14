#import sys, pygame, mygui, clientThread, time, clientGame
import sys, clientThread, time, clientGame
#from pygame.locals import *
from constants import *

class PokerClient:

    def __init__(self):

        
   	print ("Client")
    	serIP=raw_input("Enter IP: ")          #Enter IP and port on CLI
	serPort=raw_input("Enter port: ")
        print("Connecting")
        if serIP == "1":
           serIP = "10.42.0.45"
        elif serIP == "2":
           serIP = "172.24.136.242"

        if serPort =="":
           serPort = "1234"
        cliObj = clientThread.ClientThread(str(serIP),int(serPort))
	begin = cliObj.sock.recv(1024)
        if begin == "begin":
           print "Unpaused"
           clientGame.ClientGame(cliObj.sock)
