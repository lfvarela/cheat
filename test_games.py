
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
def train_data_dumbs(train_filename, num_iters, player1, player2):
    pickle_file = train_filename
    training_data = []
    if os.path.exists(pickle_file):
      print 'loading pickle'
      training_data = util.loadPickle(pickle_file)
      print 'pickle loaded'

    for _ in range(num_iters):
      game = Game(player1, player2)
      winner = game.run()
      num_data_points = len(game.players[0].endGame(winner == 0)) + len(game.players[1].endGame(winner == 1))
      training_data.extend(game.players[0].endGame(winner == 0))
      training_data.extend(game.players[1].endGame(winner == 1))

    print 'writing pickle'
    util.outputPickle(training_data, pickle_file)
    print 'pickle written'
    print 'train_data point: ' + str(len(training_data))
    print
    return training_data


def gather_train(train_filename, player1, player2):
    num_iters = 10
    num_games_per_iter = 500
    print 'training on ' + str(num_iters*num_games_per_iter) + ' games.'
    print
    for i in range(num_iters):
        train_data_dumbs(train_filename, num_games_per_iter, player1, player2)


# Trains our Logistic Regression protagonist from labeled state -> game_result data points.
def create_graph_data(train_filename, opponent):
    results = []
    num_games = 250
    training_data = util.loadPickle(train_filename)
    training_data = training_data[:200000]
    num_points = 10
    bucket_size = len(training_data)/num_points
    for i in range(num_points):
        print 'starting point ' + str(i)
        train_data_subset = training_data[:bucket_size*(i+1)]
        winners = []
        theta = [0]*len(training_data[0][0])
        util.logistic_regression_on_data(theta, train_data_subset)
        for _ in range(num_games):
          game = Game(agents.Protagonist(theta=theta), opponent)
          winner = game.run()
          winners.append(winner)
          #theta = game.players[0].endGame(winner == 0)
        print 'theta after training: ' + str(theta)
        print 'winning percentage on ' + str(num_games) + ' games: ' + str(float(len(winners) - sum(winners)) / len(winners))
        print
        results.append((len(train_data_subset), float(len(winners) - sum(winners)) / len(winners), theta))

    util.outputPickle(results, './graph_data.pkl')
    return theta

def train_lr(train_filename, opponent):
    training_data = util.loadPickle(train_filename)
    print len(training_data)
    #theta = [0]*len(training_data[0][0])
    #util.logistic_regression_on_data(theta, training_data)
    theta = [0.030033763665895923, -0.043504765531045785, -0.06373092835048186, -0.05467377661574285, -0.06521888611984926, -0.02142537397035946, -0.01905773113037618, -0.012179246903426437, -0.02319801327482905, -0.04140204704432215, -0.08858694997282894, -0.10350391538747583, -0.11151395185339537, -0.07022559696044653, 0.49029695442445576, -0.2916971059498149]
    print theta
    test_lr_vs_dumb(theta, opponent)


def test_lr_vs_dumb(theta, opponent):
    num_games = 1000
    num_wins = 0.0
    for i in range(1, num_games + 1):
        game = Game(agents.Protagonist(theta=theta), opponent)
        winner = game.run()
        if winner == 0:
            num_wins += 1
        if i % 100 == 0:
            print 'current win percentage: ' + str(num_wins/i)
    print 'final  win percentage: ' + str(num_wins/float(num_games))


# Args: filename for train data, opponent were gonna train data on.
def train_test_round_for_lr(train_filename, opponent):
    gather_train(train_filename, agents.DumbestContender())
    final_theta = create_graph_data(train_filename, agents.DumbestContender())
    print 'final theta: ' + str(final_theta)
    test_lr_vs_dumb(final_theta, agents.DumbestContender())

#good theta: [0.033518215182340716, -0.3150298815540288, -0.3374114617960079, -0.3398257534568357, -0.31420142340764967, -0.22612517765889042, -0.2517273508130277, -0.22031836693070267, -0.28037482834398614, -0.31195773031254753, -0.32635884676914323, -0.32884665971360894, -0.28319598960749615, -0.33570416012292226, 0.4377559655758766]

if __name__=='__main__':
  #train_test_round_for_lr('./dumb_train_4.pkl', agents.DumbestContender())
  train_lr('./dumb_train_4.pkl', agents.DumbestContender())


# History:

'''
Adding the new feautures for the number of cards we have improved our percentage wins to 75 percent against a dumb opponent. (from 50%)
Feautures:
    result.append(1)
    result.extend(self.radialVector)
    result.append(self.numOpponentCards)
    result.append(sum(self.radialVector))

Theta: Learned from 5000 games of DumbestContender vs DumbestContender
Theta: [0.030033763665895923, -0.043504765531045785, -0.06373092835048186, -0.05467377661574285, -0.06521888611984926, -0.02142537397035946, -0.01905773113037618, -0.012179246903426437, -0.02319801327482905, -0.04140204704432215, -0.08858694997282894, -0.10350391538747583, -0.11151395185339537, -0.07022559696044653, 0.49029695442445576, -0.2916971059498149]
Results: win 76 percent of games against DumbestContender() after 1000 games.

Using the same theta, but now including actions where we shed more than one card, we now win 95 percent of the time against the Dumbest Contender.
'''
