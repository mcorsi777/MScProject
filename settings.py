# path where the database tables are stored
PATH = '/Users/Marco/Documents/MSc/Project/Code/'

# names for the differemt databases (this needs to be modified only if you are creating the DBs)
DB = PATH + 'nodesStatic_db'   # static information for each node
DB1 = PATH + 'nodesWeights_db' # weights of the network (historical)
DB2 = PATH + 'priceHistory_db' # historical prices and mkt_cap of the nodes
DB3 = PATH + 'nodesWeightsCorrel_db' # historical prices and mkt_cap of the nodes 
DB4 = PATH + 'priceHistoryUSD_db' # historical USD prices and USD mkt_cap of the nodes 

# para,meter used for the debt rank algorithm (in the final version this functionality is not used as it proved to be unstable)
ALPHA = 0.2

# size parameters for the different areas of the graphical interface
DESCRIPTION_W = 800 #description area
STATS_W = 500 #stats table
PLOT_W = 800 #figure
PLOT_H = 500 #figure

