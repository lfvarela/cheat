import plotly.plotly as py
import plotly.graph_objs as go

z = [[0.5, .4, .25, .1, 0],
    [0.6, 0.5, .4, .25, .1],
    [0.75, .6, 0.5, .4, .25],
    [.9, .75, .6, 0.5, .4],
    [1, .9, .75, .6, 0.5]]
text = [[str(z_val) for z_val in z_l] for z_l in z]
print text
trace = go.Heatmap(z=z,
                    colorscale=[[0, 'rgb(230,0,0)'], [.5, 'rgb(250,250,0)'],[1, 'rgb(0,230,0)']],
                    text=text)
data=[trace]
py.plot(data, filename='basic-heatmap')
