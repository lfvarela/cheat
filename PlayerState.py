import util

class PlayerState:
  def __init__(self, currentCards, putDownCards, opponentClaim, numOpponentCards):
    if opponentClaim is None:
        self.radialVector = currentCards
    else:
        self.radialVector = util.getRadialVector(currentCards, opponentClaim[0])
    self.putDownCards = putDownCards
    self.opponentClaim = opponentClaim
    self.numOpponentCards = numOpponentCards
    self.currentCards = currentCards

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