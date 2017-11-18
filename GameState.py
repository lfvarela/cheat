from PlayerState import PlayerState
import util

class GameState():
  def __init__(self, protagonistCards, contenderCards, currentPlayer):
    self.playerCards = [protagonistCards, contenderCards]
    self.currentPlayer = currentPlayer
    self.lastRank = None
    self.deck = [0] * 13
    self.lastCardsPlayed = None
    self.lastClaim = None
    self.playerPutDownCards = [[],[]]

  def getWinner(self):
    if sum(self.playerCards[0]) == 0:
      return 0
    return 1

  def gameEnded(self):
    return sum(self.playerCards[self.currentPlayer]) == 0

  def getCurrentPlayer(self):
    return self.currentPlayer

  def getCurrentPlayerState(self):
    return PlayerState(self.playerCards[self.currentPlayer], self.playerPutDownCards[self.currentPlayer], self.lastClaim, len(self.playerCards[self.getCurrentOpponent()]))

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
    self.playerPutDownCards = [[],[]]
    self.lastCardsPlayed = None
    self.currentPlayer = nextPlayer

  #Update deck
  #Update player's cards
  #Update last card played
  #Update claims
  def putDownCards(self, action):
    claim, cardsPlayed = action
    util.moveStacks(self.deck, self.playerCards[self.currentPlayer], cardsPlayed)
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