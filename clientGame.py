#import sys, pygame, mygui, serverThread, time, player, json, main
import sys, serverThread, time, player, json, main
#from pygame.locals import *
from constants import *
from operator import sub
#from graphics import *
import os


def cls():
	os.system('cls' if os.name=='nt' else 'clear')

class ClientGame:
	def __init__(self, clientSocket):

		print "Inside ClientGame : init method"

		# self.test(screen)
		self.main(clientSocket)


	def recv(self, clientSocket):
		#cls()

		jsonData = clientSocket.recv(4196)
		if not jsonData:
			print "No data received from server.\nRestarting Game."
			main.Begin()
			sys.exit()

		data = jsonData.split("::")
		jsonCards = data[0]
		self.exTurn = self.turn  #Keeping last player's turn
		self.myTurn = int(data[1])
		jsonPlayers = data[2]
		jsonTblCards= data[3]
		jsonThings = data[4]
		self.winners = data[5]

		self.myCards = json.loads(jsonCards)
		self.tableCards = json.loads(jsonTblCards)
		self.winners = json.loads(self.winners)
		self.things = json.loads(jsonThings)
		self.turn = int(self.things[0])
		self.numberOfPlayers = int(self.things[1])
		self.exPot = self.pot    #Keeping the previous round's pot
		self.pot = int(self.things[2])
		self.toCallAmount = int(self.things[3])
		self.infoFlag = int(self.things[4])
		self.winCards = self.things[5]
		self.maxBet = self.things[6]
		self.resultRating = int(self.things[7])

		#print 'my cards :', self.myCards

		print 'My Cards'
		print '========================='
		for x in self.myCards:
			if x[0] == 'S':
				print 'Spade   : ', u'\u2660',  
			elif x[0] == 'H':
				print 'Heart   : ', u'\u2665',
			elif x[0] == 'D':
				print 'Diamond : ', u'\u2666',
			elif x[0] == 'C':
				print 'Club    : ', u'\u2663',
			if x[1] < 11:
				print x[1]
			elif x[1] == 11:
				print 'Jack'
			elif x[1] == 12:
				print 'Queen'
			elif x[1] == 13:
				print 'King'
			elif x[1] == 14:
				print 'A'
		print '-------------------------'

		print 'Table Cards'
		print '-------------------------'
		for x in self.tableCards:
			if x[0] == 'S':
				print 'Spade   : ', u'\u2660',  
			elif x[0] == 'H':
				print 'Heart   : ', u'\u2665',
			elif x[0] == 'D':
				print 'Diamond : ', u'\u2666',
			elif x[0] == 'C':
				print 'Club    : ', u'\u2663',
			if x[1] < 11:
				print x[1]
			elif x[1] == 11:
				print 'Jack'
			elif x[1] == 12:
				print 'Queen'
			elif x[1] == 13:
				print 'King'
			elif x[1] == 14:
				print 'A'
		print '========================='

		print 'turn : ', self.turn
		#cls()

		jsonPlayers = json.loads(jsonPlayers)
		self.players = {0:[]}
		for key in jsonPlayers:
			obj = player.Player(jsonPlayers[key]['turn'], jsonPlayers[key]['name'])
			obj.fold = jsonPlayers[key]['fold']
			obj.pot = jsonPlayers[key]['pot']
			obj.money = jsonPlayers[key]['money']
			obj.currentRoundBet = jsonPlayers[key]['currentRoundBet']
			obj.isActive = jsonPlayers[key]['isActive']

			self.players[key] = obj

		self.NAMES = []
		self.MONEY = []
		self.ROUNDBET = []
		for o in range(self.numberOfPlayers):
			self.NAMES.append(self.players[str(o)].name)
			self.MONEY.append("$"+str(self.players[str(o)].money))
			self.ROUNDBET.append("$"+str(self.players[str(o)].currentRoundBet))

	def main(self, clientSocket):

		self.turn = -1
		self.pot = 0
		#g = Graphics()

		while 1:

			self.recv(clientSocket)
			self.update_game()
			#g.order_players(self.myTurn, self.numberOfPlayers)
			#g.init_gui( self.myTurn, self.turn, self.numberOfPlayers, self.myCards, self.infoFlag, self.MONEY, self.NAMES, self.ROUNDBET)
			self.update_screen()

			move_input = raw_input("[C]all $" + str(self.toCallAmount) + " , [f]old, [a]ll-in, [r]aise, [q]uit")



					 



			if self.myTurn == self.turn:

				#g.create_buttons(self.toCallAmount) #Creating all 4 buttons
				#slider1 = mygui.Slider(screen,(450,450),(self.toCallAmount, self.maxBet))    #Creating the raise slider

				#pygame.display.update() #Displaying the buttons


				#Slider event handle
				#slider1.event_slider(event, pygame.mouse.get_pos())
				#slider1.slider_update(screen)
				print '@@@@@@@@@@@@@@@@@@'
				state = None
				if move_input == "q" or move_input == "Q":
					#pygame.quit()
					sys.exit()

				elif move_input == "c" or move_input == "C":
					state = self.toCallAmount

				elif move_input == "f" or move_input == "F":
					state = -1

				elif move_input == "a" or move_input == "A":
					state = self.maxBet

				elif move_input == "r" or move_input == "R":
					raiseValue = int(raw_input("enter a no between "+str(self.toCallAmount)+" and "+str(self.maxBet) + ": "))
					state = raiseValue  

				#Mouse Hover handling
				#g.mouse_hover(self.toCallAmount)
				print self.toCallAmount, '_____________'
				#Mouse click handling
				#isSend, state = g.mouse_click(screen, event, self.toCallAmount, self.maxBet, slider1.getValue())
				#print '************', slider1.getValue()
				#print state, '$$$$$$$$$$$$', isSend,'****#######'
				#Sending data if button clicked
				data = clientSocket.send(str(state))
				if not data:
					print "Server not receiving data.\nRestarting Game."
					main.Begin()
					sys.exit()


			else:
				pass
				#g.remove_buttons()
				#g.()
				#g.slider_remove(screen)

				#pygame.display.update()

			#g.end_hand(screen, self.infoFlag, self.winners, self.winCards, self.resultRating)   #Result and winner display
			#pygame.display.update()
	
	def update_screen(self):

		print "Turn ", self.turn, "ExTurn ", self.exTurn

		#g.draw_boy(screen, self.turn, self.myTurn, self.turn)    #Redrawing the current player's image
		#g.draw_boy_box(screen, self.turn, self.MONEY[self.turn], self.NAMES[self.turn])    #Redrawing current player's text box

		#g.draw_boy(screen, self.exTurn, self.myTurn, self.turn)   #Redrawing the last player's image
		#g.draw_boy_box(screen, self.exTurn, self.MONEY[self.exTurn], self.NAMES[self.exTurn])   #Redrawing the last player's text box

		for i in range(self.numberOfPlayers):
			pass
			#g.draw_boy_bet(screen, i, self.ROUNDBET[i])    #Draw every player's current round bet.

		#g.draw_table_cards(screen, self.infoFlag, self.tableCards)    #Draw the cards to be placed on table.

		#Display pot
		if self.pot>0 and self.pot-self.exPot>0:
			pass
			#g.pot_animation( self.pot)

	def update_game(self):
		self.MONEY = []
		self.ROUNDBET= []
		for o in range(self.numberOfPlayers):
			self.MONEY.append("$"+str(self.players[str(o)].money))
			self.ROUNDBET.append("$"+str(self.players[str(o)].currentRoundBet))


if __name__ == '__main__':
	#pygame.init()
	#pygame.display.set_caption(CAPTION)
	#screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
	ClientGame(None)
