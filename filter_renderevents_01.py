#
# Clean up raw run data for "render" files
#

import pandas as pd
import numpy as np
import sys
import os

runNum = '64'
#runNum = '80'
#runNum = '96'
#runNum = '112'
#runNum = '128'
#runNum = '256'
#runNum = '512'
#runNum = '768'
#runNum = '1024'

print( os.getcwd() )

dataFolder = os.getcwd() + '/DataWrangling/20181108Terascope_01/'

inFile =dataFolder+'stats-Render-STOP-'+runNum+'.csv'
outFile = dataFolder+'stats-Render-STOP-shaped-'+runNum+'.csv'

data  = pd.read_csv(inFile)
#print ( sys.getsizeof( data ) )


data_out = data.rename( {'timestamp-epoch':'stopTime', 'timestamp':'date'}, axis='columns' )

#Add day so that PBI has the column
data_out['day'] = '08/11/2018'

print( inFile )
print( "Num columns raw: ", data_out.shape)
data_out = data_out.drop_duplicates('taskId')
print( "Num columns taskId filtered: ", data_out.shape)

#
# Ensure that the task indicies when added are in time order.
#
data_out = data_out.sort_values(['stopTime'])

#
# Create task indices and layout X,Y coordinates.
#
data_out.insert(0, 'taskIx', range(0, 0 + data_out.shape[0]) )
a = divmod(data_out['taskIx'],257)
data_out.insert(1, 'taskX', a[0] )
data_out.insert(2, 'taskY', a[1] )


#
# Create host indices and layout X,Y coordinates
#
# Find unique host names
df = pd.DataFrame()
df.insert(0, 'host', data_out['host'] )
df = df.drop_duplicates('host')



#Create host indices
df.insert(0, 'hostIx', range(0, 0 + df.shape[0]) )
a = divmod(df['hostIx'],32)
df.insert(1, 'hostX', a[0] )
df.insert(2, 'hostY', a[1] )

#Merge into original data
data_merged = pd.merge(data_out, df, on='host')

#Set start time from 0
minStop = data_merged['stopTime'].min()
data_merged['stopTime'] =  data_merged['stopTime'] - minStop


#
# Label ventiles of stopTime - cut into equal time steps 
#
data_merged['stopVentile'] = pd.cut(data_merged['stopTime'], 20, labels=False)
data_merged['durationHalves'] = pd.cut(data_merged['duration'], 2, labels=False)
data_merged['durationVentiles'] = pd.cut(data_merged['duration'], 20, labels=False)

#print( data_merged.head())
#print( data_merged.tail())

data_merged.to_csv( outFile, index=False )

print( data_merged.shape )
print( data_merged.columns )