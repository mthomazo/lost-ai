# coding: utf-8

import players
import gamehandler
import numpy as np

class Game():

	def __init__(self, typePlayer1, typePlayer2, numberOfRounds, verbose=False):
		self.numberOfRounds = numberOfRounds
		if typePlayer1 == "ai":
			self.player1 = players.AI(1)
		elif typePlayer1 == "human":
			self.player1 = players.Human(1)
		elif typePlayer1 == "test":
			self.player1 = players.Player(1)
		else:
			raise ValueError("typePlayer1 not understood")
		if typePlayer2 == "ai":
			self.player2 = players.AI(2)
		elif typePlayer2 == "human":
			self.player2 = players.Human(2)
		elif typePlayer2 == "test":
			self.player2 = players.Player(2)
		else:
			raise ValueError("typePlayer2 not understood")
		self.scores = [0, 0]
		self.verbose = verbose

	def play(self):

		whoPlay = np.random.randint(0, 2)
		deck = gamehandler.Deck()
		board = gamehandler.Board()

		for nb_round in range(self.numberOfRounds):

			deck.reset()
			board.reset()

			hand1, hand2 = deck.giveHands()
			self.player1.setHand(hand1)
			self.player2.setHand(hand2)

			while deck.numberofCards() > 0:

				if whoPlay == 0:
					currentPlayer =	self.player1
					whoPlay = 1
				else:
					currentPlayer = self.player2
					whoPlay = 0

				cardToBePlayed, whereisplayed = currentPlayer.play(board)
				while not  board.canBePlayed(whereisplayed, cardToBePlayed):
					cardToBePlayed, whereisplayed = currentPlayer.play(board)
				
				if self.verbose:
					print(currentPlayer, "is playing")
					print("Current Player hands is :")
					for card in currentPlayer.hand:
						print(card)
					if whereisplayed == 0:
						print(currentPlayer, "dismiss", cardToBePlayed)
					else:
						print(currentPlayer, "plays", cardToBePlayed)
				currentPlayer.removeFromHand(cardToBePlayed)
				board.playCard(whereisplayed, cardToBePlayed)

				whereToDraw = currentPlayer.draw(board)
				hasdrawed = False
				while not hasdrawed:
					if whereToDraw == "deck":
						currentPlayer.addtoHand(deck.pickaCard())
						hasdrawed = True
					else:
						cardToDraw = board.pickaDismissedCard(whereToDraw)
						if cardToDraw is not None:
							currentPlayer.addtoHand(cardToDraw)
							hasdrawed = True
						else:
							whereToDraw = currentPlayer.draw(board)
			scorestemp = board.countScore()
			self.scores[0] += scorestemp[0]
			self.scores[1] += scorestemp[1]

		print(self.scores)
		if self.scores[0] > self.scores[1]:
			print("PLAYER 1 WINS")
		elif self.scores[0] < self.scores[1]:
			print("PLAYER 2 WINS")
		else:
			print("DRAW")


if __name__ == "__main__":

	for i in range(1):
		game = Game("ai", "test", 1, verbose=True)
		game.play()







