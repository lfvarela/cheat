import random
import numpy as np

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    raiseNotDefined()

class Protagonist(Agent):
  def getAction(self, currentCards, opponentClaims, currentClaims):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1: #Call bluff 10% of the time
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= self.uniformDraw(currentCards)
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    return claim, cards

  def tellTruth(self, currentCards, lastRank):
    for i in [-1,0,1]:
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > 0:
        return (index, 1), [1 if i == index else 0 for i in range(len(currentCards))]
    return None, None

  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

class Contender(Agent):
  def getAction(self, currentCards, opponentClaims, currentClaims):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1: #Call bluff 10% of the time
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= self.uniformDraw(currentCards)
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    return claim, cards

  def tellTruth(self, currentCards, lastRank):
    for i in [-1,0,1]:
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > 0:
        return (index, 1), [1 if i == index else 0 for i in range(len(currentCards))]
    return None, None
    
  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

class Game:
  def __init__(self):
    self.players= [Protagonist(), Contender()]
    protagonistCards = [0] * 13
    contenderCards = [0] * 13
    self.playerCards = [protagonistCards,contenderCards]
    self.playerClaims = [[],[]]
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
      opponentClaims = self.playerClaims[self.opponentOf(self.currentPlayer)]
      currentPlayerClaims = self.playerClaims[self.currentPlayer]
      currentPlayerCards = self.playerCards[self.currentPlayer]
      claim, cardsPlayed = self.players[self.currentPlayer].getAction(currentPlayerCards, opponentClaims, currentPlayerClaims)
      if claim == "Bluff":
        opponentBluffed = self.didOpponentBluff(opponentClaims[-1], self.cardsLastPlayed)
        if opponentBluffed:
          print("player {} was caught bluffing".format(self.opponentOf(self.currentPlayer)))
          self.penalise(self.opponentOf(self.currentPlayer))
          self.reset(self.opponentOf(self.currentPlayer))
        else:
          self.penalise(self.currentPlayer)
          self.reset(self.currentPlayer)
      else:
        self.putDownCards(claim, cardsPlayed)
        self.currentPlayer = self.opponentOf(self.currentPlayer)
    print("player {} won".format(self.getWinner()))

  def getWinner(self):
    if sum(self.playerCards[0]) == 0:
      return 0
    return 1

  def gameEnded(self):
    return sum(self.playerCards[0]) == 0 or sum(self.playerCards[1]) == 0

  def didOpponentBluff(self, opponentClaim, cardsLastPlayed):
    cardIndex = opponentClaim[0]
    return opponentClaim[1] == cardsLastPlayed[cardIndex]

  def opponentOf(self, player):
    return (player + 1)%2

  def penalise(self, player):
    self.transferStacks(self.playerCards[player], self.deck)

  def reset(self, nextPlayer):
    self.playerClaims = [[],[]]
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
    self.moveStacks(self.deck, self.playerCards[self.currentPlayer], cardsPlayed)
    self.cardsLastPlayed = cardsPlayed
    self.playerClaims[self.currentPlayer].append(claim)

  #We're gonna move cards from source to target
  def moveStacks(self, target, source, cards):
    for i in range(len(target)):
      target[i] += cards[i]
      source[i] -= cards[i]

  def transferStacks(self, target, source):
    self.moveStacks(target, source, source)

game = Game()
game.run()
