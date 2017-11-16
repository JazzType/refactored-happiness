import random


class Deck():
	def __init__(self):
		self.deck = []
		self.reset()
		self.shuffle()

	def reset(self):
		suit = ['H', 'S', 'D', 'C']
		for i in suit:
			for value in range(2, 15):
				self.deck.append((i, value))

	def shuffle(self):
		random.shuffle(self.deck)

	def pop(self):
		temp = self.deck[0]
		del self.deck[0]
		return temp

	def display(self):
		for i in self.deck:
			print i


if __name__ == '__main__':
	obj = Deck()
	obj.display()
