from __future__ import division
from ROOT import TFile, TH1F, TCanvas, TList, TColor, TLegend, THStack
from ROOT import Math, gROOT
import numpy as np
import time
import makeHists, plot
from utilities.utils import makeYlabels, str2tuple
from utilities.inputParser import readStack, readConf
from utilities.saveHistList import saveHistList
import sys
from optparse import OptionParser
import os


parser = OptionParser()
parser.add_option("-c", "--conf", default = "samples/2018_total.conf", help = "conf file")
parser.add_option("-s", "--stack", default = "samples/2018_total.stack", help = "stack file")
parser.add_option("-p", "--plot", default = "samples/2018_total.plot", help = "plot file")
parser.add_option("-o", "--output", default = None, help = "Output file for Histlist?")
parser.add_option("-y", "--year", default = "2018", help = "year")
parser.add_option("-t", "--testing", default = "no", help = "Run in test mode (1% of the data) or not?")
parser.add_option("-x", "--printHist", default = "no", help = "Print out hist content or not?")
parser.add_option("-m", "--MLalgo", default = "no", help = "Use ML algo?")
parser.add_option("-w", "--workingPoint", default = 0.5, help = "Working point?")
options, args = parser.parse_args(sys.argv[1:])

if options.testing not in ['yes', 'no'] or options.printHist not in ['yes', 'no']:

    raise ValueError("Please give a yes or no answer to testing and printHist")

if not options.output:

    if options.MLalgo:

        if not os.path.exists("histograms/{}_wp={}".format(options.MLalgo.replace(".h5", "").replace(".bin","").replace("machineLearning/models/", ""), options.workingPoint)):

            os.makedirs("histograms/{}_wp={}".format(options.MLalgo.replace(".h5", "").replace(".bin","").replace("machineLearning/models/", ""), options.workingPoint))

        output = "histograms/{}_wp={}/histList_{}.pkl".format(options.MLalgo.replace(".h5", "").replace(".bin","").replace("machineLearning/models/", ""), options.workingPoint ,options.stack.replace("samples/", "").replace(".stack", ""))
    
    else:

        output = "histograms/histList_{}.pkl".format(options.stack.replace("samples/", "").replace(".stack", ""))


else:

    output = options.output

print("Using files from {}".format(options.year))

# get all info on the data we want to plot

typeList, sourceDict, texDict, colorDict = readStack(options.stack)
locationDict, xSecDict = readConf(options.conf)

# the variables we want to plot

plotList, binList, xLabelList, xtypeList = np.loadtxt(options.plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')
print(xtypeList)
print(xLabelList)
binList = [str2tuple(string) for string in binList]
histList = makeHists.fillTList(typeList, plotList, binList)
yLabelList = makeYlabels(xtypeList, binList)

# load the ML model if we supplied one

if '.h5' in options.MLalgo:

    from keras.models import load_model

    model = load_model(options.MLalgo)

elif '.bin' in options.MLalgo:

    import xgboost as xgb

    model = xgb.Booster()
    model.load_model(options.MLalgo)

else:

    model = None

# Fill histograms

for i in range(len(typeList)):

    source = typeList[i]

    print('Currently working on {}.'.format(source))

    channels = sourceDict[source]
    print(channels)
    makeHists.fillHist(channels, xSecDict, locationDict, histList[i], plotList, year = options.year, testing = options.testing, printHists = options.printHist, model = model, algo = options.MLalgo, workingPoint = options.workingPoint)


# Plotting

start = time.time()

makeHists.fillColor(histList, colorDict, typeList)
makeHists.fillStacked(histList)

# save histograms to a .pkl file for later use

saveHistList(typeList, histList, output)


gROOT.SetBatch(True)

# hardcoded different legend position for now

leg = makeHists.makeLegend(typeList, histList, texDict)
leg_2 = makeHists.makeLegend(typeList, histList, texDict, (0.1, 0.7, 0.2, 0.9))

plot.plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = options.year, MLalgo = options.MLalgo, workingPoint = options.workingPoint)
plot.plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, title =  "No Logscale", logscale = 0, histList_nonZ = histList, titleNotZ = "Logscale", logNotZ = 1, year = options.year, MLalgo = options.MLalgo, workingPoint = options.workingPoint)
plot.plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = options.year, logscale = 0, MLalgo = options.MLalgo, workingPoint = options.workingPoint)

print("Time elapsed: {} seconds".format((time.time() - start)))

