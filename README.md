

In order to run the final system execute the following oprations:

1. Ensure the Bokeh library is installed (see: https://bokeh.pydata.org/en/latest/docs/installation.html)
2. MAKE CHROME YOUR DEFAULT BROWSER
3. OPEN PROMPT AND TAPE: bokeh serve --show PATH/GUI.py
where PATH is the location where you have stored locally all the project





# IMPORTANT: 

This project require the usage of the most recent version of the library networkx (version 2.1). 
Update older version by using: $ pip install --upgrade networkx









# DATA




The project is based on a set of 30 financial institutions that in the following will be called nodes (of the network). refer to the project documentation for more details.


allData_db: SQLite database containing the following tables

nodesStatic
 SQLITE table with static information for each node - primary key is the node yahoo ticker

nodesWeights
 SQLITE table with the weights of the network based on the equity ownership data or on the correlation data. There is a DATE feed indicating the year to which the data refer to (2018 or 2010)
 Primary key is  (Yahoo ticker, DATE, method), where method can be 'equityOwnership' or 'correlation'

priceHistory
 SQLITE table with the historical prices and mkt_cap of the nodes in local currency. Primary key is the pair (Yahoo ticker, DATE)

priceHistoryUSD
 SQLITE table with the historical prices and mkt_cap of the nodes in USD currency. Primary key is the pair (Yahoo ticker, DATE) 



G_2010.gexf
 Network based on the equity ownership data for 2010

G_2018.gexf
 Network based on the equity ownership data for 2018


G_2018Corr.gexf
 Network based on correlation data for 2018

# # IMPORTANT:
An additional database file called allDat_alpha_adj_db has been added in order to run the full test with this alternative version of the network. The three graph files will have to be generated separately using the instructions provided here.




# # PYTHON FILES




# settings.py
 File to set up the values for all the parameters to be used in the project

# DB_Utilities.py
 Set of functions to convert data from csv and json files into sqllite format

# DB_Generation.py
 Take raw information from csv files related to equity ownership, static caracteristics of the nodes and historical prices, clean and 
  consolidate the data and then store the final results into a series of SQL tables

# Financial_Network.py
 Define the class FinancialNetwork and the utility function to calculate the debt rank
 
# Graph_Builder.py 
Construct 3 different networks based on ownership data (in 2010 and 2018) and correlation data (for 2018).
 For each network the centrality debtRank measure is calculated on each node. The final networks and attributes are then stored in .gexf file.

# Description.html
 Text element for the GUI

# GUI.py
 Create a graphical interface to visualise a Financial Network and simulate the propagation of a distress over a given node across the structure.
 The three different networks previously created can be used for this exercise.







