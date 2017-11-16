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


