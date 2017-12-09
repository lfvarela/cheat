
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
def train_data(train_filename, num_iters, player1, player2):
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

# Gathers data on num_iters * num_games_per_iter between player1 and player2, and stores the last 20 states for each game, labeled 0 or 1
def gather_train(train_filename, player1, player2):
    num_iters = 10
    num_games_per_iter = 500
    print 'gathering training data on ' + str(num_iters*num_games_per_iter) + ' games.'
    print
    for i in range(num_iters):
        train_data(train_filename, num_games_per_iter, player1, player2)


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

# Trains our thetas for LR agents on the train data given
def train_lr(train_filename):
    training_data = util.loadPickle(train_filename)
    print len(training_data)
    theta = [0]*len(training_data[0][0])
    util.logistic_regression_on_data(theta, training_data)
    print 'theta = ' + str(theta)
    return theta


def test_lr(theta, opponent):
    num_games = 1000
    num_wins = 0.0
    i = 1
    while i < num_games:
        game = Game(agents.Protagonist(theta=theta), opponent)
        winner = game.run()
        if winner == 0.5:
            print 'draw'
            print i
            continue # Draw
        if winner == 0:
            num_wins += 1
        i += 1
        print i
        print 'current win percentage: ' + str(num_wins/i)
    print 'final  win percentage: ' + str(num_wins/float(num_games))


# Args: filename for train data, opponent were gonna train data on.
def train_test_round_for_lr(train_filename, opponent):
    gather_train(train_filename, agents.DumbestContender())
    final_theta = create_graph_data(train_filename, agents.DumbestContender())
    print 'final theta: ' + str(final_theta)
    test_lr_vs_dumb(final_theta, agents.DumbestContender())

def play_one_game(player1, player2, verbose=True):
    game = Game(player1, player2, verbose=verbose)
    winner = game.run()
    print 'winner is: Player' + str(winner)

#good theta: [0.033518215182340716, -0.3150298815540288, -0.3374114617960079, -0.3398257534568357, -0.31420142340764967, -0.22612517765889042, -0.2517273508130277, -0.22031836693070267, -0.28037482834398614, -0.31195773031254753, -0.32635884676914323, -0.32884665971360894, -0.28319598960749615, -0.33570416012292226, 0.4377559655758766]

if __name__=='__main__':
  #train_test_round_for_lr('./dumb_train_4.pkl', agents.DumbestContender())
  #theta = train_lr('./shedding_train.pkl')
  #theta = [-0.019594482459902463, -0.12201879994940613, -0.13181200639505908, -0.16198099140073657, -0.13261209778286293, -0.1117454130939553, -0.11828411709453032, -0.058170875752038755, -0.11217743355011119, -0.12511182597862475, -0.10318958384146198, -0.13972399216905215, -0.1589608398833307, -0.10556594801791527, 0.10706923408959328, 0.13438029095776377]
  #test_lr(theta, agents.SheddingContender())
  #test_lr([-0.019594482459902463, -0.12201879994940613, -0.13181200639505908, -0.16198099140073657, -0.13261209778286293, -0.1117454130939553, -0.11828411709453032, -0.058170875752038755, -0.11217743355011119, -0.12511182597862475, -0.10318958384146198, -0.13972399216905215, -0.1589608398833307, -0.10556594801791527, 0.10706923408959328, 0.13438029095776377], agents.DirectionalStartDeterministicAccusation())
  theta = [-0.019594482459902463, -0.12201879994940613, -0.13181200639505908, -0.16198099140073657, -0.13261209778286293, -0.1117454130939553, -0.11828411709453032, -0.058170875752038755, -0.11217743355011119, -0.12511182597862475, -0.10318958384146198, -0.13972399216905215, -0.1589608398833307, -0.10556594801791527, 0.10706923408959328, 0.13438029095776377]
  gather_train('./lr_train1.pkl', agents.Protagonist(theta=theta), agents.Protagonist(theta=theta))

'''
History: (after poster session)
All training sets are based off of 5000 games, and 20 data points from each, so 200000 data points total.
'''

'''
Adding the new feautures for the number of cards we have improved our percentage wins to 75 percent against a dumb opponent. (from 50%)
Feautures:
    result.append(1)
    result.extend(self.radialVector)
    result.append(self.numOpponentCards)
    result.append(sum(self.radialVector))

Theta: Learned from 5000 games of DumbestContender vs DumbestContender
theta = [0.030033763665895923, -0.043504765531045785, -0.06373092835048186, -0.05467377661574285, -0.06521888611984926, -0.02142537397035946, -0.01905773113037618, -0.012179246903426437, -0.02319801327482905, -0.04140204704432215, -0.08858694997282894, -0.10350391538747583, -0.11151395185339537, -0.07022559696044653, 0.49029695442445576, -0.2916971059498149]
Results: win 76 percent of games against DumbestContender() after 1000 games.

Using the same theta, but now including actions where we shed more than one card, we now win 95 percent of the time against the Dumbest Contender.
Using this same thetas, we beat the SheddingContender 81 percent of the times after 1000 games.
Using this same thetas, we they LR and SheddingContenderWithDeterministicBluffAccusation draw most of the times, interesting!, and when they don't, LR wins about half of the times.
'''

'''
Now, we gathered shedding_train.pkl (shedding vs shedding). We trained on this data and got the following
theta = [-0.019594482459902463, -0.12201879994940613, -0.13181200639505908, -0.16198099140073657, -0.13261209778286293, -0.1117454130939553, -0.11828411709453032, -0.058170875752038755, -0.11217743355011119, -0.12511182597862475, -0.10318958384146198, -0.13972399216905215, -0.1589608398833307, -0.10556594801791527, 0.10706923408959328, 0.13438029095776377]
Using these thetas, we beat the SheddingContender 78 percent of the times after 1000 games.
Using these thetas, we beat the SheddingContenderWithDeterministicBluffAccusation 76.1 percent of the times after 1000 games.
Using these thetas, we beat the DirectionalBluffDeterministicBluffAccusation 75.5 percent of the times after 1000 games.
Using these thetas, we beat the DirectionalStartDeterministicAccusation 73.7 percent of the times after 1000 games.

Now, we gather 200000 data points from games between our LR protagonist using these thetas. We store this in lr_train1.pkl.
'''

'''

'''
