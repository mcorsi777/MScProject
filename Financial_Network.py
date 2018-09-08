"""
Year End Project
Program:                Data Science
@author:                Marco Corsi
@Description: Define the class FinancialNetwork and the utility functions to calculate the Debt Rank
"""

# File Structure: 
#       1. Libraries and parameters
#       2. Definition of the class FinancialNetwork and its methods
#       3. Utility funciotns




import pandas as pd
import numpy as np
import networkx as nx



##  Class implementing the FinancialNetwork object as a child of the Dirct Graph class from the
#   library networkx. In addition to all the functionalities of DirecGraph, the financialNetwork class
#   contains the following methods:
#   - debtRankCentrality: Calculate the centrality measure for each node using the debtRank algorithm
#   - mainStats: Generate a summary of all the main statistics relevant for the graph
#   - saveNetwork: Save the graph into a .gexf file
#  
class FinancialNetwork(nx.DiGraph):
 
    ## Construct a Direct Graph based on the following parameters:
    #  @param weights: dataFrame with columns and rowns indexed by node names. Position (i,j)
    #                  contains the impact of node j over node i
    #  @param staticAttributes: dictionary where the keyas are node identifiers and the values are list containing 
    #                           the values for a list of static attributes
    #  @param attributeNames: list containing the names (as strng) of the various attributes from the 
    #                         dictionary staticAttributes
    #
    def __init__(self, weights = None, staticAttributes = None, attributeNames = None, G = None):
        
        super().__init__(self)
        
        if G != None:
            
            nodes = G.nodes(data=True)
            edges = G.edges(data=True)
            self.add_nodes_from(nodes)
            self.add_edges_from(edges)
        
        else:
        
            #  Reorganize the dataframe weights (where the position (i,j) contains the weight of the edge from j to i)
            #  into a list tuples where each tuple contains origin node, destination node and weight
            
            forGraph = []            
            for c in weights.columns :
                for cc in weights.index :
                    block = []
                    block.append(c)
                    block.append(cc)
                    block.append(weights.loc[cc,c])
                    forGraph.append(block)
            
            self.add_weighted_edges_from(forGraph) # add all the weighted node to the graph
    
            # add all the attributes
            
            count = 0
            for n in attributeNames:
                attributes = {s : staticAttributes[s][count] for s in self}
                nx.set_node_attributes(self, attributes, n)
                count = count + 1
            
            
    
    ## Save the network into a .gefx file
    #  @param path: string with path and name of the destination file
    #
    def saveNetwork(self, path):                    
       
       nx.write_gexf(self, path + ".gexf")
    
    
    ## Generate a series of basic stats for the network and store them into the 
    #  disctionary attribute _mainStats
    #  
    def mainStats(self): 
        
        mirrorG = self.copy()
        edges = mirrorG.edges(data=True)
        edgesNull = []
        for e in edges:
            if e[2]['weight'] == 0:
                edgesNull.append(e)
        mirrorG.remove_edges_from(edgesNull)
                
            
        
        
        mainStats = {}    # dictionary with all the major stats for the graph
        
        nbNodes, nbEdges = mirrorG.order(), mirrorG.size()
        avg_deg = float(nbEdges) / nbNodes
        
        # nb os strongly and weakly connected nodes
        scc = nx.number_strongly_connected_components(mirrorG)
        wcc = nx.number_weakly_connected_components(mirrorG)
        
        inDegree = mirrorG.in_degree()
        outDegree = mirrorG.out_degree()
        avgInDegree = np.mean(list(zip(*inDegree))[1])
        avgOutnDegree = np.mean(list(zip(*outDegree))[1])
        
        density = nx.density(mirrorG)
        
        mainStats['nbNodes'] = np.round(nbNodes,0)
        mainStats['nbEdges'] = np.round(nbEdges,0)
        mainStats['avg_deg'] = np.round(avg_deg,2)
        mainStats['stronglyConnectedComponents'] = np.round(scc,0)
        mainStats['weaklyConnectedComponents'] = np.round(wcc,0)
        mainStats['avgInDegree'] = np.round(avgInDegree,2)
        mainStats['avgOutnDegree'] = np.round(avgOutnDegree,2)
        mainStats['density'] = np.round(density,2)
        
        return mainStats
    
    ## Calculate for each node a centrality measure using the DebtRank algorithm and 
    #  store the results into a new node attribute called debtRankCentrality
    #  @param: relevance is a dictionnary with absolute economic relevance of each node (could be Makt cap or other)
    #
    def debtRankCentrality(self, relevance):    
        
        h = 1
        R = {}
        
        for k in self.nodes():
            SD = [k] #list of distressed nodes
            h = 1
            R[k] = debtRank(self, SD, h, relevance)[0]
        
        nx.set_node_attributes(self, R, 'debtRankCentrality')


    ## Calculate for each node the position on a 2-dimensional chart using the 
    #  Fruchterman-Reingold force-directed algorithm and store the results into 2 new node attributes called x and y
    #  @param: _scale, _threshold, _k, _iterations are all the parameters required by the 
    #           nx.spring_layout function (see relevant documentation)
    #
    def generateLayout(self, _scale, _threshold, _k, _iterations):    
        
        layout = nx.spring_layout(self, scale  = _scale, threshold = _threshold, k = _k, iterations = _iterations)         
        
        x = {}
        y = {}
        
        for k in layout.keys():
            x[k] = float(layout[k][0])
            y[k] = float(layout[k][1])
            
        nx.set_node_attributes(self, x, 'x')
        nx.set_node_attributes(self, y, 'y')





