from utilities.pklPlotTools import makeLegend, plot
from utilities.utils import makeYlabels, str2tuple
from ROOT import gROOT
import pickle
from optparse import OptionParser
import sys
from numpy import loadtxt

parser = OptionParser()
parser.add_option("-f", "--inputFile", default = "histograms/histList.pkl", help = "input pkl file")
parser.add_option("-s", "--stack", default = "samples/newSkim_2018.stack", help = "stack file")
parser.add_option("-c", "--conf", default = "samples/tuples_2018_newSkim.conf", help = "conf file")
parser.add_option("-p", "--plot", default = "samples/newSkim_2018.plot", help = ".plot file")
parser.add_option("-y", "--year", default = 2018, help = "year")

options, args = parser.parse_args(sys.argv[1:])

channels_stack, texList, _, colorList = loadtxt(options.stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = loadtxt(options.conf, comments = "%", unpack = True, dtype = str) 
plotList, binList, xLabelList, xtypeList = loadtxt(options.plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')
binList = [str2tuple(string) for string in binList]
colorList = colorList.astype(int)
xSecs = xSecs.astype(float)
yLabelList = makeYlabels(xtypeList, binList)

histList = pickle.load(file(options.inputFile))

gROOT.SetBatch(True)

leg = makeLegend(texList, histList)
leg_2 = makeLegend(texList, histList, (0.1, 0.7, 0.3, 0.9))

plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = options.year)
plot(plotList, histList, xLabelList, yLabelList, leg, leg_2, year = options.year, logscale = 0)

