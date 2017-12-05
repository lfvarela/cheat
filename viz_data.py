
import util
import matplotlib.pyplot as plt

# Each data point: (num data points, percentage of wins, theta)
data = util.loadPickle('./graph_data.pkl')
plt.plot([x[0] for x in data], [x[1] for x in data])
plt.show()

training_data = util.loadPickle('./dumb_train.pkl')
print len(training_data)
