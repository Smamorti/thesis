from __future__ import division
from ROOT import TFile, TH1F, TCanvas, TList, TColor, TLegend, THStack
from ROOT import Math, gROOT
import numpy as np
import time
import makeHists, plot


# stack = "task1_2018.stack" 
# conf = "tuples_2018.conf"

# stack = "task1_2017.stack" 
# conf = "tuples_2017.conf"

def makeYlabels(xtypeList, binList):

    yLabels = []
    
    for i in range(len(xtypeList)):

        if xtypeList[i] == "Other":

            yLabels.append("Events")

        elif xtypeList[i] == "GeV":

            binWidth = (binList[i][2] - binList[i][1]) / binList[i][0]
            
            if binWidth == 1.0:

                yLabels.append("Events / GeV")

            elif binWidth == (binList[i][2] - binList[i][1]) // binList[i][0]:

                yLabels.append("Events / {} GeV".format(int(binWidth)))

            else:

                yLabels.append("Events / {} GeV".format(binWidth))

    return yLabels

stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"

year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)


channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str) #different channel list to enable different ordering of events in .stack and .conf files, one can later match the two together


colorList = colorList.astype(int)
xSecs = xSecs.astype(float)


plotList = ["leading_lPt", "subleading_lPt", "leading_lEta", "subleading_lEta","nJets", "m_ll", "flavComp", "nbJets", "MET", "leading_DeltaR", "leading_DeltaR_b", "subleading_DeltaR", "subleading_DeltaR_b", "leading_leptonMVA", "subleading_leptonMVA", "bestW", "secondW", "bestTop", "secondTop"]
binList = [(20, 0, 200), (20, 0, 200), (10, 0, 2.5), (10, 0, 2.5), (12, 0, 12), (10, 81, 101), (2, 0, 2), (5, 0, 5), (20, 0, 500), (12, 0, 4.8), (12, 0, 4.8), (12, 0, 4.8), (12, 0, 4.8), (20, -1, 1), (20, -1, 1), (20, 55, 105), (20, 55, 105), (10, 148, 198), (10, 148, 198)]
histList = makeHists.fillTList(channels_stack, plotList, binList)  
xLabelList = ["p_{T}(l_{1}) (GeV)", "p_{T}(l_{2}) (GeV)", "|#eta|(l_{1})", "|#eta|(l_{2})", "nJets", "m(ll) (GeV)", "flavComp", "nbJets", "MET (GeV)", "#DeltaR(l_{1}, j)", "#DeltaR(l_{1}, b)", "#DeltaR(l_{2}, j)", "#DeltaR(l_{2}, b)", "leptonMVA l1", "leptonMVA l2", "m(W1) (GeV)", "m(W2) (GeV)", "m(top1) (GeV)", "m(top2) (GeV)"]
xtypeList = ["GeV", "GeV", "Other", "Other", "Other", "GeV", "Other", "Other", "GeV", "Other", "Other", "Other", "Other", "Other", "Other", "GeV", "GeV","GeV", "GeV"]
yLabelList = makeYlabels(xtypeList, binList)


#
# Fill histograms
#

#for i in range(len(files)):
for i in range(0, 1):
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

leg = makeHists.makeLegend(texList, histList)

plot.plot(plotList, histList, xLabelList, yLabelList, leg, year = year)
plot.plot(plotList, histList, xLabelList, yLabelList, leg,title =  "No Logscale", logscale = 0, histList_nonZ = histList, titleNotZ = "Logscale", logNotZ = 1, year = year)
plot.plot(plotList, histList, xLabelList, yLabelList, leg, year = year, logscale = 0)

print("Time elapsed: {} seconds".format((time.time() - start)))
