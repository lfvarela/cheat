import plotly.plotly as py
import plotly.graph_objs as go

'''
z = [[0.4944, 0.2743, 0.1544, 0.1454, 0.1494],
    [0.7250, 0.5033, 0.1726, 0.1721, 0.1718],
    [0.8577, 0.8209, 0.5057, 0.4861, 0.4738],
    [0.8570, 0.8263, 0.5073, 0.5051, 0.4860],
    [0.8483, 0.8324, 0.5078, 0.5192, 0.4986]]
#text = [[str(z_val) for z_val in z_l] for z_l in z]
trace = go.Heatmap(z=z,zmin=0, zmax=1,
                    colorscale=[[0, 'rgb(255,0,0)'], [.5, 'rgb(255,255,0)'],[1, 'rgb(0,255,0)']])
data=[trace]
py.plot(data, filename='basic-heatmap')
'''

'''
Now, we gathered shedding_train.pkl (shedding vs shedding). We trained on this data and got the following
theta = [-0.019594482459902463, -0.12201879994940613, -0.13181200639505908, -0.16198099140073657, -0.13261209778286293, -0.1117454130939553, -0.11828411709453032, -0.058170875752038755, -0.11217743355011119, -0.12511182597862475, -0.10318958384146198, -0.13972399216905215, -0.1589608398833307, -0.10556594801791527, 0.10706923408959328, 0.13438029095776377]
Using these thetas, we beat the SheddingContender 95 percent of the times after 1000 games.
Using these thetas, we beat the SheddingContender 78 percent of the times after 1000 games.
Using these thetas, we beat the SheddingContenderWithDeterministicBluffAccusation 76.1 percent of the times after 1000 games.
Using these thetas, we beat the DirectionalBluffDeterministicBluffAccusation 75.5 percent of the times after 1000 games.
Using these thetas, we beat the DirectionalStartDeterministicAccusation 73.7 percent of the times after 1000 games.
'''

z = [[0.95, 0.78, 0.761, 0.755, 0.737]]
#text = [[str(z_val) for z_val in z_l] for z_l in z]
trace = go.Heatmap(z=z,zmin=0, zmax=1,
                    colorscale=[[0, 'rgb(255,0,0)'], [.5, 'rgb(255,255,0)'],[1, 'rgb(0,255,0)']])
data=[trace]
py.plot(data, filename='basic-heatmap')
