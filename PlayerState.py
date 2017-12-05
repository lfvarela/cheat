import util

class PlayerState:
  def __init__(self, currentCards, putDownCards, lastClaim, numOpponentCards, opponentClaims):
    if lastClaim is None:
        self.radialVector = currentCards
    else:
        self.radialVector = util.getRadialVector(currentCards, lastClaim[0])
    self.putDownCards = putDownCards
    self.lastClaim = lastClaim
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
