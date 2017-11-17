import numpy as np

'''
A bunch of helper functions
'''

#Adds source to target without changing source.
#Note this method is unlike moveStacks, which changes source
def addStacks(target, source):
  for i in range(len(target)):
    target[i] += source[i]

#Adds cards from source to target. Changes source by decrementing
#source by cards.
def moveStacks(target, source, cards):
  for i in range(len(target)):
    target[i] += cards[i]
    source[i] -= cards[i]

#Moves all of source over to target. Note that source == [0]*13 after.
def transferStacks(target, source):
  moveStacks(target, source, source)

#Takes a claim and returns its equivalent "hand" representation.
def claim2Cards(claim):
  return [claim[1] if i == claim[0] else 0 for i in range(13)]

def uniformDraw(probs):
  s = float(sum(probs))
  return np.random.choice(len(probs), 1, p=[x/s for x in probs])[0]

#Returns index of a random card drawn from currentCards
def drawFavoringFarCards(currentCards, lastRank):
  probs = [0] * 13
  for i, x in enumerate(currentCards):
    if x > 0:
      #gets smallest distance from lastRank to i (including wrap around)
      probs[i] = min(abs(lastRank - i), 13 - lastRank + i)
  return uniformDraw(probs)

def drawFavoringCloseCards(currentCards):
  print(currentCards) #currentCards has some negative elements
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

def logistic_regression(self, states, alpha=0.1):
	for j in range(len(self.theta)):
    self.theta[j] += alpha*(self.result - h(state))*state[j]

def h(self, states):
  prod = sum([self.theta[i]*states[i] for i in range(len(self.theta))])
  return sigmoid(prod)

def sigmoid(z):
  return 1.0/float(1 + exp(-z))
