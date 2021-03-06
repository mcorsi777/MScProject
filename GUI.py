"""
Year End Project
Program:                Data Science
@author:                Marco Corsi
@Description: Create a graphical interface to visualise a Financial Network and simulate the propagation of a distress over a given node across the structure.
              The three different networks previously created can be used for this exercise.
    
"""

import numpy as np
from os.path import dirname, join
import pandas as pd
import networkx as nx

import settings
import Financial_Network as fnc

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, layout, column
from bokeh.models import ColumnDataSource, Button, Select, HoverTool
from bokeh.models.widgets import TextInput, Div
from bokeh.plotting import figure
from bokeh.models.widgets import PreText



# Include Description

desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=settings.DESCRIPTION_W )


# Create Input controls

textInput = TextInput(value="1", title="Stress Parameter:")
textOutput = TextInput(value=" ", title="Error Messages:")
distressButton = Button(label="Distress Node")
backToOriginalButton = Button(label="Back To Original")
dataSource = Select(title="Data", options=['G_2010', 'G_2018', 'G_2018Corr'], value= 'G_2018')
stats = PreText(text='', width=settings.STATS_W)

# Create Column Data Source that will be used by the plot

nodeSource = ColumnDataSource(data=dict(x=[], y=[], node_id = [], names = [], centrality = [], 
                                        inducedStress = [], sizeParameter = [], alphas = []))
lines_source = ColumnDataSource(data=dict(xs=[], ys=[], alphas=[], weights=[])) 


# Tooltips for hoover function

TOOLTIPS=[
    ('name', '@names'),
    ('id', '@node_id'),
    ('inducedStress', '@inducedStress'),
    ('centrality', '@centrality')
]


# Create plot elements

plot = figure(plot_height=settings.PLOT_H, plot_width=settings.PLOT_W, title="network",
              tools=['tap', 'reset', 'box_zoom'], 
              x_range=[settings.X_MIN, settings.X_MAX], y_range=[settings.Y_MIN, settings.Y_MAX])


r_circles = plot.circle('x', 'y', source=nodeSource, size=settings.SIZE_CIRCLES, color=settings.COL_CIRCLES, level='overlay', alpha='alphas', fill_alpha = 'alphas')

r_lines = plot.multi_line('xs', 'ys', line_width=1, alpha='alphas', color=settings.COL_LINES,
                          source=lines_source)

r_circles.glyph.size = 'sizeParameter'

plot.add_tools(HoverTool(tooltips=TOOLTIPS, renderers=[r_circles])) 


##  Get data from the source specified in the dataSource widget and fill all the columns of 
#   nodeSource and LineSource.
#
def update():
    source = dataSource.value
    G = nx.read_gexf(settings.PATH + source + '.gexf')
    G = fnc.FinancialNetwork(None, None, None, G)
    centrality = nx.get_node_attributes(G,'debtRankCentrality')  # dictionary with nodex centrality  
    names = nx.get_node_attributes(G,'name')
    x = nx.get_node_attributes(G,'x')
    y = nx.get_node_attributes(G,'y')
    nodes = list(zip(*sorted(x.items())))[0]
    nodes_xs  = list(zip(*sorted(x.items())))[1]
    nodes_ys  = list(zip(*sorted(y.items())))[1]
    nodesCentrality = list(zip(*sorted(centrality.items())))[1]
    nodesNames = list(zip(*sorted(names.items())))[1]
    nodeSource.data = dict(
        node_id = nodes,
        x=nodes_xs,
        y=nodes_ys,
        names = list(nodesNames),
        sizeParameter = [settings.SIZE_CIRCLE_1  + settings.SIZE_CIRCLE_2 * t / max(nodesCentrality) for t in nodesCentrality],
        centrality = [t  for t in nodesCentrality],
        inducedStress = len(centrality) * ['-'],
        alphas = len(centrality) * [1]       
        )
    graphStats = pd.DataFrame.from_dict(G.mainStats(), orient='index')
    graphStats = graphStats.rename(columns={0: 'Stats'})
    lines_source.data = get_edges_specs(G)
    stats.text = str(graphStats)

##  Associated to the backToOriginalButton widget. Reset the graph to its original state.
#
#
def backToOriginal():

    nodesCentrality = nodeSource.data['centrality']
    nodeSource.data['sizeParameter'] = [settings.SIZE_CIRCLE_1 + settings.SIZE_CIRCLE_2 * t / max(nodesCentrality) for t in nodesCentrality]
    nodeSource.data['inducedStress'] = len(nodesCentrality ) * ['-']
    nodeSource.data['alphas']  = len(nodesCentrality ) * [1]
    textOutput.value = ""
    
    


##  Associated to the distressButton widget. Apply the stress parameter specified in the widget
#   textInput to the selecet node and simulate its propagation across the network.
#
#   
def distress_node():

    try:
        
        # Get coordinates and name of the selected node and value of the stress parameter
        idx = nodeSource.selected['1d']['indices'][0]
        node = nodeSource.data['node_id'][idx]
        distressParameter = float(textInput.value)
        
        if distressParameter > 1 or distressParameter <= 0:
            raise ValueError
            
        source = dataSource.value  
        G = nx.read_gexf(settings.PATH + source + '.gexf')
        
        if source == "G_2018Corr":
            raise Warning(' do not apply debt rank to a correlation based network')
            
                               
        #Get mkt cap data as a relevance parameter for the debtRank function
        mktCap = nx.get_node_attributes(G,'mktCap')
        #print(mktCap)
        
        # Apply stress and simulate propagation
        R, affectedNodes = fnc.debtRank(G, {node}, distressParameter, mktCap)
        impact = {k: affectedNodes[k][1] for k in affectedNodes.keys()}
        # Update graph
        nodeSource.data['inducedStress'] = [impact[t] for t in sorted(impact.keys())]
        nodeSource.data['alphas'] = [min(1, settings.DISTRESS_SCALING * impact[t]) for t in sorted(impact.keys())]
        textOutput.value = ""
    
    except ValueError:
        
        textOutput.value = 'Stress parameter must be number >0 and <=1'
        
    except IndexError:
        
        textOutput.value = 'Select a node first'
        
    except Exception as error:
        
        textOutput.value = 'Problem with Data ' + str(error)
 
        
        

    

##  Create edges for the graphs and define the the intensity of their colour
#
#
def get_edges_specs(graph):
    d = dict(xs=[], ys=[], alphas=[], weights=[])
    weights = [d['weight'] for u, v, d in graph.edges(data=True)]
    max_weight = max(weights)
    calcAlpha = lambda h:  settings.EDGE_SCALING * (h / max_weight)
    x = nx.get_node_attributes(graph,'x')
    y = nx.get_node_attributes(graph,'y')

    for u, v, data in graph.edges(data=True):
        d['xs'].append([x[u], x[v]])
        d['ys'].append([y[u], y[v]])
        d['alphas'].append(calcAlpha(data['weight']))
        d['weights'].append(data['weight'])
    
    return d



# Create and populate layout

controls = [distressButton, backToOriginalButton, dataSource]
for control in controls:
    if control == backToOriginalButton:
        
        control.on_click(backToOriginal)
    if control == distressButton:
        
        control.on_click(distress_node)
    
    if control == dataSource:
        control.on_change('value', lambda attr, old, new: update())

        
sizingMode = 'fixed' 

inputs = row(widgetbox(distressButton, backToOriginalButton, textInput, textOutput, dataSource, stats))

l = layout([
    [desc],
    [plot, inputs]
], sizing_mode=sizingMode)


update()  # initial load of the data

curdoc().add_root(l)