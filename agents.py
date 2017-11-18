import random
import numpy as np
import copy
import util
import State

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:
  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    raiseNotDefined()

class Protagonist(Agent):

  def __init__(self, theta=None):
    self.theta = theta

  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if np.random.rand() < .1 or numOpponentCards == 0:
      return "Bluff", None
    currentState = State(currentCards, putDownCards, opponentClaims[-1], numOpponentCards)
    possibleActions = self.getPossibleActions(currentCards, opponentClaims[-1][0])
    # epsilon-greedy exploration
    explorationProb = 0.1
    if random.random() < explorationProb:
        return random.choice(possibleActions)
    else:
        return max((self.getExpectedScore(currentState, action), action) for action in possibleActions)[1]

  #Return the expected score from taking action from state. Scores come from neural network.
  def getExpectedScore(self, state, action):
    if self.theta is None:
      self.theta = [0] * state.getNumFeatures()
    claim, handPlayed = action
    #1. Calculate expected score if opponent calls bluff.
    if currentPlayerBluffed(claim, handPlayed):
      


  def getPossibleActions(self, currentCards, currentRank):
    possibleActions = []
    for rank, numCards in enumerate(currentCards):
      if numCards > 0:
        for dx in [-1,0,1]:
          claimRank = (rank + dx) % len(currentCards)
          cardsPutDown = util.buildPutDownCardsOfOne(rank, len(currentCards))
          claim = (claimRank, 1)
          possibleActions.append((claim, cardsPutDown))
    return possibleActions

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
    return None, None


class DirectionalStartDeterministicAccusation(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= util.drawFavoringCloseCards(currentCards)
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
    randomIndex= util.drawFavoringFarCards(currentCards, opponentClaims[-1][0])
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
    return None, None

class DirectionalBluffDeterministicBluffAccusation(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if self.opponentBluffing(opponentClaims[-1], currentCards, putDownCards) or numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one card, favouring cards that are far away from last rank.
    randomIndex= util.drawFavoringFarCards(currentCards, opponentClaims[-1][0])
    cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
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

class SheddingContenderWithDeterministicBluffAccusation(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(currentCards)
      cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
      claim = (randomIndex, 1)
      return claim, cards
    #np.random.rand() < .1
    if self.opponentBluffing(opponentClaims[-1], currentCards, putDownCards) or numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= util.uniformDraw(currentCards)
    cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
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

class SheddingContender(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(currentCards)
      cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1 or numOpponentCards == 0: #Call bluff 10% of the time or when the opponent has no cards.
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= util.uniformDraw(currentCards)
    cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
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

class DumbestContender(Agent):
  def getAction(self, currentCards, putDownCards, opponentClaims, currentClaims, numOpponentCards):
    if len(opponentClaims) == 0:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(currentCards)
      cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1 or numOpponentCards == 0: #Call bluff 10% of the time or when the opponent has no cards.
      return "Bluff", None
    claim, cards = self.tellTruth(currentCards, opponentClaims[-1][0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= util.uniformDraw(currentCards)
    cards = util.buildPutDownCardsOfOne(randomIndex, len(currentCards))
    claim = (opponentClaims[-1][0], 1)
    print("player {} is bluffing".format(1))
    return claim, cards

  def tellTruth(self, currentCards, lastRank):
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > 0:
        return (index, 1), util.buildPutDownCardsOfOne(index, len(currentCards))
    return None, None
