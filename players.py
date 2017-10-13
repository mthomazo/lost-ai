# coding: utf-8

class Player():
	"""
	Mother class for all players, AI like humans
	"""

	def __init__(self, playerId):
		"""
		Arguments:
			playerId (int): the Id of the player
		"""
		self.playerId = playerId
		self.hand = []

	def setHand(self, hand):
		"""
		Set the hand of the player
		Arguments:
			hand (list of Card): hand of the player
		"""
		self.hand = hand

	def play(self, board):
		"""
		First step of a turn. Choose which card to play and where.
		Arguments:
			board (Board): the current board
		return:
			Card: the chosen card
			int: the Id of the player if the card has to be play on its board,
				 0 if the card has to be dicarded
		"""
		temp = self.hand[0]
		return (temp, 0)

	def removeFromHand(self, card):
		"""
		Remove one card from the player's hand
		Arguments:
			card (Card): card to be removed
		"""
		temp = self.hand
		self.hand = []
		for i in temp:
			if card != i:
				self.hand.append(i)
		if len(self.hand) == len(temp):
			raise ValueError("Card not in player hand")

	def addtoHand(self, card):
		"""
		Add a card to the player's hand
		Arguments:
			card (Card): card to be added
		"""
		i = 0
		while card > self.hand[i]:
			i +=1
			if i == len(self.hand):
				break
		if i == 0:
			self.hand = [card] + self.hand
		elif i == len(self.hand):
			self.hand = self.hand + [card] 
		else:
			self.hand = self.hand[:i] + [card] + self.hand[i:]

	def draw(self, board):
		"""
		Second step of a turn. Decide where the card will be drawed from.
		Arguments:
			board (Board): current board
		Return:
			String: either "deck" if the player wants to draw a card from the deck,
					either a color if the player wants to draw a card from a 
					dicard pile.
		"""
		return "deck"
