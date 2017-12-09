'''
Run this file to visualize data from graph_data.pkl, x[0] is x and x[1] is y for every data point x
'''


import util
import matplotlib.pyplot as plt

# Each data point: (num data points, percentage of wins, theta)
data = util.loadPickle('./graph_data.pkl')

plt.plot([x[0] for x in data], [x[1] for x in data])
plt.show()
