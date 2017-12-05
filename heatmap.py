import plotly.plotly as py
import plotly.graph_objs as go

z = [[0.4944, 0.2743, 0.1544, 0.1454, 0.8490],
    [0.7250, 0.5033, 0.1726, 0.1721, 0.8267],
    [0.8577, 0.8209, 0.5057, 0.4861, 0.5038],
    [0.8570, 0.8263, 0.5073, 0.5051, 0.4703],
    [0.8483, 0.8324, 0.5078, 0.5192, 0.4986]]
#text = [[str(z_val) for z_val in z_l] for z_l in z]
trace = go.Heatmap(z=z,zmin=0, zmax=1,
                    colorscale=[[0, 'rgb(255,0,0)'], [.5, 'rgb(255,255,0)'],[1, 'rgb(0,255,0)']])
data=[trace]
py.plot(data, filename='basic-heatmap')
