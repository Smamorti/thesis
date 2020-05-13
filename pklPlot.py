from utilities.pklPlotTools import makeLegend, plot, makeStackedList, fillStacked, makeHistList, makePath, countSignal, countSignBkg, makeSummedHist, makePath2
from utilities.utils import makeYlabels, str2tuple
from utilities.inputParser import readStack
from ROOT import gROOT, THStack
import pickle
from optparse import OptionParser
import sys
from numpy import loadtxt
import os
import numpy as np

parser = OptionParser()
parser.add_option("-f", "--inputFile", default = "histograms/histList_2018_total.pkl", help = "input pkl file")
parser.add_option("-y", "--year", default = 2018, help = "year")
parser.add_option("-c", "--conf", default = "samples/2018_total_v3.conf", help = "conf file")
parser.add_option("-s", "--stack", default = "samples/2018_total.stack", help = "stack file")
parser.add_option("-p", "--plot", default = "samples/2018_total.plot", help = "plot file")
parser.add_option("-t", "--typeList", default = None, help = "typeList")
parser.add_option("-o", "--onlyCount", default = "no", help = "Only count signal events, no plotting?")
parser.add_option("-d", "--dataFile", default = None, help = "Location of datafile?")
parser.add_option("-b", "--bottomPad", default = "Data/MC", help = "What info on bottom pad?")
parser.add_option("-e", "--extra", default = '', help = '')
options, args = parser.parse_args(sys.argv[1:])


# get all info on the data we want to plot                                           

typeList, sourceDict, texDict, colorDict = readStack(options.stack)

# the variables we want to plot                                                                  

plotList, binList, xLabelList, xtypeList = loadtxt(options.plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')

if type(plotList) != list and type(plotList) != np.ndarray:

    plotList = [plotList]
    binList = [binList]
    xLabelList = [xLabelList]
    xtypeList = [xtypeList]

binList = [str2tuple(string) for string in binList]
yLabelList = makeYlabels(xtypeList, binList)

for i in range(len(plotList)):

    plotList[i] = plotList[i].rstrip()


# also make the plotter able to use seperate source files and then stack the hists together itself

if options.typeList:

    typeList = options.typeList.split(',')

    location = options.inputFile.replace('.pkl', '')

    sources = [location + '_{}.pkl'.format(x) for x in typeList]
    
    stackedList = makeStackedList(plotList)
    fillStacked(sources, stackedList)
    histList = makeHistList(sources)

    folder = makePath2(sources[0])

else:

    histList = pickle.load(file(options.inputFile))[:-1]
    stackedList = pickle.load(file(options.inputFile))[-1]

    folder = makePath2(options.inputFile)

summedList = makeSummedHist(histList)

#    countSignal(options.inputFile, histList, typeList, xLabelList)

#    countSignBkg(options.inputFile, histList, typeList, xLabelList)

dataList = pickle.load(file(options.dataFile))

if not os.path.exists(folder):
    os.makedirs(folder)


if options.onlyCount == "no":

    gROOT.SetBatch(True)

    leg = makeLegend(typeList, histList, texDict, dataList)
    leg_2 = makeLegend(typeList, histList, texDict, dataList, (0.15, 0.685, 0.24, 0.875))

    plot(plotList, stackedList, dataList, summedList, xLabelList, yLabelList, leg, leg_2, year = options.year, folder = folder, bottomPad = options.bottomPad, extra = options.extra)
    plot(plotList, stackedList, dataList, summedList, xLabelList, yLabelList, leg, leg_2, year = options.year, logscale = 0, folder = folder, bottomPad = options.bottomPad, extra = options.extra)
