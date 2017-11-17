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

def getState(currentCards, cardsPutDown, lastRank, numOpponentCards):
  distanceVector = [0]*len(currentCards)
  middleIndex = 6
  distanceVector[middleIndex] = currentCards[lastRank]
  for distance in range(1,7):
    distanceVector[middleIndex - distance] = currentCards[(lastRank-distance)%len(currentCards)]
    distanceVector[middleIndex + distance] = currentCards[(lastRank+distance)%len(currentCards)]
  distanceVector.extend(cardsPutDown)
  distanceVector.append(lastRank)
  distanceVector.append(numOpponentCards)
  distanceVecotr.append(1) #the last term is the bias term
  return distanceVector

currentCards = [1, 3, 2, 4, 0, 0, 4, 2, 1, 1, 0, 2, 2]
cardsPutDown = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lastRank = 9
numOpponentCards = 3
print(getState(currentCards, cardsPutDown, lastRank, numOpponentCards))
