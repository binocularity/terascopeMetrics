#
# Calculate measurd statistics over all runs.
#

import pandas as pd
import numpy as np
import sys


print( "Calculating measured statistics" )


outFile='summaryStats_1024_20181108.csv'

index = ['64','80','96','112','128','256','512','768','1024']

columns = ['runId','totTskTme','avTskTme', 'minTskTme', 'maxTskTme', 'totRunTme','idealS','measuredS','measuredEf','uniqHosts','uniqTasks']
outDf = pd.DataFrame(index=index, columns=columns)
outDf = outDf.fillna(0) # with 0s rather than NaNs
outDf['runId'] = map(int,index)

#Process shaped run data files.
for runNum in index :
    inFile ='stats-Render-STOP-shaped-'+runNum+'.csv'
    print( inFile )
    inData = pd.read_csv(inFile)
    print( inData.head() )
    
    outDf.loc[runNum,'totTskTme'] = inData['duration'].sum()
    outDf.loc[runNum,'avTskTme'] = inData['duration'].mean()
    outDf.loc[runNum,'minTskTme'] = inData['duration'].min()
    outDf.loc[runNum,'maxTskTme'] = inData['duration'].max()
    outDf.loc[runNum,'uniqHosts'] = inData['host'].nunique()
    outDf.loc[runNum,'uniqTasks'] = inData['taskId'].nunique()    
    
    minStart = inData['stopTime'].min()
    maxStop =  inData['stopTime'].max()
    outDf.loc[runNum,'totRunTme'] = maxStop - minStart
    
#Calculate speedups for each run   
baseNodes = float(outDf.loc[index[0],'runId'])
baseTime = outDf.loc[index[0],'totRunTme']
for runNum in index :  
        outDf.loc[runNum,'idealS'] = outDf.loc[runNum,'runId']/baseNodes
        outDf.loc[runNum,'measuredS'] = baseTime/outDf.loc[runNum,'totRunTme']
        outDf.loc[runNum,'measuredEf'] = outDf.loc[runNum,'measuredS'] / outDf.loc[runNum,'idealS']

outDf.index.name='index'

print( outDf )
outDf.to_csv( outFile )