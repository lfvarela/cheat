import random
import numpy as np
import copy
import util

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
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    #np.random.rand() < .1
    if self.opponentBluffing(opponentClaims[-1], currentCards, putDownCards) or numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one card, favouring cards that are far away from last rank.
    randomIndex= self.drawFavoringFarCards(currentCards, opponentClaims[-1][0])
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    print("player {} is bluffing".format(0))
    return claim, cards

  #Assumes opponent is telling the truth most of the time. Finish this!
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    for putDown in putDownCards:
      util.addStacks(truth, putDown)
    util.addStacks(truth, util.claim2Cards(opponentClaim))
    for count in truth:
      if count > 4:
        return True
    return False

  def tellTruth(self, currentCards, lastRank):
    largestPossibleHand = None
    indexLargestPossibleHand = None
    sizeOfLargestPossibleHand = 0
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > sizeOfLargestPossibleHand:
        largestPossibleHand = [currentCards[index] if i == index else 0 for i in range(len(currentCards))]
        indexLargestPossibleHand = index
        sizeOfLargestPossibleHand = currentCards[index]
    if sizeOfLargestPossibleHand > 0 and largestPossibleHand != None and indexLargestPossibleHand != None:
      return (indexLargestPossibleHand, sizeOfLargestPossibleHand), largestPossibleHand
        #return (index, 1), [1 if i == index else 0 for i in range(len(currentCards))]
    return None, None

  #Returns index of a random card drawn from currentCards
  def drawFavoringFarCards(self, currentCards, lastRank):
    probs = [0] * 13
    for i, x in enumerate(currentCards):
      if x > 0:
        #gets smallest distance from lastRank to i (including wrap around)
        probs[i] = min(abs(lastRank - i), 13 - lastRank + i)
    s = float(sum(probs))
    return np.random.choice(len(probs), 1, p=[x/s for x in probs])[0]

  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

class DirectionalStartDeterministicBluffAccusation(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    #np.random.rand() < .1
    if self.opponentBluffing(opponentClaims[-1], currentCards, putDownCards) or numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one card, favouring cards that are far away from last rank.
    randomIndex= self.drawFavoringFarCards(currentCards, opponentClaims[-1][0])
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    print("player {} is bluffing".format(0))
    return claim, cards

  #Assumes opponent is telling the truth most of the time. Finish this!
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    for putDown in putDownCards:
      util.addStacks(truth, putDown)
    util.addStacks(truth, util.claim2Cards(opponentClaim))
    for count in truth:
      if count > 4:
        return True
    return False

  def tellTruth(self, currentCards, lastRank):
    largestPossibleHand = None
    indexLargestPossibleHand = None
    sizeOfLargestPossibleHand = 0
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > sizeOfLargestPossibleHand:
        largestPossibleHand = [currentCards[index] if i == index else 0 for i in range(len(currentCards))]
        indexLargestPossibleHand = index
        sizeOfLargestPossibleHand = currentCards[index]
    if sizeOfLargestPossibleHand > 0 and largestPossibleHand != None and indexLargestPossibleHand != None:
      return (indexLargestPossibleHand, sizeOfLargestPossibleHand), largestPossibleHand
        #return (index, 1), [1 if i == index else 0 for i in range(len(currentCards))]
    return None, None

  #Returns index of a random card drawn from currentCards
  def drawFavoringFarCards(self, currentCards, lastRank):
    probs = [0] * 13
    for i, x in enumerate(currentCards):
      if x > 0:
        #gets smallest distance from lastRank to i (including wrap around)
        probs[i] = min(abs(lastRank - i), 13 - lastRank + i)
    s = float(sum(probs))
    return np.random.choice(len(probs), 1, p=[x/s for x in probs])[0]

  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

class SheddingContenderWithDeterministicBluffAccusation(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    #np.random.rand() < .1
    if self.opponentBluffing(opponentClaims[-1], currentCards, putDownCards) or numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= self.uniformDraw(currentCards)
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    print("player {} is bluffing".format(0))
    return claim, cards

  #Assumes opponent is telling the truth most of the time. Finish this!
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    for putDown in putDownCards:
      util.addStacks(truth, putDown)
    util.addStacks(truth, util.claim2Cards(opponentClaim))
    for count in truth:
      if count > 4:
        return True
    return False

  def tellTruth(self, currentCards, lastRank):
    largestPossibleHand = None
    indexLargestPossibleHand = None
    sizeOfLargestPossibleHand = 0
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > sizeOfLargestPossibleHand:
        largestPossibleHand = [currentCards[index] if i == index else 0 for i in range(len(currentCards))]
        indexLargestPossibleHand = index
        sizeOfLargestPossibleHand = currentCards[index]
    if sizeOfLargestPossibleHand > 0 and largestPossibleHand != None and indexLargestPossibleHand != None:
      return (indexLargestPossibleHand, sizeOfLargestPossibleHand), largestPossibleHand
        #return (index, 1), [1 if i == index else 0 for i in range(len(currentCards))]
    return None, None

  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

class SheddingContender(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1 or numOpponentCards == 0: #Call bluff 10% of the time or when the opponent has no cards.
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= self.uniformDraw(currentCards)
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    print("player {} is bluffing".format(1))
    return claim, cards

  def tellTruth(self, currentCards, lastRank):
    largestPossibleHand = None
    indexLargestPossibleHand = None
    sizeOfLargestPossibleHand = 0
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > sizeOfLargestPossibleHand:
        largestPossibleHand = [currentCards[index] if i == index else 0 for i in range(len(currentCards))]
        indexLargestPossibleHand = index
        sizeOfLargestPossibleHand = currentCards[index]
    if sizeOfLargestPossibleHand > 0 and largestPossibleHand != None and indexLargestPossibleHand != None:
      return (indexLargestPossibleHand, sizeOfLargestPossibleHand), largestPossibleHand
    return None, None
    
  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

class DumbestContender(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= self.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1 or numOpponentCards == 0: #Call bluff 10% of the time or when the opponent has no cards.
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= self.uniformDraw(currentCards)
    cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
    claim = (opponentClaims[-1][0], 1)
    print("player {} is bluffing".format(1))
    return claim, cards

  def tellTruth(self, currentCards, lastRank):
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > 0:
        return (index, 1), [1 if i == index else 0 for i in range(len(currentCards))]
    return None, None
    
  #Returns index of a random card drawn from currentCards
  def uniformDraw(self, currentCards):
    s = float(sum(currentCards))
    return np.random.choice(len(currentCards), 1, p=[x/s for x in currentCards])[0]

