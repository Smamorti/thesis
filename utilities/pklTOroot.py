import pickle
from ROOT import TFile
import sys
from optparse import OptionParser
import os

# example usage:
# python utilities/pklTOroot.py -i test.pkl -o weights/MC_nTrueInt.root

parser = OptionParser()
parser.add_option('-i', '--inputfile')
parser.add_option('-o', '--outputfile')
options, args = parser.parse_args(sys.argv[1:])

outputFile = TFile(options.outputfile, 'RECREATE')
outputFile.cd()


hist = pickle.load(file(options.inputfile))
hist.Write()
outputFile.Close()
