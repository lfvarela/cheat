from PlayerState import PlayerState
import util
import random

class GameState():
  def __init__(self, protagonistCards, contenderCards, currentPlayer):
    self.playerCards = [protagonistCards, contenderCards]
    self.currentPlayer = currentPlayer#random.randint(0,2)#random choice between player 0 or 1
    self.lastRank = None
    self.deck = [0] * 13
    self.lastCardsPlayed = None
    self.lastClaim = None
    self.playerPutDownCards = util.initEmptyDecks()
    self.playerClaims = util.initEmptyDecks()

  def getWinner(self):
    if sum(self.playerCards[0]) == 0:
      return 0
    return 1

  def gameEnded(self):
    return sum(self.playerCards[self.currentPlayer]) == 0

  def getCurrentPlayer(self):
    return self.currentPlayer

  def getCurrentPlayerState(self):
    return PlayerState(self.playerCards[self.currentPlayer], self.playerPutDownCards[self.currentPlayer], self.lastClaim[0] if self.lastClaim else None, len(self.playerCards[self.getCurrentOpponent()]), self.playerClaims[self.getCurrentOpponent()])

  def getLastClaim(self):
    return self.lastClaim

  def getLastCardsPlayed(self):
    return self.lastCardsPlayed

  def getCurrentOpponent(self):
    return self.opponentOf(self.currentPlayer)

  def opponentOf(self, player):
    return (player + 1)%2

  def penalise(self, player):
    util.transferStacks(self.playerCards[player], self.deck)
    self.reset(player)

  def reset(self, nextPlayer):
    self.lastClaim = None
    self.playerPutDownCards = util.initEmptyDecks()
    self.lastCardsPlayed = None
    self.currentPlayer = nextPlayer
    self.playerClaims = util.initEmptyDecks()


  #Update deck
  #Update player's cards
  #Update last card played
  #Update claims
  def putDownCards(self, action):
    claim, cardsPlayed = action
    util.addStacks(self.playerPutDownCards[self.currentPlayer], cardsPlayed)
    self.playerClaims[self.currentPlayer][claim[0]] += claim[1]
    util.moveStacks(self.deck, self.playerCards[self.currentPlayer], cardsPlayed)
    self.playerClaims[self.currentPlayer]
    self.lastCardsPlayed = cardsPlayed
    self.lastClaim = claim

  def changePlayer(self):
    self.currentPlayer = self.getCurrentOpponent()

  def sanityCheck(self):
    if not all(i >= 0 for i in self.playerCards[self.currentPlayer]):
      raise("Negative counts")
    if sum(self.deck) + sum(self.playerCards[self.currentPlayer]) + sum(self.playerCards[self.opponentOf(self.currentPlayer)]) != 52:
      raise("Does not sum")
    if not all(i >= 0 for i in self.deck):
      raise("Negative deck")
