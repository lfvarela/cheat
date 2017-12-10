import util

class PlayerState:
  def __init__(self, currentCards, putDownCards, lastClaim, numOpponentCards, opponentClaims, myClaims=[], numOpponentBluffs=0, numOpponentNonBluffs=0):
    if lastClaim is None:
        self.radialVector = currentCards
    else:
        self.radialVector = util.getRadialVector(currentCards, lastClaim[0])
    self.putDownCards = putDownCards
    self.lastClaim = lastClaim
    self.numOpponentCards = numOpponentCards
    self.currentCards = currentCards
    self.opponentClaims = opponentClaims
    self.myClaims = myClaims
    self.numOpponentBluffs = numOpponentBluffs
    self.numOpponentNonBluffs = numOpponentNonBluffs

  def featurize(self):
    result = []
    result.append(1)
    result.extend(self.radialVector)
    result.append(self.numOpponentCards)
    result.append(sum(self.radialVector))
    return result

  def getNumFeatures(self):
    return len(self.featurize())
