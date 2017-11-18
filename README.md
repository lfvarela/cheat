# cheat
Modeling the game 'Cheat' with AI

The Protagonist's offensive decision process with Logistic Regression:
1) We will have a ContenderBelief class, which is a class that models our belief of the Contender.
2) From a currentState, the Protagonist will produce a list of all the possibleActions it can take from that state. Where every action is a (claim, cardsPlayed) tuple. And claim is a (rank, numCards) tuple.
3) The Protagonist will pass those possibleActions to the Game, and the Game will produce a mediumState for each of those actions.
4) For each mediumState, the Game will ask the ContenderBelief for all (action, probabilityOfAction) tuples that the ContenderBelief will take from the medState, and the ContenderBelief will return this.
5) The Game will process all the (action, probabilityOfAction) tuples into the corresponding state that results from each action, and create a list of (nextState, probOfNextState) tuples. The Game will pass said list to the Protagonist.
6) The Protagonist will receive the list of (nextState, probOfNextState) tuples, and from these calculate the expected value of the action the Protagonist. The score for each state is a dot product between the learned weights from logistic regression (theta) and the state features.
7) Finally, the Protagonist will take the action that maximizes the expected value of taking that action, which we described in steps 3-6.
