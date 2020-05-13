#
# This script combines the trees from two root files into one root file, such that it can be used for ML purposes
#

from ROOT import TFile
from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-c", "--signal", default = "../newTrees/reducedTrees/goodTreesTotal/tree_signal_2018_nominal.root", help = "signal root file")
parser.add_option("-b", "--background", default = "../newTrees/reducedTrees/goodTreesTotal/tree_background_2018_nominal.root", help = "background root file")
parser.add_option("-o", "--outputfile", default = "../newTrees/reducedTrees/goodTreesTotal/trees_total_2018_nominal.root", help = "output root file")
parser.add_option("-y", "--year", default = 2018, help = "year")

options, args = parser.parse_args(sys.argv[1:])

outputFile = TFile(options.outputfile, 'RECREATE')
outputFile.cd()

signal = TFile.Open(options.signal)
outputFile.cd()
signalTree = signal.Get("tree_signal_2018")
signalTree.CloneTree().Write()
signal.Close()
del signalTree


bkg = TFile.Open(options.background)
outputFile.cd()
bkgTree = bkg.Get("tree_background_2018")
bkgTree.CloneTree().Write()
bkg.Close()
del bkgTree


outputFile.Close()
