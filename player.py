from constants import *


class Player():
	def __init__(self, turn, name="John"):
		self.isActive = True
		self.turn = turn
		self.name = name
		self.reset()

	def reset(self):
		self.fold = False
		self.money = INITMONEY
		self.pot = 0
		self.currentRoundBet = 0

	def bet(self, amount):
		if amount > self.money:
			amount = self.money
		self.money -= amount
		self.pot += amount
		self.currentRoundBet += amount
		return amount

	def do_fold(self):
		self.fold = True

	def display(self):
		print self.turn, self.name, self.money, self.pot, self.fold


if __name__ == '__main__':
	obj = Player(0)
