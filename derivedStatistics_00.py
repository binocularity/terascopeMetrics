#
# Calculate additional derived statistics over all runs.
#

import pandas as pd
import numpy as np
import sys


print( "Calculating derived statistics" )


inFile='summaryStats_1024_20181108.csv'
outFile='derivedStats_1024_20181108.csv'

outDf = pd.read_csv( inFile, index_col = 0 )
print( outDf )

index = outDf.index.values

runNum = 1
outDf.loc[runNum,'runId'] = int(runNum)
outDf.loc[runNum,'uniqHosts'] = 1
outDf.loc[runNum,'uniqTasks'] = 65793
outDf.loc[runNum,'totTskTme'] = outDf.loc[index,'totTskTme'].mean()
outDf.loc[runNum,'avTskTme'] = outDf.loc[index,'avTskTme'].mean()
outDf.loc[runNum,'minTskTme'] = outDf.loc[index,'minTskTme'].mean()
outDf.loc[runNum,'maxTskTme'] = outDf.loc[index,'maxTskTme'].mean()
outDf.loc[runNum,'measuredS'] = 1
outDf.loc[runNum,'measuredEf'] = 1

sumRT = 0 
for runIndex in index:
    sumRT = sumRT + ( outDf.loc[runIndex,'totRunTme'] * outDf.loc[runIndex,'runId'] )
outDf.loc[runNum,'totRunTme'] = sumRT / len(index)



index = outDf.index.values
#Calculate relative speedups for each run
baseMeasuredNodes = float(outDf.loc[64,'runId'])
baseNodes = float(outDf.loc[1,'runId'])
baseTime = outDf.loc[1,'totRunTme']
for runNum in index :  
        if ( runNum == 1 ):
            outDf.loc[runNum,'idealMeasuredS'] = 1
        else:
            outDf.loc[runNum,'idealMeasuredS'] = outDf.loc[runNum,'runId']/baseMeasuredNodes
        
        outDf.loc[runNum,'idealRealS'] = outDf.loc[runNum,'runId']/baseNodes
        outDf.loc[runNum,'realS'] = baseTime/outDf.loc[runNum,'totRunTme']
        outDf.loc[runNum,'realEf'] = outDf.loc[runNum,'realS'] / outDf.loc[runNum,'idealRealS']
    

outDf = outDf.sort_values('runId')

print( outDf )
outDf.to_csv( outFile, index=False )