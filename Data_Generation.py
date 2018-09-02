"""
Created on Tue Jul 24 09:46:00 2018

@author: marcocorsi
"""

import pandas as pd
import numpy as np
import DB_Construction as db
import settings

##  This function uses raw data (originated by Factset) in csv files representing the percentage of each financial company from a 
#   selected list owned by any other financial insitution in the world (including the other institution in the list)
#   The data are aggregated and consolidated in order to show for each company in the selected list the $amount owned by the other
#   companie in the list (methodology in the [1]). The final result is stored in a dataframe. Additionaly 
#   a dictionary with  information for each node (such as name, identifier, currency, current mkt_cap) is generated
# 

def createNodesAttributes():

    ##  Build Mapping Dictionary
    #   - Key: bank name from fcatsect database
    #   - Value[0]: Bank name from yahoo finance database
    #   - Value[1]: Bank Market Capitalisation in USd as of July-18
    #   - Value[2]: Bank ticker from yahoo finance
    #   - Value[3]: Bank currency denomination
    #   - value[4]: Bank market benchmark (yahoo ticker)
    
    mapNodes = {'Morgan Stanley':['Morgan Stanley', 88.392, 'MS', 'USD', '^GSPC'],
                 'Royal Bank of Canada': ['Royal Bank of Canada', 111.577, 'RY.TO', 'CAD', '^GSPTSE'],
                 'Royal Bank of Scotland': ['Royal Bank of Scotland', 39.37, 'RBS.L', 'GBP','^FTSE'],
                 'Santander': ['Santander', 87.30, 'SAN.MC', 'EUR', '^STOXX50E'],
                 'Société Generale': ['Societe Generale', 37.38, 'GLE.PA', 'EUR', '^STOXX50E'],
                 'Standard Chartered': ['Standard Chartered', 29.37, 'STAN.L', 'GBP','^FTSE'],
                 'State Street': ['State Street', 33.149, 'STT', 'USD', '^GSPC'],
                 'Sumitomo Mitsui FG': ['Sumitomo Mitsui', 55.756, '8316.T', 'JPY', '^N225'],
                 'UBS': ['UBS', 59.959, 'UBSG.VX', 'CHF', '^SSMI'],
                 'Unicredit Group': ['Unicredit', 38.12, 'UCG.MI', 'EUR', '^STOXX50E'],
                 'Bank of New York Mellon': ['BNYM', 53.182, 'BK', 'USD', '^GSPC'],
                 'Credit Suisse': ['Credit Suisse', 40.712, 'CSGN.VX', 'CHF', '^SSMI'],
                 'Groupe Crédit Agricole': ['Credit Agricole', 41.48, 'ACA.PA', 'EUR', '^STOXX50E'],
                 'ING': ['ING', 58.605, 'INGA.AS', 'EUR', '^STOXX50E'],
                 'Mizuho FG': ['Mizuho', 45.028, '8411.T', 'JPY', '^N225'],
                 'Nordea': ['Nordea', 40.43, 'NDA-SEK.ST', 'SEK', '^STOXX50E'],
                 'Bank of America': ['Bank of America', 315.978, 'BAC', 'USD', '^GSPC'],
                 'JP Morgan Chase': ['JPM', 396.195, 'JPM', 'USD', '^GSPC'],
                 'Citigroup': ['Citigroup', 182.227, 'C', 'USD', '^GSPC'],
                 'Deutsche Bank': ['Deutsche Bank', 26.448, 'DBK.DE', 'EUR', '^STOXX50E'],
                 'HSBC': ['HSBC', 189.389, 'HSBA.L', 'GBP','^FTSE'],
                 'Bank of China': ['Bank of China', 163.96, '3988.HK', 'HKD', '^HSI'],
                 'Barclays': ['Barclays', 42.929, 'BARC.L', 'GBP', '^FTSE'],
                 'BNP Paribas': ['BNP Paribas', 79.01, 'BNP.PA', 'EUR', '^STOXX50E'],
                 'China Construction Bank': ['China Construction Bank', 275.68, '0939.HK', 'HKD', '^HSI'],
                 'Goldman Sachs': ['Goldman Sachs', 89.794, 'GS', 'USD', '^GSPC'],
                 'Industrial and Commercial Bank of China Limited': ['ICBC', 255.30, '1398.HK', 'HKD', '^HSI'],
                 'Mitsubishi UFJ FG': ['Mitsubishi FG', 80.531, '8306.T', 'JPY', '^N225'],
                 'Wells Fargo': ['Wells Fargo', 285.222, 'WFC', 'USD', '^GSPC'],
                 'Agricultural Bank of China': ['Agricultural Bank of China', 159.5, '1288.HK', 'HKD', '^HSI']
                 }
    
    
    nodesAttributes = {mapNodes[g][0]: [mapNodes[g][1], mapNodes[g][2], mapNodes[g][3], mapNodes[g][4]] for g in mapNodes}
    
    return nodesAttributes, mapNodes



