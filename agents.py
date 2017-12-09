import random
import numpy as np
import copy
import util
from PlayerState import PlayerState

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:
  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index
    self.game = None

  def getAction(self, state):
    raiseNotDefined()

  def setGame(self, game):
    self.game = game

  # Returns any info we need after game ends. For Logistic Regression, return theta
  def endGame(self, i_won):
    return None


# Logistic regression. We store our belief of the opponent cards. We call bluff determinitically.
class LRwithOpponentBelief(Agent):

  def __init__(self, theta=None, explorationProb=0):
    self.theta = theta
    self.stateHistory = []
    self.explorationProb = explorationProb
    self.opponentBelief

  def getAction(self, state):
    self.stateHistory.append(state.featurize())

    # Call bluff scenarios: 10% of the times randomly, this will update our belief if the opponent is a bluffer or not. Determinitically if we are sure the opponent is bluffing.
    if (np.random.rand() < .1 and state.lastClaim is not None) or state.numOpponentCards == 0 or self.opponentBluffing(state.lastClaim, state.currentCards, state.putDownCards):
      return "Bluff", None

    possibleActions = self.getPossibleActions(state.currentCards, state.lastClaim)
    # epsilon-greedy exploration
    if random.random() < self.explorationProb:
        return random.choice(possibleActions)
    else:
        return max((self.getExpectedScore(state, action), action) for action in possibleActions)[1]

  #Return the expected score from taking action from state. Scores come from neural network.
  def getExpectedScore(self, state, action):
    if self.theta is None:
      self.theta = [0] * state.getNumFeatures()
    claim, handPlayed = action
    #1. Calculate expected score if opponent calls bluff.
    if util.currentPlayerBluffed(claim, handPlayed):
      # Opponent calls bluff on our bluff: bad for us
      new_hand_belief_b = util.addLists([state.currentCards, state.opponentClaims, state.putDownCards])
      opponentCallsBluffNS = PlayerState(new_hand_belief_b, None, None, state.numOpponentCards, None)

      # Opponent does not call bluff
      currCardsCopy = list(state.currentCards)
      util.substractStacks(currCardsCopy, handPlayed)
      opponentNotCallsBluffNS = PlayerState(currCardsCopy, None, claim, state.numOpponentCards, None)

      action_value = 0.1*util.h(self.theta, opponentCallsBluffNS.featurize()) + 0.9*util.h(self.theta, opponentNotCallsBluffNS.featurize())
      return action_value

    else: # Current Player did not bluff

      # Opponent calls bluff (and we did not bluff)
      currCardsCopy = list(state.currentCards)
      util.substractStacks(currCardsCopy, handPlayed)
      deck_belief = util.addLists([state.opponentClaims, state.putDownCards])
      opponentCallsBluffNS = PlayerState(currCardsCopy, None, None, state.numOpponentCards + sum(deck_belief), None)

      # Opponent does not call bluff (and we did not bluff)
      opponentNotCallsBluffNS = PlayerState(currCardsCopy, None, claim, state.numOpponentCards, None)
      action_value = 0.1*util.h(self.theta, opponentCallsBluffNS.featurize()) + 0.9*util.h(self.theta, opponentNotCallsBluffNS.featurize())
      return action_value

  # A deterministic check to see if opponent is bluffing. We always call bluff when this return true.
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    for putDown in putDownCards:
      util.addStacks(truth, putDown)
    util.addStacks(truth, util.claim2Cards(opponentClaim))
    for count in truth:
      if count > 4:
        return True
    return False

  def endGame(self, i_won):
    util.logistic_regression(self.theta, self.stateHistory[-20:], 1 if i_won else 0)
    return self.theta


