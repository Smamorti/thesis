from __future__ import division
from ROOT import TFile, TH1F, TCanvas, TList, TColor, TLegend, THStack
from ROOT import Math, gROOT
import numpy as np
import time
import makeHists, plot
import pickle
from utilities.utils import makeYlabels, str2tuple


stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"
plt = "samples/newSkim_2018.plot"

# stack = "samples/2018_v2.stack"
# conf = "samples/2018_v2.conf"

# stack = "samples/ttunder_2018.stack"
# conf = "samples/ttunder_2018.conf"

year = '2018'
#year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)


channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str) #different channel list to enable different ordering of events in .stack and .conf files, one can later match the two together
plotList, binList, xLabelList, xtypeList = np.loadtxt(plt, comments = "%" ,unpack = True, dtype = str, delimiter='\t')
binList = [str2tuple(string) for string in binList]
histList = makeHists.fillTList(channels_stack, plotList, binList)
colorList = colorList.astype(int)
xSecs = xSecs.astype(float)
yLabelList = makeYlabels(xtypeList, binList)


# plotList = ["leptonMVA"]
# binList = [(20, -1, 1)]
# histList = makeHists.fillTList(channels_stack, plotList, binList)
# xLabelList = ["leptonMVA"]
# xtypeList = ["Other"]
# yLabelList = makeYlabels(xtypeList, binList)


#
# Fill histograms
#

for i in range(len(files)):
#for i in range(0, 1):
    f = TFile.Open(files[i])
    print("Working on file number {}".format(i))
    print(files[i])
    print(channels_stack[i])
    makeHists.fillHist(f, xSecs[i], histList[i], plotList, year = year)
    
    f.Close()

start = time.time()

makeHists.fillColor(histList, colorList)
makeHists.fillStacked(histList)

#
#Plotting
#

gROOT.SetBatch(True)

# hardcoded different legend position for now


leg = makeHists.makeLegend(texList, histList)
leg_2 = makeHists.makeLegend(texList, histList, (0.1, 0.7, 0.3, 0.9))

plot.plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = year)
plot.plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, title =  "No Logscale", logscale = 0, histList_nonZ = histList, titleNotZ = "Logscale", logNotZ = 1, year = year)
plot.plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = year, logscale = 0)

print("Time elapsed: {} seconds".format((time.time() - start)))

pickle.dump(histList, file('histograms/histList.pkl', 'w'))
