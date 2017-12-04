import random
import numpy as np
import copy
import util
import agents
from GameState import GameState

'''
Action[0] = (rank, numCards)
Action[1] = counts of cards in hand played
'''
class Game():
  def __init__(self, protagonist, contender):
    protagonist.setGame(self)
    contender.setGame(self)
    self.players = [protagonist, contender]
    protagonistCards = [0] * 13
    contenderCards = [0] * 13
    initialCards = []
    for _ in range(4):
      for i in range(0,13):
        initialCards.append(i)
    for _ in range(26):
      protagonistCards[initialCards.pop(random.randint(0,len(initialCards)-1))]+=1
      contenderCards[initialCards.pop(random.randint(0,len(initialCards)-1))]+=1
    self.gameState = GameState(protagonistCards, contenderCards, 0)

  def run(self):
    gameState = self.gameState
    while not gameState.gameEnded():
      print("It is player {} turn".format(gameState.getCurrentPlayer()))
      gameState.sanityCheck()
      action = self.players[gameState.getCurrentPlayer()].getAction(gameState.getCurrentPlayerState())
      print("claim: {}".format(action[0]))
      print("cardsPlayed: {}".format(action[1]))
      self.updateGameState(action)
      print("")
      print("")
    return gameState.getWinner()

  def updateGameState(self, action):
    claim, cardsPlayed =action
    gameState = self.gameState
    if claim == "Bluff":
      opponentBluffed = self.didOpponentBluff(gameState.getLastClaim(), gameState.getLastCardsPlayed())
      if opponentBluffed:
        print("player {} was caught bluffing".format(gameState.getCurrentOpponent()))
        gameState.penalise(gameState.getCurrentOpponent())
      else:
        print("player {} called bluff incorrectly".format(gameState.getCurrentPlayer()))
        gameState.penalise(gameState.getCurrentPlayer())
    else:
      gameState.putDownCards(action)
      gameState.changePlayer()

  def didOpponentBluff(self, opponentClaim, cardsLastPlayed):
    cardIndex = opponentClaim[0]
    return opponentClaim[1] != cardsLastPlayed[cardIndex]

#game = Game(Protagonist(), DumbestContender())
#print("player {} won".format(game.run()))
winners = []
for _ in range(1000):
  game = Game(agents.DumbestContender(), agents.DumbestContender())
  winners.append(game.run())
print("player 0 won: {}".format( float(len(winners) - sum(winners)) / len(winners) ))
print("player 1 won: {}".format( float(sum(winners)) / len(winners) ))

#test = [5, 7, 3, 0, 0, 0, 1, 2, 3, 10, 1, 1, 5]
#print(util.drawFavoringCloseCards(test))