# Logistic Regression, call bluff 10% of the time.
# Note, for our expected value of each state, we assume the opponent calls bluff 10% of the time, we will improve this or our next agent. 
class Protagonist(Agent):

  def __init__(self, theta=None, explorationProb=0):
    self.theta = theta
    self.stateHistory = []
    self.explorationProb = explorationProb

  def getAction(self, state):
    self.stateHistory.append(state.featurize())
    if (np.random.rand() < .1 and state.lastClaim is not None) or state.numOpponentCards == 0:
      return "Bluff", None
    possibleActions = self.getPossibleActions(state.currentCards, state.lastClaim)
    # epsilon-greedy exploration
    if random.random() < self.explorationProb:
        return random.choice(possibleActions)
    else:
        return max((self.getExpectedScore(state, action), action) for action in possibleActions)[1]

  #Return the expected score from taking action from state. Scores come from neural network.
  def getExpectedScore(self, state, action):
    if self.theta is None:
      self.theta = [0] * state.getNumFeatures()
    claim, handPlayed = action
    #1. Calculate expected score if opponent calls bluff.
    if util.currentPlayerBluffed(claim, handPlayed):
      # Opponent calls bluff on our bluff: bad for us
      new_hand_belief_b = util.addLists([state.currentCards, state.opponentClaims, state.putDownCards])
      opponentCallsBluffNS = PlayerState(new_hand_belief_b, None, None, state.numOpponentCards, None)

      # Opponent does not call bluff
      currCardsCopy = list(state.currentCards)
      util.substractStacks(currCardsCopy, handPlayed)
      opponentNotCallsBluffNS = PlayerState(currCardsCopy, None, claim, state.numOpponentCards, None)

      action_value = 0.1*util.h(self.theta, opponentCallsBluffNS.featurize()) + 0.9*util.h(self.theta, opponentNotCallsBluffNS.featurize())
      return action_value

    else: # Current Player did not bluff

      # Opponent calls bluff (and we did not bluff)
      currCardsCopy = list(state.currentCards)
      util.substractStacks(currCardsCopy, handPlayed)
      deck_belief = util.addLists([state.opponentClaims, state.putDownCards])
      opponentCallsBluffNS = PlayerState(currCardsCopy, None, None, state.numOpponentCards + sum(deck_belief), None)

      # Opponent does not call bluff (and we did not bluff)
      opponentNotCallsBluffNS = PlayerState(currCardsCopy, None, claim, state.numOpponentCards, None)
      action_value = 0.1*util.h(self.theta, opponentCallsBluffNS.featurize()) + 0.9*util.h(self.theta, opponentNotCallsBluffNS.featurize())
      return action_value

  def endGame(self, i_won):
    #util.logistic_regression(self.theta, self.stateHistory[-20:], 1 if i_won else 0)
    #return self.theta
    return [(x, 1 if i_won else 0) for x in self.stateHistory[-20:]] # Return last 20 states


  '''
  All possible actions, including lies, where the user claims to put down 1-4 cards.
  '''
  def getPossibleActions(self, currentCards, lastClaim):
    possibleActions = []
    if lastClaim is None:
        for rank, numCards in enumerate(currentCards):
          if numCards > 0:
            for claimRank in range(13):
              for putDown in range(1, 4 + 1):
                  if putDown <= numCards:
                      cardsPutDown = [putDown if i == rank else 0 for i in range(len(currentCards))]
                      claim = (claimRank, putDown)
                      possibleActions.append((claim, cardsPutDown))
    else:
        for rank, numCards in enumerate(currentCards):
          if numCards > 0:
            for dx in [-1,0,1]:
              for putDown in range(1, 4 + 1):
                  if putDown <= numCards:
                      claimRank = (lastClaim[0] + dx) % len(currentCards)
                      cardsPutDown = [putDown if i == rank else 0 for i in range(len(currentCards))]
                      claim = (claimRank, putDown)
                      possibleActions.append((claim, cardsPutDown))
    return possibleActions


  '''
  All possible actions, including bluffs, where the user claims to put down 1 card.
  '''
  '''
  def getPossibleActions(self, currentCards, lastClaim):
    possibleActions = []
    if lastClaim is None:
        for rank, numCards in enumerate(currentCards):
          if numCards > 0:
            for claimRank in range(13):
              cardsPutDown = util.buildPutDownCardsOfOne(rank, len(currentCards))
              claim = (claimRank, 1)
              possibleActions.append((claim, cardsPutDown))
    else:
        for rank, numCards in enumerate(currentCards):
          if numCards > 0:
            for dx in [-1,0,1]:
              claimRank = (lastClaim[0] + dx) % len(currentCards)
              cardsPutDown = util.buildPutDownCardsOfOne(rank, len(currentCards))
              claim = (claimRank, 1)
              possibleActions.append((claim, cardsPutDown))
    return possibleActions
    '''

    '''
    TODO: I think we can delete this.
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
'''

