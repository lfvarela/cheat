import random
import numpy as np
import copy
import util
import agents

class Game:
  def __init__(self, protagonist, contender):
    self.players= [protagonist, contender]
    protagonistCards = [0] * 13
    contenderCards = [0] * 13
    self.playerCards = [protagonistCards,contenderCards]
    self.playerClaims = [[],[]]
    self.playerPutDownCards = [[],[]]
    initialCards = []
    for _ in range(4):
      for i in range(0,13):
        initialCards.append(i)
    for _ in range(26):
      self.playerCards[0][initialCards.pop(random.randint(0,len(initialCards)-1))]+=1
      self.playerCards[1][initialCards.pop(random.randint(0,len(initialCards)-1))]+=1
    self.deck = [0] * 13
    self.currentPlayer = 0
    self.cardsLastPlayed = None

  def run(self):
    while not self.gameEnded():
      print("check: {}".format(sum(self.deck) + sum(self.playerCards[self.currentPlayer]) + sum(self.playerCards[self.opponentOf(self.currentPlayer)])))
      print("It is player {} turn".format(self.currentPlayer))
      opponentClaims = self.playerClaims[self.opponentOf(self.currentPlayer)]
      currentPlayerClaims = self.playerClaims[self.currentPlayer]
      currentPlayerPutDownCards = self.playerPutDownCards[self.currentPlayer]
      currentPlayerCards = self.playerCards[self.currentPlayer]
      claim, cardsPlayed = self.players[self.currentPlayer].getAction(currentPlayerCards, currentPlayerPutDownCards, opponentClaims, currentPlayerClaims, sum(self.playerCards[self.opponentOf(self.currentPlayer)]))
      print("claim: {}".format(claim))
      print("cardsPlayed: {}".format(cardsPlayed))
      if claim == "Bluff":
        opponentBluffed = self.didOpponentBluff(opponentClaims[-1], self.cardsLastPlayed)
        if opponentBluffed:
          print("player {} was caught bluffing".format(self.opponentOf(self.currentPlayer)))
          self.penalise(self.opponentOf(self.currentPlayer))
          self.reset(self.opponentOf(self.currentPlayer))
        else:
          print("player {} called bluff incorrectly".format(self.currentPlayer))
          self.penalise(self.currentPlayer)
          self.reset(self.currentPlayer)
      else:
        self.putDownCards(claim, cardsPlayed)
        self.playerPutDownCards[self.currentPlayer].append(cardsPlayed)
        self.currentPlayer = self.opponentOf(self.currentPlayer)
      print("")
      print("")
    #print("player {} won".format(self.getWinner()))
    return self.getWinner()

  def getWinner(self):
    if sum(self.playerCards[0]) == 0:
      return 0
    return 1

  #weird bug.
  def gameEnded(self):
    return sum(self.playerCards[self.currentPlayer]) == 0

  def didOpponentBluff(self, opponentClaim, cardsLastPlayed):
    cardIndex = opponentClaim[0]
    return opponentClaim[1] != cardsLastPlayed[cardIndex]

  def opponentOf(self, player):
    return (player + 1)%2

  def penalise(self, player):
    util.transferStacks(self.playerCards[player], self.deck)

  def reset(self, nextPlayer):
    self.playerClaims = [[],[]]
    self.playerPutDownCards = [[],[]]
    self.cardsLastPlayed = None
    self.currentPlayer = nextPlayer

  def penaliseCurrentPlayer(self):
    print("player {} incorrectly called bluff".format(self.currentPlayer))
    self.playerClaims = [[],[]]
    self.playerCards[self.currentPlayer].extend(self.deck)
    self.currentPlayer = self.currentPlayer #currentPlayer incorrectly bluffed so its his turn.
    self.currentRank = None

  #Update deck
  #Update player's cards
  #Update last card played
  #Update claims
  def putDownCards(self, claim, cardsPlayed):
    util.moveStacks(self.deck, self.playerCards[self.currentPlayer], cardsPlayed)
    self.cardsLastPlayed = cardsPlayed
    self.playerClaims[self.currentPlayer].append(claim)


#game = Game(Protagonist(), DumbestContender())
#print("player {} won".format(game.run()))
winners = []
for _ in range(100):
  game = Game(agents.Protagonist(), agents.SheddingContenderWithDeterministicBluffAccusation())
  winners.append(game.run())
print("player 0 won: {}".format( float(len(winners) - sum(winners)) / len(winners) ))
print("player 1 won: {}".format( float(sum(winners)) / len(winners) ))