# Utility Functions #######################################################################




## Calculate the debt rank measure for a set of nodes in a graph, associated with 
#  a specific level of distress. if the set contains only one node then the measure 
#  is its debt rank; if the set contains multiple nodes then
#  the measure is the cumulative debt rank for the set.
#  @param graph: the graph
#  @param SD: set of nodes for which the measure must be calculated
#  @param h: scalar (double) in [0,1] with the initial level of distress (equal for all nodes). 1 is default
#  @param maxIter: maximum number of iterations
#  @param relevance: dictionnary with absolute economic relevance of each node (could be Makt cap or other)
#  
def debtRank(graph, SD, h, relevance, maxIter = 100):

    #  Construct the dictionnar S0 with the initial conditions. key are the nodes and values 
    #  are the pairs [s, h] where s can be 'D' (distressed), 'I' (inactive), 'U' (undistressed)
    #  and h is the level of distress.
    
    
    if relevance == {}:
        for i in graph.nodes():
            relevance[i] = 1

    cumRelevance = sum([relevance[i] for i in relevance])
    

    S0 = {} 
    for n in graph.nodes():
        if n in SD:
            S0[n] = ['D', h]
        else:
            S0[n] = ['U', 0]
    
    S1 = S0.copy() 
    nbIter = 0
    R0 = sum(S0[k][1] * relevance[k] / cumRelevance  for k in S0.keys()) # cumulative initial distress
    nbDistressed = len(SD)

    
    while nbDistressed != 0 and nbIter < maxIter:
        nbIter = nbIter + 1
        
        # Update the distress function
        for j in graph.nodes():
            h = S0[j][1]
            for k in SD:
                if (k,j) in graph.edges():
                    h = h + S0[k][1] * graph[k][j]['weight']
            h = min(1, h)
            S1[j][1] = h
        
        # Update the state
        for i in graph.nodes():
            if S0[i][0] == 'D' or S0[i][0] == 'I':
                S1[i][0] = 'I'
            else:
                if S1[i][1] > 0 and S0[i][0] != 'I':
                    S1[i][0] = 'D'
                else:
                    S1[i][0] = 'U'
        
        SD = [s for s in S1.keys() if S1[s][0] == 'D']
        nbDistressed = len(SD)
    
    R = sum(S1[k][1] * relevance[k] / cumRelevance  for k in S1.keys()) - R0

    
    return R, S1