##  This function uses raw data (originated by Factset) in csv files representing the percentage of each financial company from a 
#   selected list owned by any other financial insitution in the world (including the other institution in the list)
#   The data are aggregated and consolidated in order to show for each company in the selected list the $amount owned by the other
#   companie in the list (methodology in the [1]). The final result is stored in a dataframe.
#
def cleanRawdata(data, mapNodes):
    
    #Aggregate ownership data from subsidiaries of the same entity    
    newData = pd.DataFrame([])
    newData['JP Morgan Chase'] = data[data.index.str.contains("JPM")==True].sum()
    newData['Morgan Stanley'] = data[data.index.str.contains('Morgan Stanley')==True].sum()
    newData['Royal Bank of Canada'] = data[data.index.str.contains(r'RBC |[Rr]oyal.*[Bb]ank.*Canada')==True].sum()
    newData['Royal Bank of Scotland'] = data[data.index.str.contains("Royal Bank of Scotland")==True].sum()
    newData['Santander'] = data[data.index.str.contains("Santander")==True].sum()
    newData['Société Generale'] = data[data.index.str.contains(r'[Ss]ociete [Gg]enerale|^SG ')==True].sum()
    newData['Standard Chartered'] = data[data.index.str.contains("Standard Chartered")==True].sum()
    newData['State Street'] = data[data.index.str.contains(r'State Street')==True].sum()
    newData['Sumitomo Mitsui FG'] = data[data.index.str.contains("Sumitomo Mitsui")==True].sum()
    newData['UBS'] = data[data.index.str.contains("UBS")==True].sum()
    newData['Unicredit Group'] = data[data.index.str.contains(r'Uni[Cc]redit')==True].sum()
    newData['Bank of New York Mellon'] = data[data.index.str.contains("Mellon")==True].sum()
    newData['Credit Suisse'] = data[data.index.str.contains(r'[Cc]redit [sS]uisse|^CS ')==True].sum()
    newData['Groupe Crédit Agricole'] = data[data.index.str.contains("Credit Agricole")==True].sum()
    newData['ING'] = data[data.index.str.contains(r'^ING')==True].sum()
    newData['Mizuho FG'] = data[data.index.str.contains("Mizuho")==True].sum()
    newData['Nordea'] = data[data.index.str.contains("Nordea")==True].sum()
    newData['Bank of America'] = data[data.index.str.contains(r'Ban[ck] of America|Merrill Lynch')==True].sum()
    newData['Citigroup'] = data[data.index.str.contains(r'Citigroup|Citicorp|Citibank')==True].sum()
    newData['Deutsche Bank'] = data[data.index.str.contains(r'Deutsche Bank|Deutsche Asset|Deutsche Invest|^DB ')==True].sum()
    newData['HSBC'] = data[data.index.str.contains("HSBC")==True].sum()
    newData['Barclays'] = data[data.index.str.contains("Barclays")==True].sum()
    newData['BNP Paribas'] = data[data.index.str.contains("BNP ")==True].sum()
    newData['Goldman Sachs'] = data[data.index.str.contains("Goldman Sachs")==True].sum()
    newData['Industrial and Commercial Bank of China Limited'] = data[data.index.str.contains("ICBC")==True].sum()
    newData['Mitsubishi UFJ FG'] = data[data.index.str.contains("Mitsubishi UFJ")==True].sum()
    newData['Wells Fargo'] = data[data.index.str.contains("Wells Fargo")==True].sum()
    newData['Bank of China'] = data[data.index.str.contains("Bank of China")==True].sum()
    newData['China Construction Bank'] = data[data.index.str.contains("China Construction Bank")==True].sum()
    newData['Agricultural Bank of China'] = data[data.index.str.contains("Agricultural Bank of China")==True].sum()
    
    # Transform ownership data in $ terms
    for c in newData.columns:
        newData[c] = newData[c] * (mapNodes[c][1])
    
    # Reindexing using yahoo denomination 
    newData['Temp'] = newData.index
    newData['Temp'] = newData['Temp'].str.strip() #trim
    
    for i in range(newData['Temp'].shape[0]):
        newData['Temp'][i] = mapNodes[newData['Temp'][i]][0]
    
    newData.index = newData['Temp']
    del newData['Temp']
    
    # Rename columns using yahoo denomination 
    for k in newData.columns:
        newData.rename(columns = { k : mapNodes[k][0]}, inplace = True)
    
    # Ensure columns and index are ordered in the same way
    newData = newData[list(newData.index)]
    newData = newData.T
    
    # Remove cycles
    for i in range(newData.shape[0]):
        newData.iloc[i][i] = 0
    
    
    ## From the matrix of the ownership data generates the network matrix
    #  Position (i,j) contains the impact of j over i, obtained by 
    #  dividing the investment of i in j by the sum of all the investment made by i over the rest of the matrix
    sumOwnership = newData.sum(axis = 1)
    network = newData.div(sumOwnership, axis = 0)
    
    network = network.replace(np.nan, 0)
    network = network.replace(np.inf, 0)
    
    maxImpact = network.max(axis = 1)
    
    # Normalization as per the suggestion in [] (will not be used)
    networkAdj = network.div(maxImpact, axis = 0)
    networkAdj = networkAdj*ALPHA
    networkAdj = networkAdj.applymap(lambda x: min(x, 1))
    networkAdj = networkAdj.replace(np.nan, 0)
    
    return network



