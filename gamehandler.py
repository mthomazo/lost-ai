# coding: utf-8

import numpy as np

colors = ["yellow", "blue", "white", "green", "red"]
color_order = {colors[i]: i for i in range(len(colors)) }
		
class Card():
	"""
	Implement one card
	"""

	def __init__(self, color, height, disambiguation=None):
		"""
		Arguments:
			color (string): Must be in ["yellow", "blue", "white", "green", "red"]. 
						    Represents the color of a card
			height (int): Must be in [O] + range(2, 11). Represents the height of a card.
						  If 0, the card is a bet.
			dismabiguation (int): Must be in range(3). Make the three bets unique.
		"""
		self.color = color
		self.height = height
		self.disambiguation = disambiguation

	def __repr__(self):
		if self.disambiguation is None:
			return "%s %s"%(self.height, self.color)
		else:
			return "%s bet (%s)"%(self.color, self.disambiguation)

	def __lt__(self, other):
		if isinstance(other, Card):
			if (color_order[self.color] < color_order[other.color]):
				return True
			else:
				answer = (color_order[self.color] == color_order[other.color])
			return (answer and (self.height < other.height))
		else:
			return NotImplemented 

	def __gt__(self, other):
		if isinstance(other, Card):
			if (color_order[self.color] > color_order[other.color]):
				return True
			else:
				answer = (color_order[self.color] == color_order[other.color])
			return (answer and (self.height > other.height))
		else:
			return NotImplemented

	def __eq__(self, other):
		if isinstance(other, Card):
			return ((self.color == other.color) and (self.height == other.height))
		else:
			return NotImplemented
			

class Deck():
	"""
	Implement the deck.
	"""
	
	def __init__(self):
		self.cards = []
		self.reset()

	def reset(self):
		"""
		Reset the deck
		"""
		self.cards = [Card(color, 0, i) for i in range(3) for color in colors]

		for color in colors:
			for height in range(2, 11):
				self.cards.append(Card(color, height))

		np.random.shuffle(self.cards)

	def giveHands(self):
		"""
		Give two hands of 8 cards.
		Return:
			2-uple of lists of cards
		"""
		hand1, hand2 = [], []
		for i in range(8):
			hand1.append(self.pickaCard())
			hand2.append(self.pickaCard())
		return (hand1, hand2)

	def pickaCard(self):
		"""
		Return the card on the top on the deck.
		Return:
			Card
		"""
		if self.cards :
			card = self.cards[0]
			if len(self.cards) > 1:
				self.cards = self.cards[1:]
			else:
				self.cards = []
			return card
		else:
			raise ValueError("The deck is empty")

	def numberofCards(self):
		"""
		Return the number of cards left in the deck.
		"""
		return len(self.cards)

class Board():
	"""
	Implement the board
	"""

	def __init__(self):
		player1 = {color: [] for color in colors}
		player2 = {color: [] for color in colors}
		discardpile = {color: [] for color in colors}

		self.players = {0: discardpile, 1: player1, 2: player2}

	def reset(self):
		"""
		Reset the board to the initial position
		"""
		player1 = {color: [] for color in colors}
		player2 = {color: [] for color in colors}
		discardpile = {color: [] for color in colors}

		self.players = {0: discardpile, 1: player1, 2: player2}

	def canBePlayed(self, playerId, card):
		"""
		Check if a card can be played.
		Arguments:
			playerId (int): Id of the player who wants to play
			card (Card): card which will be tested
		Return:
			Boolean: True is the card can be played, false otherwise.
		"""
		if self.getHighestCard(playerId, card.color) is None:
			return True
		else:
			temp = (card.height >= self.getHighestCard(playerId, card.color).height)
			return (playerId == 0) or temp

	def getHighestCard(self, playerId, color):
		"""
		Return the highest card played by a player.
		Arguments:
			playerId (int): Id of the player
			color (string): Color to check
		Return:
			The highest card or -1 otherwise
		"""
		temp = self.players[playerId][color]
		if temp:
			return temp[-1]
		else:
			return None

	def getCards(self, playerId, color):
		"""
		Return the cards played by a player in one color
		Arguments:
			playerId (int): Id of the player
			color (string): Color to return
		Return:
			list of Cards
		"""
		return self.players[playerId][color]

	def getEverything(self):
		"""
		Return all information of the board
		Return:
			Dict
		"""
		return self.players

	def pickaDismissedCard(self, color):
		"""
		Return the latest card on a discard pile
		Arguments:
			color (string): color of the discard pile
		Return:
			Card 
		"""
		temp = self.players[0][color]
		if temp:
			answer = temp[-1]
			self.players[0][color] = self.players[0][color][: -1]
			return temp[-1]
		else:
			return None

	def playCard(self, playerId, card):
		"""
		Update the board when a card is played.
		Arguments:
			playerId (int): Id where the card is played 
							(playerId or 0 for the discard)
			card (Card): card which is played
		"""
		if self.canBePlayed(playerId, card):
			self.players[playerId][card.color].append(card)
		else:
			raise ValueError("Card can't be played")

	def countScore(self):
		scores = [0, 0]
		for i in range(1, 3):
			for color in colors:
				playedCards = self.players[i][color]
				if playedCards == []:
					continue
				if len(playedCards) > 7:
					toadd = 20
				else:
					toadd = 0
				temp = -20
				multiplier = 1
				while playedCards[0].height == 0:
					multiplier += 1
					playedCards = playedCards[1:]
					if len(playedCards) == 0:
						break
				temp += np.sum([card.height for card in playedCards])
				temp *= multiplier
				temp += toadd
				scores[i-1] += temp
		return scores	



if __name__ == "__main__":
	board = Board()
	deck = Deck()
	hand1, _ = deck.giveHands()
	for card in hand1:
		print(card)
		print(board.canBePlayed(1, card))
		if board.canBePlayed(1, card):
			board.playCard(1, card)
		else:
			board.playCard(0, card)
	for color in colors:
		try:
			print(board.pickaDismissedCard(color))
		except:
			print("Not appliable")

	for color in colors:
		print(board.getCards(1, color))
	print(board.getEverything())
