from utilities.pklPlotTools import makeLegend, plot
from utilities.utils import makeYlabels, str2tuple
from utilities.inputParser import readStack
from ROOT import gROOT, THStack
import pickle
from optparse import OptionParser
import sys
from numpy import loadtxt
# from utilities.pklPlotTools import stackHists


parser = OptionParser()
parser.add_option("-f", "--inputFile", default = "histograms/histList_2018_total.pkl", help = "input pkl file")
parser.add_option("-y", "--year", default = 2018, help = "year")
parser.add_option("-c", "--conf", default = "samples/2018_total.conf", help = "conf file")
parser.add_option("-s", "--stack", default = "samples/2018_total.stack", help = "stack file")
parser.add_option("-p", "--plot", default = "samples/newSkim_2018.plot", help = "plot file")

options, args = parser.parse_args(sys.argv[1:])

# also make the plotter able to use seperate source files and then stack the hists together itself

# if ',' in options.inputFile:

#     sources = options.inputFile.split(',')

    ### WORK IN PROGRESS

# get all info on the data we want to plot                                           

typeList, sourceDict, texDict, colorDict = readStack(options.stack)

# the variables we want to plot                                                                  

plotList, binList, xLabelList, xtypeList = loadtxt(options.plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')

binList = [str2tuple(string) for string in binList]
yLabelList = makeYlabels(xtypeList, binList)

histList = pickle.load(file(options.inputFile))

gROOT.SetBatch(True)

leg = makeLegend(typeList, histList, texDict)
leg_2 = makeLegend(typeList, histList, texDict, (0.1, 0.7, 0.2, 0.9))

plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = options.year)
plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = options.year, logscale = 0)

