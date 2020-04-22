from ROOT import TFile, TH1F
import sys
from optparse import OptionParser
import os
import pickle
import numpy as np

parser = OptionParser()
parser.add_option('-p', '--path', default = 'histograms/NN_final_80_0_20_18epochs_v3_wp=noWorkingPointv3/histList_2018_total_', help = 'path for normal histos')
parser.add_option('-u', '--pathJECUp', default = 'histograms/NN_final_80_0_20_18epochs_v3_wp=JECUp/histList_2018_total_', help = 'path for JECUp histos')
parser.add_option('-d', '--pathJECDown', default = 'histograms/NN_final_80_0_20_18epochs_v3_wp=JECDown/histList_2018_total_', help = 'path for JECDown histos')
parser.add_option('-o', '--output', default = 'shapes/shapeWithJEC.root', help = 'location of output root file')
parser.add_option('--plot', default = 'samples/2018_total.plot', help = 'location of used plot file')
options, args = parser.parse_args(sys.argv[1:])


sources = ['ttZ', 'ttX', 'ttW', 'tt', 'other', 'DY', 'data']
# types = ['', '_JECUp', '_JECDown']

types = ['']

plotList, _, _, _ = np.loadtxt(options.plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')

for i in range(len(plotList)):

    plotList[i] = plotList[i].rstrip()

# we want to only keep the modelOutput TH1F

index = np.argwhere(plotList == 'modelOutput')[0][0]


outputFile = TFile(options.output, 'RECREATE')
outputFile.cd()


for kind in types:

    path = options.path
    
    if kind == '_JECUp':

        path = options.pathJECUp

    elif kind == '_JECDown':

        path = options.JECDown

    for source in sources:

        print(source)

        histList = pickle.load(file(path + source + '.pkl'))
        hist = histList[index]
        hist.SetName(source + kind)
        print(hist.GetBinContent(40))

        hist.Write()

outputFile.Close()
