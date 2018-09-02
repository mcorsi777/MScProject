#
# Set of functions to convert data from csv and json files into sqllite format
#

import sqlite3
import pandas as pd




## Create a table with all nodes static attributes
#  node_id is the yahoo company ticker
#  name    is the comapny name
#  currency is the currency denomination of the stock price
#  benchmark is the relevant market benchmark, identified by the yahoo ticker
#  @param DB is a string with the name and path of the database
#
def createNodesAttributes(DB):
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
    cursor.execute('''
    		CREATE TABLE nodesStatic (
    		node_id     varchar    PRIMARY KEY,
    		name        text        NOT NULL,
    		currency    varchar(3)  NOT NULL,
            benchmark   varchar
    			);
    		''')
    db.commit()
    db.close()



## Populate the Nodes table using data from the nodesAttributes dictionary
#  @param DB is a string with the name and path of the database
#  @nodesAttributes dictionary - keys are node identifiers and values are list of attributes 
#
def populateNodes(DB, nodesAttributes):
    db = sqlite3.connect(DB)  
    cursor = db.cursor()
    
    for k in nodesAttributes.keys():
        name = k
        node_id = nodesAttributes[k][1]
        currency = nodesAttributes[k][2]
        benchmark = nodesAttributes[k][3]
        cursor.execute("""INSERT INTO nodesStatic VALUES (?,?,?,?)""", 
                       (node_id, name, currency, benchmark))
        
    db.commit()
    db.close()



## Create a table with all nodes dynamic weights
#  node_id is the yahoo company ticker
#  year    is the year to which the weight refer
#  all other columns are identified by the yahoo ticker for the companies and 
#  contain the percentage of that company owned by the node_id
#  @param DB is a string with the name and path of the database
#  @nodesAttributes dictionary - keys are node identifiers and values are list of attributes (one attribute must be current mkt_cap)
#
def createNodesWeights(DB, nodesAttributes):
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
    cursor.execute('''
    		CREATE TABLE nodesWeights (
    		node_id     varchar NOT NULL REFERENCES nodes(node_id),  --foreign key  
    		date        YEAR         NOT NULL,
         PRIMARY KEY (node_id, date) 
    			);
    		''')
    
    for k in nodesAttributes.keys():   
        name = "OWNED_OF_" + nodesAttributes[k][1].replace(".", "_").replace("-", "_")
        cursor.execute('''ALTER TABLE nodesWeights ADD COLUMN ''' + name + ''' varchar''')
    
    db.commit()
    db.close()



## Populate the NodesWeights table using data from the Network dataframe
#  @param year is a string with the reference year for the weights
#  @param DB is a string with the name and path of the database
#  @param nodesAttributes dictionary - keys are node identifiers and values are list of attributes (one attribute must be current mkt_cap)
#  @param network: dataFrame - rown and columns labelled based on nodes id - position
#
def populateNodesWeights(DB, year, nodesAttributes, network):
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
   
    
#    network  = pd.read_csv(PATH + "network_" + year + ".csv")
#    network.index = network[network.columns[0]]
#    del network[network.columns[0]]


    
    allColumns = {}
    
    for k in nodesAttributes.keys():  
        name = "OWNED_OF_" + nodesAttributes[k][1].replace(".", "_").replace("-", "_")
        allColumns[name] = k

    for k in nodesAttributes.keys():
        date = year
        node_id = nodesAttributes[k][1]
        cursor.execute("""INSERT INTO nodesWeights (node_id, date ) VALUES (?,?) """, 
                       (node_id, date))
        
        for c in allColumns.keys():
            value = network.loc[k, allColumns[c]]
            cursor.execute("UPDATE nodesWeights SET " + c + "=? WHERE node_id=? AND date=?",
                           (value, node_id, date))
        
    db.commit()
    db.close()

## Create a table with all nodes historical prices and mkt cap
#  node_id is the yahoo company ticker
#  date    is the day
#  price   is the closing price in local currency
#  market_cap is the market cap in USD
#  nb_shares is the number of outstanding shares
#  @param DB is a string with the name and path of the database
#
def createPriceHistoryUSD(DB):
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
    cursor.execute('''
    		CREATE TABLE priceHistory (
    		node_id     varchar NOT NULL REFERENCES nodes(node_id),  --foreign key  
    		date        DATE        NOT NULL,
         price       DOUBLE,
         market_cap  DOUBLE,
         nb_shares   DOUBLE,
         PRIMARY KEY (node_id, date) 
    			);
    		''')
    
    db.commit()
    db.close()



