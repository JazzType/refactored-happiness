from operator import itemgetter


class Result:
	def hand_comparator(self, cards1, cards2):
		for i in range(5):
			if cards1[i][1] > cards2[i][1]:
				return 1
			elif cards1[i][1] < cards2[i][1]:
				return 2
		return 0

	def hand_strength(self, cards):
		cards = sorted(cards, key=itemgetter(1), reverse=True)
		self.topFiveCards = []
		# 1 - High card
		# 2 - One pair
		# 3 - Two pairs
		# 4 - Three of a kind
		# 5 - Straight
		# 6 - Flush
		# 7 - Full house
		# 8 - Four of a kind
		# 9 - Straight Flush

		if self.straight_flush(cards):
			if self.topFiveCards[0][1] == 14:
				return 10, self.topFiveCards
			return 9, self.topFiveCards

		elif self.four_of_a_kind(cards):
			return 8, self.topFiveCards

		elif self.full_house(cards):
			return 7, self.topFiveCards

		elif self.flush(cards):
			return 6, self.topFiveCards

		elif self.straight(cards):
			return 5, self.topFiveCards

		elif self.three_of_a_kind(cards):
			return 4, self.topFiveCards

		elif self.two_pair(cards):
			return 3, self.topFiveCards

		elif self.one_pair(cards):
			return 2, self.topFiveCards

		elif self.high_card(cards):
			return 1, self.topFiveCards

		else:
			return 1, self.topFiveCards

	def straight_flush(self, cards):
		cardsCopy = sorted(cards)
		for i in range(3):
			if cardsCopy[i][1] == cardsCopy[i + 1][1] - 1 and \
				cardsCopy[i][1] == cardsCopy[i + 2][1] - 2 and \
				cardsCopy[i][1] == cardsCopy[i + 3][1] - 3 and \
				cardsCopy[i][1] == cardsCopy[i + 4][1] - 4:
				if cardsCopy[i][0] == cardsCopy[i + 1][0] and \
					cardsCopy[i][0] == cardsCopy[i + 2][0] and \
					cardsCopy[i][0] == cardsCopy[i + 3][0] and \
					cardsCopy[i][0] == cardsCopy[i + 4][0]:
					self.topFiveCards = cardsCopy[i:i + 5]
					self.topFiveCards.reverse()
					return True

		for i in range(7):
			if cardsCopy[i][1] == 14:
				cardsCopy[i] = (cardsCopy[i][0], 1)
		cardsCopy = sorted(cardsCopy)

		for i in range(3):
			if cardsCopy[i][1] == cardsCopy[i + 1][1] - 1 and \
				cardsCopy[i][1] == cardsCopy[i + 2][1] - 2 and \
				cardsCopy[i][1] == cardsCopy[i + 3][1] - 3 and \
				cardsCopy[i][1] == cardsCopy[i + 4][1] - 4:

				if cardsCopy[i][0] == cardsCopy[i + 1][0] and \
					cardsCopy[i][0] == cardsCopy[i + 2][0] and \
					cardsCopy[i][0] == cardsCopy[i + 3][0] and \
					cardsCopy[i][0] == cardsCopy[i + 4][0]:

					self.topFiveCards = cardsCopy[i:i + 5]
					self.topFiveCards.reverse()
					self.topFiveCards[4] = (self.topFiveCards[4][0], 14)
					return True

		return False

	def four_of_a_kind(self, cards):
		for i in range(4):
			if cards[i][1] == cards[i + 1][1] and \
				cards[i][1] == cards[i + 2][1] and \
				cards[i][1] == cards[i + 3][1]:

				self.topFiveCards = cards[i:i + 5]

				if cards[0][1] != cards[i][1]:
					self.topFiveCards.append(cards[0])

				else:
					self.topFiveCards.append(cards[4])

				return True

		return False

	def full_house(self, cards):
		for i in range(3):
			if cards[i][1] == cards[i + 1][1] and \
				cards[i][1] == cards[i + 2][1]:
				for j in range(i + 3, 6):
					if cards[j][1] == cards[j + 1][1]:
						self.topFiveCards = cards[i:i + 3] + cards[j:j + 2]
						return True
		for i in range(3):
			if cards[i][1] == cards[i + 1][1]:
				for j in range(i + 2, 5):
					if cards[j][1] == cards[j + 1][1] and cards[j][1] == cards[j + 2][1]:
						self.topFiveCards = cards[j:j + 3] + cards[i:i + 2]
						return True

		return False

	def flush(self, cards):
		cardsCopy = sorted(cards)
		for i in range(3):
			if cardsCopy[i][0] == cardsCopy[i + 1][0] and \
				cardsCopy[i][0] == cardsCopy[i + 2][0] and \
				cardsCopy[i][0] == cardsCopy[i + 3][0] and \
				cardsCopy[i][0] == cardsCopy[i + 4][0]:
				self.topFiveCards = cardsCopy[i:i + 5]
				return True
		return False

	def straight(self, cards):
		for i in range(3):
			if cards[i][1] == cards[i + 1][1] + 1 and \
				cards[i][1] == cards[i + 2][1] + 2 and \
				cards[i][1] == cards[i + 3][1] + 3 and \
				cards[i][1] == cards[i + 4][1] + 4:
				self.topFiveCards = cards[i:i + 5]
				return True

		if cards[0][1] == 14:
			card = cards[0]
			cardsCopy = cards
			cardsCopy[0] = ('H', 1)
			cardsCopy = sorted(cardsCopy, key=itemgetter(1), reverse=True)
			cards[0] = card
			for i in range(3):
				if cardsCopy[i][1] == cardsCopy[i + 1][1] + 1 and \
					cardsCopy[i][1] == cardsCopy[i + 2][1] + 2 and \
					cardsCopy[i][1] == cardsCopy[i + 3][1] + 3 and \
					cardsCopy[i][1] == cardsCopy[i + 4][1] + 4:
					self.topFiveCards = cardsCopy[i:i + 5]
					return True

		return False

	def three_of_a_kind(self, cards):
		for i in range(5):
			if cards[i][1] == cards[i + 1][1] and cards[i][1] == cards[i + 2][1]:
				self.topFiveCards = cards[i:i + 3]
				if cards[0][1] == cards[i][0]:
					self.topFiveCards += cards[3:5]
				else:
					self.topFiveCards.append(cards[0])
					if cards[1][1] == cards[i][1]:
						self.topFiveCards.append(cards[4])
					else:
						self.topFiveCards.append(cards[1])
				return True
		return False

	def two_pair(self, cards):
		for i in range(4):
			if cards[i][1] == cards[i + 1][1]:
				for j in range(i + 1, 6):
					if cards[j][1] == cards[j + 1][1]:
						self.topFiveCards = cards[i:i + 2] + cards[j:j + 2]
						if cards[0][1] == cards[i][1]:
							if cards[2][1] == cards[j][1]:
								self.topFiveCards.append(cards[4])
							else:
								self.topFiveCards.append(cards[2])
						else:
							self.topFiveCards.append(cards[0])
						return True
		return False

	def one_pair(self, cards):
		self.topFiveCards = []
		for i in range(6):
			if cards[i][1] == cards[i + 1][1]:
				self.topFiveCards.append(cards[i])
				self.topFiveCards.append(cards[i + 1])
				del cards[i + 1]
				del cards[i]
				self.topFiveCards += cards[:3]
				return True
		return False

	def high_card(self, cards):
		self.topFiveCards = cards[:5]
		return True


def main():
	cards = [('D', 5), ('H', 14), ('D', 14), ('D', 4), ('D', 3), ('D', 2), ('C', 14)]  # 9straight_flush
	obj = Result(cards)
	obj.hand_strength(cards)

if __name__ == '__main__':
	main()
