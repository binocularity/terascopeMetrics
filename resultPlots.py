import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os

dataFolder = os.getcwd() + '/DataWrangling/20181108Terascope_01/'

inFile=dataFolder+'summaryStats_1024_20181108.csv'
outFile = dataFolder+"neasuredSPlot.svg"

plotDf = pd.read_csv( inFile, index_col = 0 )

fg = plt.figure()
thePlot = fg.gca()
thePlot.plot( plotDf['runId'], plotDf['measuredS'], color='lime', marker = '.', markeredgecolor = 'black', markerfacecolor = 'black' )
plt.xlabel('runId')
plt.ylabel('measuredS')
plt.xlim((0,1200))

for i,j in plotDf[['runId','measuredS']].values:
    if ( (i < 65) or (i > 112) ):
        plt.annotate( '{:5.1f}'.format(j), xy=(i+20,j) )

plt.draw() # necessary to render figure before saving
fg.savefig(outFile, bbox_inches='tight')
