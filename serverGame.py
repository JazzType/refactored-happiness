import sys
import time
import json
from constants import *
from deck import *
from player import *
from result import *
from operator import itemgetter


class ServerGame:
	def __init__(self, clientSockets):
		self.clientSockets = clientSockets

	# one match = several games, one game = 4 rounds
	def update_game(self, receivedBetValue):
		if receivedBetValue < 0:
			self.numberOfUnfoldedPlayers -= 1
			self.players[self.turn].do_fold()

		else:

			amount = self.players[self.turn].bet(receivedBetValue)
			self.roundPot += amount
			if self.players[self.turn].currentRoundBet > self.currentRoundBet:
				self.currentRoundBet = self.players[self.turn].currentRoundBet
				self.lastRaisedPlayer = self.turn

	def init_round(self):

		for i in range(self.numberOfPlayers):
			self.players[i].currentRoundBet = 0

		if self.infoFlag == 0:
			self.currentRoundBet = self.bigBlind

			temp1 = (self.start + 1) % self.numberOfPlayers
			while self.players[temp1].isActive is False:
				temp1 = (temp1 + 1) % self.numberOfPlayers

			self.players[self.start].bet(self.smallBlind)
			self.players[temp1].bet(self.bigBlind)

			temp2 = (temp1 + 1) % self.numberOfPlayers
			while self.players[temp2].isActive is False:
				temp2 = (temp2 + 1) % self.numberOfPlayers
			self.turn = temp2

			self.roundPot = self.players[self.start].currentRoundBet + \
				self.players[temp1].currentRoundBet
		else:
			self.currentRoundBet = 0
			self.roundPot = 0
			self.turn = self.start

		self.lastRaisedPlayer = self.turn

		self.toCallAmount = self.currentRoundBet - \
			self.players[self.serverTurn].currentRoundBet

		# update the gui?

	def start_round(self):
		self.init_round()

		if self.numberOfUnfoldedPlayers <= 1:
			return

		while True:
			self.toCallAmount = self.currentRoundBet - \
				self.players[self.serverTurn].currentRoundBet
			# self.maxBet = min(self.maxPlayerMoney,self.players[self.serverTurn].money)

			self.before_move()

			if (not self.players[self.turn].fold) and self.players[self.turn].money != 0 and self.players[self.turn].isActive:
				self.broadcast()
				if self.turn == self.serverTurn:
					recievedBetValue = self.server_move()  # server_move()
				else:
					self.client_move()
					recievedBetValue = 0
					try:
						recievedBetValue = int(self.clientSockets[self.turn].recv(
						1024))     # wait for client to move
					except ValueError:
						recievedBetValue = -1
					except IndexError:
						print 'Insufficient number of players, terminating game'
						sys.exit()

				self.update_game(recievedBetValue)

			self.exTurn = self.turn
			self.exPot = self.pot
			self.turn = (self.turn + 1) % self.numberOfPlayers

			self.after_move()

			if self.turn == self.lastRaisedPlayer or self.numberOfUnfoldedPlayers <= 1:
				break
		self.fin_round()
		# self.broadcast()

	def fin_round(self):
		self.pot += self.roundPot
		self.roundPot = 0
		self.numberOfUnfoldedPlayers = 0
		for i in range(self.numberOfPlayers):
			self.players[i].currentRoundBet = 0
			if not self.players[i].fold and self.players[i].money != 0:
				self.numberOfUnfoldedPlayers += 1

	def init_hand(self):
		self.deck = Deck()
		self.tableCards = []
		self.smallBlind = 10
		self.bigBlind = self.smallBlind * 2
		self.handWinners = []
		self.numberOfUnfoldedPlayers = self.numberOfActivePlayers
		self.pot = 0
		self.winCards = (self.deck.pop(), self.deck.pop())
		# Initializing cards
		self.cards = {0: []}

		# Temp changes
		#
		# tempc = (self.deck.pop(),self.deck.pop())
		# for cSock in self.clientSockets:
		#     self.cards[cSock] = tempc
		#     self.cards[i] = self.cards[cSock]
		#     i += 1
		# self.cards[self.serverTurn] = tempc#(self.deck.pop(),self.deck.pop()) #Server Cards
		#
		# self.myCards = self.cards[self.serverTurn]
		#
		# 3

		i = 0
		for cSock in self.clientSockets:
			self.cards[cSock] = (self.deck.pop(), self.deck.pop())
			self.cards[i] = self.cards[cSock]
			i += 1
		self.cards[self.serverTurn] = (
			self.deck.pop(), self.deck.pop())  # Server Cards

		self.myCards = self.cards[self.serverTurn]

		for i in range(self.numberOfPlayers):
			self.players[i].pot = 0
			self.players[i].fold = False

		# self.initGuiFlag = False

	def start_hand(self):
		self.init_hand()

		self.infoFlag = 0          # round 0
		self.start_round()

		self.tableCards.append(self.deck.pop())
		self.tableCards.append(self.deck.pop())
		self.tableCards.append(self.deck.pop())
		self.infoFlag = 1         # round 1
		self.start_round()

		self.tableCards.append(self.deck.pop())
		self.infoFlag = 2         # round 2
		self.start_round()

		self.tableCards.append(self.deck.pop())
		self.infoFlag = 3         # round 3
		self.start_round()

		self.infoFlag = 10        # Result 10
		# print "Hand completed"
		self.fin_hand()

	def fin_hand(self):

		# Hand result
		self.hand_result()

		# Decrese numberOfActivePlayers and remove from activePlayers
		for i in self.activePlayers:
			if self.players[i].money == 0:
				self.players[i].isActive = False
				self.numberOfActivePlayers -= 1
				self.activePlayers.remove(i)
		# increment start
		self.start = (self.start + 1) % self.numberOfPlayers
		while self.players[self.start].isActive is False:
			self.start = (self.start + 1) % self.numberOfPlayers

		self.turn = -1  # Added by safal
		self.broadcast()          # Final broadcast, broadcast result
		self.after_move()

	def init_game(self):
		self.resultRating = 0

		self.init_gui()

		self.numberOfPlayers = len(self.clientSockets) + 1
		self.numberOfActivePlayers = self.numberOfPlayers
		self.gameWinner = -1
		self.serverTurn = self.numberOfPlayers - 1
		self.start = 0
		self.myTurn = self.serverTurn
		self.exTurn = -1

		# Initializing cards and player
		self.players = {0: []}
		for i in range(self.numberOfPlayers):
			self.players[i] = Player(i, "client " + str(i))
		self.players[self.serverTurn].name = "Server"

		# List of ids of active players
		self.activePlayers = range(self.numberOfActivePlayers)

	def start_game(self):
		self.init_game()

		# multiple hands : game > hand > round
		while self.numberOfActivePlayers > 1:
			self.start_hand()

		self.fin_game()

	def fin_game(self):
		pass

	def broadcast(self):   # infoFlag, client's cards, myTurn, players, tablecards, turn, numberOfPlayers, pot, toCallAmount
		i = 0
		for cSock in self.clientSockets:
			maxPlayerMoney = 0
			for j in self.activePlayers:
				if not self.players[j].fold and j != i:
					maxPlayerMoney = max(
						maxPlayerMoney, self.players[j].money + self.players[j].currentRoundBet)

			maxBet = min(
				maxPlayerMoney -
				self.players[i].currentRoundBet,
				self.players[i].money)

			msgPlayerCards = json.dumps(self.cards[cSock])
			msgPlayers = json.dumps(self.players, default=lambda o: o.__dict__)
			msgTableCards = json.dumps(self.tableCards)

			toCallAmount = self.currentRoundBet - \
				self.players[i].currentRoundBet
			things = (
				self.turn,
				self.numberOfPlayers,
				self.pot,
				toCallAmount,
				self.infoFlag,
				self.winCards,
				maxBet,
				self.resultRating)
			msgThings = json.dumps(things)
			msgWinners = json.dumps(self.handWinners)
			completeMessage = msgPlayerCards + "::" + \
				str(i) + "::" + msgPlayers + "::" + msgTableCards + \
				"::" + msgThings + "::" + msgWinners
			i += 1
			# print completeMessage
			try:
				cSock.send(completeMessage)
			except Exception:
				print 'Player {} quit'.format(self.clientSockets.index(cSock) + 1)
				self.clientSockets.__delitem__(self.clientSockets.index(cSock))

			# print "Size of message sent : "+ str(sys.getsizeof(completeMessage)) +" bytes!"

	def hand_result(self):
		obj = Result()
		handStrengths = []
		extraMoney = {0: []}
		moneyToGive = []
		for i in range(self.numberOfPlayers):
			moneyToGive.append(0.0)
		for i in self.activePlayers:
			extraMoney[i] = float(self.players[i].pot)
			if not self.players[i].fold:
				playerCards = self.tableCards[:]
				playerCards.append(self.cards[i][0])
				playerCards.append(self.cards[i][1])
				a, b = obj.hand_strength(playerCards)
				handStrengths.append((i, a, b, self.players[i].pot))

		handPot = sorted(handStrengths, key=itemgetter(3), reverse=True)
		handStrengths = sorted(handStrengths, key=itemgetter(1), reverse=True)

		length = len(handStrengths)
		for i in range(length - 1):
			if handStrengths[i][1] == handStrengths[i + 1][1]:
				comp = obj.hand_comparator(
					handStrengths[i][2], handStrengths[i + 1][2])
				if comp == 2:
					handStrengths[i], handStrengths[i + 1] = handStrengths[i + 1], handStrengths[i]  # Swap

		# Removes all from handPot who won't get any money
		for i in range(length):
			temp = handStrengths[i]
			for j in range(length):
				if handStrengths[j][3] >= handStrengths[i][3]:
					if handStrengths[j][1] > handStrengths[i][1] or (handStrengths[j][1] == handStrengths[i][1] and obj.hand_comparator(handStrengths[j][2], handStrengths[i][2]) == 1):
						# moneyToGive.append(0.0)
						# extraMoney.append(temp[3])
						handPot.remove(temp)
						break

		handPot = sorted(handPot, key=itemgetter(3), reverse=True)
		length = len(handPot)

		# print handPot
		# print length
		# print extraMoney

		self.handWinners = []
		for i in range(length):
			self.handWinners.append(handPot[i][0])

		extraMoneyLength = len(extraMoney)

		while self.pot != 0 and len(handPot) > 0:
			# print "in loop 1"
			length = len(handPot)
			if length == 1:
				# Last player may get some extra money
				self.players[handPot[0][0]].money += self.pot
				break

			countEqual = 1
			for i in range(1, length):
				if handPot[i][1] == handPot[0][1] and obj.hand_comparator(handPot[i][2], handPot[0][2]) == 0:
					countEqual += 1
				else:
					break
			# print countEqual
			while True:
				largestPot = handPot[0][3]
				lessPot = 0
				count = 1
				for i in range(1, length):
					if handPot[i][3] < largestPot:
						lessPot = handPot[i][3]
						break
					count += 1
				exMon = 0
				for i in range(extraMoneyLength):
					exMon += extraMoney[i] - min(lessPot, extraMoney[i])
					extraMoney[i] = min(lessPot, extraMoney[i])
				tempd = int(count)

				for i in range(0, tempd):
					tmp = handPot[i][0]
					moneyToGive[tmp] = moneyToGive[tmp] + exMon / count
					hp = (handPot[i][0], handPot[i][1], handPot[i][2], lessPot)
					handPot[i] = hp
				self.pot -= exMon

				if count == countEqual:
					for i in range(tempd):
						del handPot[0]
					break

		for i in range(self.numberOfPlayers):
			self.players[i].money += moneyToGive[i]
			self.players[i].money = int(self.players[i].money)

		self.pot = 0

		self.winCards = self.cards[self.handWinners[0]]
		self.resultRating = handStrengths[0][1]

	############################
	# Code for GUI starts here #
	############################

	def init_gui(self):
		# self.g = Graphics()
		self.HANDBEGIN = False
		self.CARDDRAWN = [False, False, False]

	def before_move(self):
		self.update_MONEY()

		if not self.HANDBEGIN:
			self.draw_init_cards(self.myCards, self.infoFlag)

			for i in range(3):
				self.CARDDRAWN[i] = False

			self.HANDBEGIN = True

		self.update_screen()

	def draw_init_cards(self, myCards, infoFlag):
		if infoFlag == 0:
			print "\nNew Hand"
			print "my cards:"
			print myCards[0]
			print myCards[1]

	def server_move(self):
		maxPlayerMoney = 0
		for j in self.activePlayers:
			if not self.players[j].fold and j != self.serverTurn:
				maxPlayerMoney = max(
					maxPlayerMoney, self.players[j].money + self.players[j].currentRoundBet)
		self.maxBet = min(
			maxPlayerMoney - self.players[self.serverTurn].currentRoundBet, self.players[self.serverTurn].money)
		move_input = None
		if self.toCallAmount != 0:
			move_input = raw_input(
				"[c]all $" + str(self.toCallAmount) + " , [f]old, [a]ll-in, [r]aise or [q]uit > ")

		state = None
		if move_input == "q" or move_input == "Q":
			sys.exit()

		elif move_input == "c" or move_input == "C":
			state = self.toCallAmount

		elif move_input == "f" or move_input == "F":
			state = -1

		elif move_input == "a" or move_input == "A":
			state = self.maxBet

		elif move_input == "r" or move_input == "R":
			raiseValue = int(raw_input(
				"enter a no between " + str(self.toCallAmount) + " and " + str(self.maxBet) + ": "))
			state = raiseValue
		return state

	def client_move(self):
		pass

	def after_move(self):
		if self.infoFlag == 10:
			self.before_move()

		if self.infoFlag != 10:
			return

		print "Hand completed!"
		print "Winners are : " + str(self.handWinners)

		if self.handWinners[0] == len(self.clientSockets):
			print 'You won this hand!'
		else:
			self.clientSockets[self.handWinners[0]].send('::')
		self.HANDBEGIN = False

		time.sleep(4)
		# should we show other detals like cards won etc ??

		# g.end_hand(screen, self.infoFlag, self.handWinners, self.winCards, self.resultRating)   #Result and winner display

		# pygame.display.update()

	def update_screen(self):

		# print "Turn ", self.turn, "ExTurn ", self.exTurn
		print "new turn"
		'''g.draw_boy(screen, self.turn, self.myTurn, self.turn)    #Redrawing the current player's image
		g.draw_boy_box(screen, self.turn, self.MONEY[self.turn], self.NAMES[self.turn])    # Redrawing current player's text box

		g.draw_boy(screen, self.exTurn, self.myTurn, self.turn)   #Redrawing the last player's image'''

		# g.draw_boy_box(screen, self.exTurn, self.MONEY[self.exTurn], self.NAMES[self.exTurn])   #Redrawing the last player's text box
		# print "current round bet:"
		for i in range(self.numberOfPlayers):
			if self.ROUNDBET[i] != "$0":
				print self.NAMES[i] + " : " + str(self.ROUNDBET[i])
			# g.draw_boy_bet(screen, i, self.ROUNDBET[i])    #Draw every player's current round bet.

		# g.draw_table_cards(screen, self.infoFlag, self.tableCards)    #Draw the cards to be placed on table.
		if self.infoFlag == 1:
			if not self.CARDDRAWN[0]:
				print self.tableCards[0]
				print self.tableCards[1]
				print self.tableCards[2]
				self.CARDDRAWN[0] = True

		elif self.infoFlag == 2:
			if not self.CARDDRAWN[1]:
				print self.tableCards[3]
				self.CARDDRAWN[1] = True
		elif self.infoFlag == 3:
			if not self.CARDDRAWN[2]:
				print self.tableCards[4]
				self.CARDDRAWN[2] = True
		elif self.infoFlag == 10:
			for i in range(5):
				print self.tableCards[i]
			for i in range(3):
				self.CARDDRAWN[i] = True

		# Display pot
		print "pot : " + str(self.pot)
		# HAVE TO IMPLEMENT STILL
		'''if self.pot>0 and self.pot-self.exPot>0:
			g.pot_animation(screen, self.pot)'''

	def update_MONEY(self):
		self.NAMES = []
		self.MONEY = []
		self.ROUNDBET = []
		for i in range(self.numberOfPlayers):
			self.NAMES.append(self.players[i].name)
			self.MONEY.append("$" + str(self.players[i].money))
			self.ROUNDBET.append("$" + str(self.players[i].currentRoundBet))

	##########################
	# Code for GUI ends here #
	##########################


def unpause_clients(clientSockets):
	for obj in clientSockets:
		obj.send("begin")


def main(clientSockets):
	# clients = [1,2,3]

	unpause_clients(clientSockets)
	# print "Inside serverGame file : Method main()"

	game = ServerGame(clientSockets)
	game.start_game()

	time.sleep(5)
	sys.exit()

	# init(clientSockets)
	# start_game()


if __name__ == '__main__':
	main()
