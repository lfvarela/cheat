import numpy as np
import math
import pickle

'''
A bunch of helper functions
'''

# Adds source to target without changing source.
# Note this method is unlike moveStacks, which changes source
def addStacks(target, source):
  for i in range(len(target)):
    target[i] += source[i]


# Decrements target by source without changing source.
def substractStacks(target, source):
  for i in range(len(target)):
    target[i] -= source[i]


# Adds cards from source to target. Changes source by decrementing
#nsource by cards.
def moveStacks(target, source, cards):
  for i in range(len(target)):
    target[i] += cards[i]
    source[i] -= cards[i]


# Moves all of source over to target. Note that source == [0]*13 after.
def transferStacks(target, source):
  moveStacks(target, source, source)


# Takes a claim and returns its equivalent "hand" representation.
def claim2Cards(claim):
  return [claim[1] if i == claim[0] else 0 for i in range(13)]


def uniformDraw(probs):
  s = float(sum(probs))
  return np.random.choice(len(probs), 1, p=[x/s for x in probs])[0]


# Returns index of a random card drawn from currentCards
def drawFavoringFarCards(currentCards, lastRank):
  probs = [0] * 13
  for i, x in enumerate(currentCards):
    if x > 0:
      #gets smallest distance from lastRank to i (including wrap around)
      probs[i] = min(abs(lastRank - i), 13 - lastRank + i)
  return uniformDraw(probs)


def drawFavoringCloseCards(currentCards):
  probs = [0] * 13
  for i, count in enumerate(currentCards):
    if count > 0:
      weight = 0
      for distance in range(1,7):
        leftIndex = (i - distance) % len(currentCards)
        rightIndex = (i + distance) % len(currentCards)
        weight += float(currentCards[leftIndex] + currentCards[rightIndex]) / distance
      probs[i] = weight
  return uniformDraw(probs)


# Logistic regression for our game.
# states: list of states, where a state is a list of feature values
# result: For now: either 1 or 0, 1 represents that all states in states led to a win. 0 to a lose
# alpha: step size?
#
# states is a 29 element list (0 - 12: reformatted radial counts of agent cards, 13 - 25: cards played standard format, 28: number of opponent cards, 29: offset coefficient)
# Update rule: https://www.dropbox.com/s/2ywl9jw7aujj0ss/Screenshot%202017-11-16%2022.05.01.png?dl=0
# CS 229 lecture notes: http://cs229.stanford.edu/notes/cs229-notes1.pdf
def logistic_regression(theta, states, result, alpha=0.001):
  for state in states:
    for j in range(len(theta)):
      theta[j] += alpha*(result - h(theta, state))*state[j]


def logistic_regression_on_data(theta, train_data, alpha=0.001):
  for x, y in train_data:
    for j in range(len(theta)):
      theta[j] += alpha*(y - h(theta, x))*x[j]

def logistic_reg_test(theta, x, y, alpha=0.001):
  for i in range(len(x)):
    print(i)
    for j in range(len(theta)):
      theta[j] += alpha*(y[i] - h(theta, x[i]))*x[i][j]


def h(theta, features):
  prod = sum([theta[i]*features[i] for i in range(len(theta))])
  return sigmoid(prod)

def neuralNetworkPredict(model, features):
  return model.predict(np.reshape(features, (-1, len(features)))) > 0.5

def sigmoid(z):
  return 1.0/float(1 + math.exp(-z))


def getRadialVector(currentCards, lastRank):
  radialVector = [0]*len(currentCards)
  middleIndex = 6
  radialVector[middleIndex] = currentCards[lastRank]
  for distance in range(1,7):
    radialVector[middleIndex - distance] = currentCards[(lastRank-distance)%len(currentCards)]
    radialVector[middleIndex + distance] = currentCards[(lastRank+distance)%len(currentCards)]
  return radialVector


def buildPutDownCardsOfOne(index, handLen):
    return [1 if i == index else 0 for i in range(handLen)]

# Initializes two lists of 13 zeros, modeling player empty hands.
def initEmptyDecks():
    return [[0]*13, [0]*13]

def addLists(lists):
    res = [0]*len(lists[0])
    for l in lists:
        for i, x in enumerate(l):
            res[i] += x
    return res


def getBeliefOfOpponentCards(opponentClaims, currentCards, putDownCards):
    deck = [4]*13
    substractStacks(deck, opponentClaims)
    substractStacks(deck, currentCards)
    substractStacks(deck, putDownCards)
    return deck

def currentPlayerBluffed(claim, handPlayed):
    standardizedClaim = [claim[1] if claim[0] == i else 0 for i in range(13)]
    return standardizedClaim != handPlayed


def outputPickle(l, filename):
    with open(filename, 'wb') as f:
        pickle.dump(l, f)


def loadPickle(filename):
    with open(filename, 'rb') as f:
        theta = pickle.load(f)
        return theta
#[([x1, x2, ...,xn], 0), ]
def formatTrainingData(training_data):
  x = np.zeros((len(training_data), len(training_data[0][0])))
  y = np.zeros(len(training_data))
  for i in range(len(training_data)):
    x[i] = training_data[i][0]
    y[i] = training_data[i][1]
  return x, y
'''
currentCards = [1, 3, 2, 4, 0, 0, 4, 2, 1, 1, 0, 2, 2]
cardsPutDown = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lastRank = 9
numOpponentCards = 3
print(getState(currentCards, cardsPutDown, lastRank, numOpponentCards))
'''


'''
  def getPossibleActions(self, currentCards, currentRank):
      truthful = False
      possibleActions = []
      for dx in [-1,0,1]:
        newRank = (currentRank + dx) % len(currentCards)
        if currentCards[newRank] > 0:
          truthful = True
          cardsPutDown = util.buildPutDownCardsOfOne(newRank, len(currentCards))
          claim = (newRank, 1)
          possibleActions.append((cardsPutDown, claim))
      if not truthful:
          newRank = util.drawFavoringFarCards(currentCards, lastRank)
          cardsPutDown = util.buildPutDownCardsOfOne(newRank, len(currentCards))
          claim = (newRank, 1)
          possibleActions.append((cardsPutDown, claim))
      return possibleActions
'''