## Populate the PriceHistory table using data from the allPrices dataframe
#  @param DB is a string with the name and path of the database
#  @param nodesAttributes dictionary - keys are node identifiers and values are list of attributes (one attribute must be current mkt_cap)
#  @param allPrices - dataframe - index are days, columns labelled using nodes_id - values are closing prices
#
def populatePriceHistoryUSD(DB, nodesAttributes, allPrices):
    
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
    day = '2018-06-12' #last day of available information
    allPrices1 = allPrices.drop(day)

    for k in nodesAttributes.keys():
        
        node_id = nodesAttributes[k][1]
        mktCap = nodesAttributes[k][0]
        nbShares = mktCap/allPrices.loc[day, node_id]
        price = allPrices.loc[day, node_id]
        cursor.execute("""INSERT INTO priceHistory (node_id, date, market_cap, nb_shares, price) VALUES (?,?,?,?,?) """, 
                       (node_id, day,mktCap,nbShares, price))
        
        
        for c in allPrices1.index:
            value = allPrices1.loc[c, node_id]
            mktCap = nbShares * value
            cursor.execute("""INSERT INTO priceHistory (node_id, date, market_cap, nb_shares, price) VALUES (?,?,?,?,?) """, 
                       (node_id, c, mktCap,nbShares, value))
        
    db.commit()
    db.close()




## Create a table with all nodes historical prices and mkt cap
#  node_id is the yahoo company ticker
#  date    is the day
#  price   is the closing price in local currency
#  @param DB is a string with the name and path of the database
#
def createPriceHistory(DB):
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
    cursor.execute('''
    		CREATE TABLE priceHistory (
    		node_id     varchar NOT NULL REFERENCES nodes(node_id),  --foreign key  
    		date        DATE        NOT NULL,
         price       DOUBLE,
         PRIMARY KEY (node_id, date) 
    			);
    		''')
    
    db.commit()
    db.close()



## Populate the PriceHistory table using data from the allPrices dataframe
#  @param DB is a string with the name and path of the database
#  @param nodesAttributes dictionary - keys are node identifiers and values are list of attributes 
#  @param allPrices - dataframe - index are days, columns labelled using nodes_id - values are closing prices
#
def populatePriceHistory(DB, nodesAttributes, allPrices):
    
    db = sqlite3.connect(DB)  
    cursor = db.cursor() 
    #day = '2018-08-10' #last day of available information
    #allPrices1 = allPrices.drop(day)

    for k in nodesAttributes.keys():
        
        node_id = nodesAttributes[k][1]

        for c in allPrices.index:
            price = allPrices.loc[c, node_id]
            cursor.execute("""INSERT INTO priceHistory (node_id, date, price) VALUES (?,?,?) """, 
                       (node_id, c, price))
        
    db.commit()
    db.close()

## Get data from the nodesAttribute DB and store them into a dictionary
#  @param DB is a string with the name and path of the database
#
def getNodesAttributes(DB):
    
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute('''SELECT node_id, name, currency, benchmark FROM nodesStatic''')
    all_rows = cursor.fetchall()
    nodesAttributes = {}
    
    for r in all_rows:
        nodesAttributes[r[0]] = list(r[1:])
        
    db.close()
    
    return nodesAttributes

## Get data from the nodesWeights DB and store them into a dataframe where columns and rows 
#  are identified via the yahoo ticker of the node. The position (i,j) contains the impact of 
#  of j over i.
#  @param DB is a string with the name and path of the database
#  @param year is a string with the reference year for the weights
#
def getNodesWeights(DB, year):
    
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM nodesWeights WHERE date = ? ", (year,))
    all_rows = cursor.fetchall()
    allNames = {}
    for r in all_rows:
        adjusted = "OWNED_OF_" + r[0].replace(".", "_").replace("-", "_")
        allNames[adjusted] = r[0]

    
    
    weights = pd.DataFrame(index = allNames.values(), columns = allNames.keys())
    
    for n in allNames.values():
        for m in allNames.keys():
            cursor.execute("SELECT " + m + " FROM nodesWeights WHERE date = ? AND node_id = ?", 
                           (year,n))
            value = cursor.fetchone()
            weights.loc[n,m] = float(value[0])
    
    weights = weights.rename(columns=allNames)
    db.close()
    
    return weights


