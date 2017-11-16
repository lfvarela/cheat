import random

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
  def __init__(self):
    pass

  def getAction(self, gameState):
    pass

class Contender(Agent):
  def __init__(self):
    pass

  def getAction(self, gameState):
    pass

class Game:
  def __init__(self):
    self.protagonist = Protagonist()
    self.playerCards = [[],[]]
    self.playerClaims = [[],[]]
    self.contender = Contender()
    initialCards = []
    for _ in range(4):
      for i in range(1,14):
        initialCards.append(i)
    for _ in range(26):
      self.playerCards[0].append(initialCards.pop(random.randint(0,len(initialCards)-1)))
      self.playerCards[1].append(initialCards.pop(random.randint(0,len(initialCards)-1)))
    self.deck = []
    self.currentPlayer = 0

  def run(self):
    while not self.gameEnded():
      opponentClaims = self.playerClaims[(self.currentPlayer + 1)%2]
      currentPlayerClaims = self.playerClaims[self.currentPlayer]
      currentPlayerCards = self.playerCards[self.currentPlayer]
      claim, cards = self.currentPlayer.getAction(currentPlayerCards, opponentClaims, currentPlayerClaims)
      if claim == "Bluff":
        opponentBluffed = didOpponentBluff(opponentClaims[-1])
        if opponentBluffed:
          print("player {} was caught bluffing".format((self.currentPlayer + 1)%2))
          self.playerClaims = [[],[]]
          self.playerCards[(self.currentPlayer+1)%2].extend(self.deck) #bluffing player gets deck
          self.currentPlayer = (self.currentPlayer+1)%2 #the new player is the opponent
        else:
          print("player {} incorrectly called bluff".format(self.currentPlayer))
          self.playerClaims = [[],[]]
          self.playerCards[self.currentPlayer].extend(self.deck)
          
      else:
        currentPlayerClaims.append(claim)
        self.deck.extend(cards)
    print("player {} won".format(self.getWinner()))

  def gameEnded(self):
    return len(self.playerCards[0]) == 0 or len(self.playerCards[1]) == 0

  def didOpponentBluff(opponentClaim):
    return opponentClaim == self.deck[-len(opponentClaim):]

game = Game()
print(game.protagonistCards)
print(game.opponentCards)



