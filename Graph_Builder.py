"""
Year End Project
Program:                Data Science
@author:                Marco Corsi
@Description:  Construct 3 different graphs based on ownership data (in 2010 and 2018) and correlation data (for 2018).
For each graph the centrality debtRank measure is calculated on each node. The final graphs and attributes are then stored 
in .gexf files.
"""




import pandas as pd
import numpy as np
import networkx as nx
import sqlite3
import DB_Utilities as dbm
import settings
import Financial_Network as fn


def main():
    
    listAttributes = ['name', 'currency', 'benchmark']
    
    # get weighst and nodes attributes
    nodesAttributes = dbm.getNodesAttributes(settings.DB)
    weights2010 = dbm.getNodesWeights(settings.DB, '2010', 'equityOwnership')
    weights2018 = dbm.getNodesWeights(settings.DB, '2018', 'equityOwnership')
    weights2018Corr = dbm.getNodesWeights(settings.DB, '2018', 'correlation')
    
    G2010 = fn.FinancialNetwork(weights2010, nodesAttributes, listAttributes)
    G2018 = fn.FinancialNetwork(weights2018, nodesAttributes, listAttributes)
    G2018Corr = fn.FinancialNetwork(weights2018Corr, nodesAttributes, listAttributes)
    
    # Get market cap for each node as of the last available day (in USD)
    db = sqlite3.connect(settings.DB)
    cursor = db.cursor()
    cursor.execute("SELECT node_id, market_cap FROM priceHistoryUSD WHERE date = '2018-06-12' ")
    all_rows = cursor.fetchall()
    marketCaps2018 = {}
    for i in range(len(all_rows)):
        marketCaps2018[all_rows[i][0]] = float(all_rows[i][1])
    db.close()
    
    # Get market cap for each node as of the last available day (in USD)
    db = sqlite3.connect(settings.DB)
    cursor = db.cursor()
    cursor.execute("SELECT node_id, market_cap FROM priceHistoryUSD WHERE date = '2010-07-21' ")
    all_rows = cursor.fetchall()
    marketCaps2010 = {}
    for i in range(len(all_rows)):
        marketCaps2010[all_rows[i][0]] = float(all_rows[i][1])
    db.close()    
    
    # add mkt cap as attribute
    nx.set_node_attributes(G2010, marketCaps2010, 'mktCap')
    nx.set_node_attributes(G2018, marketCaps2018, 'mktCap')
    nx.set_node_attributes(G2018Corr, marketCaps2018, 'mktCap')
    
    # add layout (i.e. chart coordinates) as attribute
    G2010.generateLayout(settings.SCALE, settings.LIMIT, settings.IDEAL_DIST, settings.MAX_ITER)
    G2018.generateLayout(settings.SCALE, settings.LIMIT, settings.IDEAL_DIST, settings.MAX_ITER)
    G2018Corr.generateLayout(settings.SCALE, settings.LIMIT, settings.IDEAL_DIST, settings.MAX_ITER)
    
    # add debt rank centrality as attribute
    G2010.debtRankCentrality(marketCaps2010)
    G2018.debtRankCentrality(marketCaps2018)
    G2018Corr.debtRankCentrality(marketCaps2018)
    
    # save
    G2010.saveNetwork(settings.PATH + "G_2010")
    G2018.saveNetwork(settings.PATH + "G_2018")
    G2018Corr.saveNetwork(settings.PATH + "G_2018Corr")



main()