def correlationNetwork(allPrices, period, window, nodesAttributes):
    allReturns = allPrices.pct_change(period)
    allReturns = allReturns.drop(allReturns.index[0:period-1])

    for k in nodesAttributes.keys():
        symbol = nodesAttributes[k][1]
        index = nodesAttributes[k][3]
        allReturns[symbol + '-ER'] = allReturns[symbol] - allReturns[index] #calculate excess return series
    
    excessReturns = allReturns[[nodesAttributes[i][1] + '-ER' for i in nodesAttributes.keys()]]
    excessReturns = excessReturns.iloc[-window:,:] # select only the last 'window' returns to calculate the correl
    correlationMatrix = excessReturns.corr()
    
    correlationMatrix[correlationMatrix<=0.3] = 0
    correlationMatrix[correlationMatrix==1] = 0
    
    # transform the correlation into a distance
    distances = correlationMatrix#np.sqrt(2*(1-correlationMatrix))
    
    inverseMap = {}
    for k in nodesAttributes.keys():
        inverseMap[nodesAttributes[k][1]] = k
    
    # rename columns and indices using nodes keys
    distances = distances.rename(columns=lambda x: x.replace('-ER', ''))
    distances = distances.rename(index=lambda x: x.replace('-ER', ''))
    
    
    for i in inverseMap.keys():
        distances = distances.rename(columns = {i:inverseMap[i] })
        distances = distances.rename(index = {i:inverseMap[i] })

    return distances



def main():
    
    extensionList = ['2010-08-10', '2018-08-10']
    networkAdj = {}
    correlationAdj = {}
    
    # creates nodes attributes
    nodesAttributes, mapNodes = createNodesAttributes()
  
    
    # price data from yahoo in csv file
    allPrices = pd.read_csv(settings.PATH + "allPrices.csv")
    allPrices.index = allPrices['Date']
    del allPrices['Date']
    
    # USD price data from yahoo in csv file
    allPricesUSD = pd.read_csv(settings.PATH + "allPricesUSD.csv")
    allPricesUSD.index = allPricesUSD['Date']
    del allPricesUSD['Date']
    
    
    # consolidates exposures data  
    for extension in extensionList:
        
        year = extension[0:4]
        position = allPrices.index.get_loc(extension)
        
        # Raw exposures data from facsect
        data = pd.read_csv(settings.PATH + "RawData_" + year +".csv")
        data.index = data.loc[:,data.columns[0]]
        del data[data.columns[0]]
        data = data.drop(data.index[0])
        data = data.apply(pd.to_numeric)
        
        # consolidate and clean raw data
        networkAdj[year] = cleanRawdata(data, mapNodes)
        
        # Get the return data and calculate correlation only if there are at leat 100 datapoints available
        if position >=100:
            relevantPrices = allPrices.iloc[:position,:]
            correlationAdj[year] = correlationNetwork(relevantPrices, 5, 200, nodesAttributes)

    
    # load data into sql tables
    db.createNodesAttributes(settings.DB)
    db.populateNodes(settings.DB, nodesAttributes)
    
    db.createNodesWeights(settings.DB1, nodesAttributes)
    db.createNodesWeights(settings.DB3, nodesAttributes)
    
    db.createPriceHistory(settings.DB2)
    db.populatePriceHistory(settings.DB2, nodesAttributes, allPrices)
    
    db.createPriceHistoryUSD(settings.DB4)
    db.populatePriceHistoryUSD(settings.DB4, nodesAttributes, allPricesUSD)
    
    for extension in extensionList:
        year = extension[0:4]
        position = allPrices.index.get_loc(extension)
        db.populateNodesWeights(settings.DB1, year, nodesAttributes, networkAdj[year])
        
        if position >=100:
            db.populateNodesWeights(settings.DB3, year, nodesAttributes, correlationAdj[year])



main()






































