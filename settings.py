"""
Use this file to set up the values for all the parameters to be used in the project
"""

from os.path import join

# path where the database tables are stored
PATH = '/Users/marcocorsi/MyPython/Project/'

# names for the differemt databases (this needs to be modified only if you are creating the DBs)
DB = join(PATH , 'allData_db')  # static information for each node


# para,meter used for the debt rank algorithm (in the final version this functionality is not used as it proved to be unstable)
ALPHA = 0.2

# size parameters for the different areas of the graphical interface
DESCRIPTION_W = 800 #description area
STATS_W = 500 #stats table
PLOT_W = 800 #figure
PLOT_H = 500 #figure
X_MIN = -2
X_MAX = 2
Y_MIN = -2
Y_MAX = 2

# Characteristcs of  plot elements
SIZE_CIRCLES = 10
COL_CIRCLES = 'navy'
COL_LINES = 'gray'

# Parameter for Layout definition in the class FinancialNetworks
SCALE = 1.5
LIMIT = 0.00001
IDEAL_DIST = 2.5
MAX_ITER = 100


# Parameters for the FUNCTION  backToOriginal() and update() in GUI
SIZE_CIRCLE_1 = 7 
SIZE_CIRCLE_2 = 20 

  
# Parameter for the FUNCTION distress_node in GUI
DISTRESS_SCALING = 1.3

##  Parameter for the Function get_edges_specs in GUI
EDGE_SCALING = 0.6

# PArameters for correlation network
PERIOD = 5 #(5 means returns over 5 business day)
WINDOW = 200 # data points for the calculation of the correll