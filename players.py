# coding: utf-8

from gamehandler import Card, colors

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

	def __repr__(self):
		return ("Player %s"%self.playerId)

	def setHand(self, hand):
		"""
		Set the hand of the player
		Arguments:
			hand (list of Card): hand of the player
		"""
		self.hand = []
		for card in hand:
			self.addtoHand(card)

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
		if board.canBePlayed(self.playerId, temp):
			return (temp, self.playerId)
		else:
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
		if len(self.hand) == 0:
			self.hand = [card]
		else:
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

class Human(Player):
	pass

class AI(Player):

	def play(self, board):
		must_played = self._mustplayed(board)
		if must_played is not None:
			print("MUST PLAY")
			return(must_played, self.playerId)
		hand_temp = self.hand
		i_temp = 0
		cardToPlay = None
		whereToPlay = self.playerId
		while cardToPlay is None:
			if hand_temp != []:
				card_temp = hand_temp[0]
				i_temp = 0
				for i, card in enumerate(hand_temp):
					if card.height < card_temp.height:
						i_temp = i
						card_temp = card
				if board.canBePlayed(self.playerId, card_temp):
					cardToPlay = card_temp
				else:
					if i_temp == 0:
						hand_temp = hand_temp[1:]
					elif i_temp == len(hand_temp) - 1:
						hand_temp = hand_temp[:-1]
					else:
						hand_temp = hand_temp[:i_temp] + hand_temp[i_temp+1:]
			else:
				whereToPlay = 0
				card_temp = self.hand[0]
				for card in self.hand:
					if card.height < card_temp.height:
						card_temp = card
				cardToPlay = card_temp
		return (cardToPlay, whereToPlay)

	def _mustplayed(self, board):
		for color in colors:
			temp = board.getHighestCard(self.playerId, color)
			if temp is not None:
				if temp.height != 0:
					for card in self.hand:
						if card == Card(temp.color, temp.height + 1):
							return card
		return None

	def draw(self, board):
		for color in colors:
			temp = board.getHighestCard(0, color)
			if temp is not None:
				if board.canBePlayed(self.playerId, temp):
					return color
		return "deck"


				




