import util

class PlayerState:
  def __init__(self, currentCards, putDownCards, lastRank, numOpponentCards, opponentClaims):
    if lastRank is None:
        self.radialVector = currentCards
    else:
        self.radialVector = util.getRadialVector(currentCards, lastRank)
    self.putDownCards = putDownCards
    self.lastRank = lastRank
    self.numOpponentCards = numOpponentCards
    self.currentCards = currentCards
    self.opponentClaims = opponentClaims

  '''
  def featurize(self):
    result = []
    result.append(1)
    result.extend(self.radialVector)
    result.extend(self.putDownCards)
    result.append(self.opponentClaim[0])
    result.append(self.numOpponentCards)
    return result
  '''

  def featurize(self):
    result = []
    result.append(1)
    result.extend(self.radialVector)
    result.append(self.numOpponentCards)
    return result

  def getNumFeatures(self):
    return len(self.featurize())
