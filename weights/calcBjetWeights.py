from ROOT import TFile, TF1, gROOT, TList
import ROOT
import numpy as np
import sys
from optparse import OptionParser
import os

parser = OptionParser()
parser.add_option("-c", "--csv", default = "DeepCSV_94XSF_WP_V4_B_F.csv", help = "input csv file?")
options, args = parser.parse_args(sys.argv[1:])

def getWeightFormula(formula, i):

    gROOT.ProcessLine('#include <string>')
    gROOT.ProcessLine('TF1 f'+str(i)+'("f'+str(i)+'", '+formula[i].strip()+');')     

    return  getattr(ROOT, 'f'+str(i))


OperatingPoint, measurementType, sysType, jetFlavor, etaMin, etaMax, ptMin, ptMax, discrMin, discrMax, formulas = np.loadtxt(options.csv, unpack = True, skiprows = 1, delimiter = ', ', dtype = str)

print(formulas[(sysType == 'up') & (measurementType == 'incl') & (OperatingPoint == '0')])


tformulas = TList()

for i in range(len(formulas)):

    f = getWeightFormula(formulas, i)

    tformulas.Add(f)

for x in tformulas:

    print(x.Eval(50))

