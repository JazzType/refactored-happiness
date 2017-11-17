import sys
import player
import json
import os


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


def print_cards(cards):
	print '========================='
	if len(cards) == 0:
		print None
		return
	for x in cards:
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


class ClientGame:
	def __init__(self, clientSocket):
		self.main(clientSocket)

	def recv(self, clientSocket):
		jsonData = clientSocket.recv(4196)
		if not jsonData:
			print "No data received from server.\nTerminating Game."
			sys.exit()

		data = jsonData.split("::")
		if data[0] == '':
			return True

		jsonCards = data[0]
		self.exTurn = self.turn  # Keeping last player's turn
		self.myTurn = int(data[1])
		jsonPlayers = data[2]
		jsonTblCards = data[3]
		jsonThings = data[4]
		self.winners = data[5]

		self.myCards = json.loads(jsonCards)
		self.tableCards = json.loads(jsonTblCards)
		self.winners = json.loads(self.winners)
		self.things = json.loads(jsonThings)
		self.turn = int(self.things[0])
		self.numberOfPlayers = int(self.things[1])
		self.exPot = self.pot  # Keeping the previous round's pot
		self.pot = int(self.things[2])
		self.toCallAmount = int(self.things[3])
		self.infoFlag = int(self.things[4])
		self.winCards = self.things[5]
		self.maxBet = self.things[6]
		self.resultRating = int(self.things[7])
		cls()
		print 'Your Cards', ' ' * 11
		print_cards(self.myCards)
		print 'Table Cards'
		print_cards(self.tableCards)

		jsonPlayers = json.loads(jsonPlayers)
		self.players = {0: []}
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
			self.MONEY.append("$" + str(self.players[str(o)].money))
			self.ROUNDBET.append("$" + str(self.players[str(o)].currentRoundBet))

	def main(self, clientSocket):
		self.turn = -1
		self.pot = 0

		while True:
			wonHand = self.recv(clientSocket)
			if wonHand is True:
				print 'You won this hand!    '
			self.update_game()
			print 'Please wait your turn.\r',
			if self.myTurn == self.turn:
				move_input = raw_input("[c]all $" + str(self.toCallAmount) + " , [f]old, [a]ll-in, [r]aise, [q]uit > ")
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
					raiseValue = int(raw_input("Enter amount between " + str(abs(self.toCallAmount)) + " and " + str(abs(self.maxBet)) + ": "))
					state = raiseValue

				data = clientSocket.send(str(state))

				if not data:
					print "Connection to server failed. Terminating."
					sys.exit()

	def update_game(self):
		self.MONEY = []
		self.ROUNDBET = []
		for o in range(self.numberOfPlayers):
			self.MONEY.append("$" + str(self.players[str(o)].money))
			self.ROUNDBET.append("$" + str(self.players[str(o)].currentRoundBet))


if __name__ == '__main__':
	ClientGame(None)
