import util

class State:
  def __init__(self, currentCards, putDownCards, opponentClaim, numOpponentCards):
    self.radialVector = getRadialVector(currentCards, lastRank)
    self.putDownCards = putDownCards
    self.opponentClaim = opponentClaim
    self.numOpponentCards = numOpponentCards

  def featurize(self):
    result = []
    result.append(1)
    result.extend(self.radialVector)
    result.extend(self.putDownCards)
    result.append(self.opponentClaim[0])
    result.append(numOpponentCards)
    return result

  def getNumFeatures(self):
    return len(self.featurize())