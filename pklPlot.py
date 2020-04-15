from utilities.pklPlotTools import makeLegend, plot, makeStackedList, fillStacked, makeHistList, makePath, countSignal, countSignBkg
from utilities.utils import makeYlabels, str2tuple
from utilities.inputParser import readStack
from ROOT import gROOT, THStack
import pickle
from optparse import OptionParser
import sys
from numpy import loadtxt
import os

parser = OptionParser()
parser.add_option("-f", "--inputFile", default = "histograms/histList_2018_total.pkl", help = "input pkl file")
parser.add_option("-y", "--year", default = 2018, help = "year")
parser.add_option("-c", "--conf", default = "samples/2018_total.conf", help = "conf file")
parser.add_option("-s", "--stack", default = "samples/2018_total.stack", help = "stack file")
parser.add_option("-p", "--plot", default = "samples/2018_total.plot", help = "plot file")
parser.add_option("-t", "--typeList", default = None, help = "typeList")
parser.add_option("-o", "--onlyCount", default = "no", help = "Only count signal events, no plotting?")
options, args = parser.parse_args(sys.argv[1:])


# get all info on the data we want to plot                                           

typeList, sourceDict, texDict, colorDict = readStack(options.stack)

# the variables we want to plot                                                                  

plotList, binList, xLabelList, xtypeList = loadtxt(options.plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')

binList = [str2tuple(string) for string in binList]
yLabelList = makeYlabels(xtypeList, binList)

for i in range(len(plotList)):

    plotList[i] = plotList[i].rstrip()


# also make the plotter able to use seperate source files and then stack the hists together itself

if ',' in options.inputFile:

    sources = options.inputFile.split(',')
    print(sources)
    typeList = options.typeList.split(',')
    stackedList = makeStackedList(plotList)
    fillStacked(sources, stackedList)
    histList = makeHistList(sources)
    
    folder = makePath(sources[0])


else:

    histList = pickle.load(file(options.inputFile))[:-1]
    stackedList = pickle.load(file(options.inputFile))[-1]

    folder = makePath(options.inputFile)

#    countSignal(options.inputFile, histList, typeList, xLabelList)

    countSignBkg(options.inputFile, histList, typeList, xLabelList)


if not os.path.exists(folder):
    os.makedirs(folder)


if options.onlyCount == "no":

    gROOT.SetBatch(True)

    leg = makeLegend(typeList, histList, texDict)
    leg_2 = makeLegend(typeList, histList, texDict, (0.11, 0.7, 0.2, 0.89))

    plot(plotList, stackedList, xLabelList, yLabelList, leg, leg_2, year = options.year, folder = folder)
    plot(plotList, stackedList, xLabelList, yLabelList, leg, leg_2, year = options.year, logscale = 0, folder = folder)
