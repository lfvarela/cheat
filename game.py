import random
import numpy as np
import copy
import util
import agents
from GameState import GameState
from random import shuffle

'''
Action[0] = (rank, numCards) # Claim
Action[1] = counts of cards in hand played
'''
class Game():
  def __init__(self, protagonist, contender, verbose=False):
    self.verbose = verbose
    protagonist.setGame(self)
    contender.setGame(self)
    self.players = [protagonist, contender]
    protagonistCards = [0] * 13
    contenderCards = [0] * 13
    initialCards = []
    for _ in range(4):
      for i in range(0,13):
        initialCards.append(i)
    shuffle(initialCards)
    for i in range(26):
      protagonistCards[initialCards[i]]+=1
    for i in range(26, 52):
      contenderCards[initialCards[i]]+=1
    self.gameState = GameState(protagonistCards, contenderCards, random.randint(0,1))

  def run(self):
    gameState = self.gameState
    while not gameState.gameEnded():
      if self.verbose: print("It is player {} turn".format(gameState.getCurrentPlayer()))
      gameState.sanityCheck()
      action = self.players[gameState.getCurrentPlayer()].getAction(gameState.getCurrentPlayerState())
      if self.verbose: print("claim: {}".format(action[0]))
      if self.verbose: print("cardsPlayed: {}".format(action[1]))
      if self.verbose: print("currCards: {}").format(gameState.playerCards[gameState.getCurrentPlayer()])
      if self.verbose: print("num bluffs: {}").format(gameState.numBluffs[gameState.getCurrentPlayer()])
      if self.verbose: print("num non bluffs: {}").format(gameState.numNonBluffs[gameState.getCurrentPlayer()])
      self.updateGameState(action)
      if self.verbose: print("")
      if self.verbose: print("")
      gameState.incrTurn()
      if gameState.numTurns > 1000: return 0.5 #Call it a draw
    return gameState.getWinner()

  def updateGameState(self, action):
    claim, cardsPlayed = action
    gameState = self.gameState
    if claim == "Bluff":
      gameState.incrBluff(gameState.getCurrentPlayer())
      opponentBluffed = self.didOpponentBluff(gameState.getLastClaim(), gameState.getLastCardsPlayed())
      if opponentBluffed:
        if self.verbose: print("player {} was caught bluffing".format(gameState.getCurrentOpponent()))
        gameState.penalise(gameState.getCurrentOpponent())
      else:
        if self.verbose: print("player {} called bluff incorrectly".format(gameState.getCurrentPlayer()))
        gameState.penalise(gameState.getCurrentPlayer())
    else:
      gameState.incrNonBluff(gameState.getCurrentPlayer())
      gameState.putDownCards(action)
      gameState.changePlayer()

  def didOpponentBluff(self, opponentClaim, cardsLastPlayed):
    cardIndex = opponentClaim[0]
    return opponentClaim[1] != cardsLastPlayed[cardIndex]
