
import os.path
from game import Game
import util
import agents

def test_agents(protagonist, contender):
  winners = []
  for i in range(10000):
    print(i)
    game = Game(protagonist, contender)
    winners.append(game.run())
  print "protagonist won:" + str(float(len(winners) - sum(winners)) / len(winners))

'''
Play num_iter games of DumbestContender against DumbestContender and gather the last states
(received from each player) and label 
'''
def train_data_dumbs(num_iters):
    pickle_file = './dumb_train_2.pkl'
    training_data = []
    if os.path.exists(pickle_file):
      print 'loading pickle'
      training_data = util.loadPickle(pickle_file)
      print 'pickle loaded'

    for _ in range(num_iters):
      game = Game(agents.DumbestContender(), agents.DumbestContender())
      winner = game.run()
      num_data_points = len(game.players[0].endGame(winner == 0)) + len(game.players[1].endGame(winner == 1))
      training_data.extend(game.players[0].endGame(winner == 0))
      training_data.extend(game.players[1].endGame(winner == 1))

    print 'writing pickle'
    util.outputPickle(training_data, pickle_file)
    print 'pickle written'
    print 'train_data point: ' + str(len(training_data))
    return training_data


def gather_train_dumb_v_dumb():
    while True:
        train_data_dumbs(5000)

def create_graph_data():
    results = []
    training_data = util.loadPickle('./dumb_train_2.pkl')
    training_data = training_data[:500000]
    num_points = 10
    bucket_size = len(training_data)/num_points
    for i in range(num_points):
        print 'starting point ' + str(i)
        train_data_subset = training_data[:bucket_size*(i+1)]
        winners = []
        theta = [0]*len(training_data[0][0])
        util.logistic_regression_on_data(theta, train_data_subset)
        for _ in range(500):
          game = Game(agents.Protagonist(theta=theta), agents.DumbestContender())
          winner = game.run()
          winners.append(winner)

        print 'theta after training: ' + str(theta)
        print 'winning percentage: ' + str(float(len(winners) - sum(winners)) / len(winners))
        print
        results.append((len(train_data_subset), float(len(winners) - sum(winners)) / len(winners), theta))

    util.outputPickle(results, './graph_data.pkl')


      # theta = game.players[0].endGame(winner == 0)
      #print 'theta at end of game: ' + str(theta)

#print("player 0 won: {}".format( float(len(winners) - sum(winners)) / len(winners) ))
#print("player 1 won: {}".format( float(sum(winners)) / len(winners) ))

#test = [5, 7, 3, 0, 0, 0, 1, 2, 3, 10, 1, 1, 5]
#print(util.drawFavoringCloseCards(test))

if __name__=='__main__':
  #gather_train_dumb_v_dumb()
  create_graph_data()
  #test_agents(agents.DirectionalBluffDeterministicBluffAccusation(), agents.DumbestContender())
  #DirectionalStartDeterministicAccusation
  #DirectionalBluffDeterministicBluffAccusation
  #SheddingContenderWithDeterministicBluffAccusation
  #SheddingContender
  #DumbContender