class DirectionalStartDeterministicAccusation(Agent):
  def getAction(self, state):
    if state.lastClaim is None:
      #Play one card and tell the truth
      randomIndex= util.drawFavoringCloseCards(state.currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(state.currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if self.opponentBluffing(state.lastClaim, state.currentCards, state.putDownCards) or state.numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(state.currentCards, state.lastClaim[0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one card, favouring cards that are far away from last rank.
    randomIndex= util.drawFavoringFarCards(state.currentCards, state.lastClaim[0])
    cards = [1 if i == randomIndex else 0 for i in range(len(state.currentCards))]
    claim = (state.lastClaim[0], 1)
    #print("player {} is bluffing".format(0))
    return claim, cards

  #Assumes opponent is telling the truth most of the time. Finish this!
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    util.addStacks(truth, putDownCards)
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
  def getAction(self, state):
    if state.lastClaim is None:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(state.currentCards)
      cards = [1 if i == randomIndex else 0 for i in range(len(state.currentCards))]
      claim = (randomIndex, 1)
      return claim, cards
    if self.opponentBluffing(state.lastClaim, state.currentCards, state.putDownCards) or state.numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(state.currentCards, state.lastClaim[0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one card, favouring cards that are far away from last rank.
    randomIndex= util.drawFavoringFarCards(state.currentCards, state.lastClaim[0])
    cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
    claim = (state.lastClaim[0], 1)
    #print("player {} is bluffing".format(0))
    return claim, cards

  #Assumes opponent is telling the truth most of the time. Finish this!
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    util.addStacks(truth, putDownCards)
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
  def getAction(self, state):
    if state.lastClaim is None:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(state.currentCards)
      cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
      claim = (randomIndex, 1)
      return claim, cards
    #np.random.rand() < .1
    if self.opponentBluffing(state.lastClaim, state.currentCards, state.putDownCards) or state.numOpponentCards == 0:
      return "Bluff", None
    claim, cards = self.tellTruth(state.currentCards, state.lastClaim[0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= util.uniformDraw(state.currentCards)
    cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
    claim = (state.lastClaim[0], 1)
    #print("player {} is bluffing".format(0))
    return claim, cards

  #Assumes opponent is telling the truth most of the time. Finish this!
  def opponentBluffing(self, opponentClaim, currentCards, putDownCards):
    truth = copy.copy(currentCards)
    #for putDown in putDownCards:
      #util.addStacks(truth, putDown)
    util.addStacks(truth, putDownCards)
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
  def __init__(self):
    self.stateHistory = []

  def getAction(self, state):
    state_memory = 20 # Number of states the contender stores
    if len(self.stateHistory) > 20:
        self.stateHistory.pop(0)
    self.stateHistory.append(state.featurize())
    if state.lastClaim is None:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(state.currentCards)
      cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1 or state.numOpponentCards == 0: #Call bluff 10% of the time or when the opponent has no cards.
      return "Bluff", None
    claim, cards = self.tellTruth(state.currentCards, state.lastClaim[0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= util.uniformDraw(state.currentCards)
    cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
    claim = (state.lastClaim[0], 1)
    #print("player {} is bluffing".format(1))
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

  def endGame(self, i_won):
    return [(x, 1 if i_won else 0) for x in self.stateHistory[-20:]]

class DumbestContender(Agent):
  def __init__(self):
    self.stateHistory = []

  def getAction(self, state):
    state_memory = 20 # Number of states the contender stores
    if len(self.stateHistory) > 20:
        self.stateHistory.pop(0)
    self.stateHistory.append(state.featurize())
    if state.lastClaim is None:
      #Play one card and tell the truth
      randomIndex= util.uniformDraw(state.currentCards)
      cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
      claim = (randomIndex, 1)
      return claim, cards
    if np.random.rand() < .1 or state.numOpponentCards == 0: #Call bluff 10% of the time or when the opponent has no cards.
      return "Bluff", None
    claim, cards = self.tellTruth(state.currentCards, state.lastClaim[0])
    if cards != None:
      return claim, cards
    #Must lie. Draw one random card from currentCards and claim same as opponent's last card
    randomIndex= util.uniformDraw(state.currentCards)
    cards = util.buildPutDownCardsOfOne(randomIndex, len(state.currentCards))
    claim = (state.lastClaim[0], 1)
    #print("player {} is bluffing".format(1))
    return claim, cards

  def tellTruth(self, currentCards, lastRank):
    for i in np.random.permutation([-1,0,1]):
      index = (lastRank + i) % len(currentCards)
      if currentCards[index] > 0:
        return (index, 1), util.buildPutDownCardsOfOne(index, len(currentCards))
    return None, None

  def endGame(self, i_won):
    return [(x, 1 if i_won else 0) for x in self.stateHistory[-20:]]
