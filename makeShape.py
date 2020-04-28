from ROOT import TFile, TH1F
import sys
from optparse import OptionParser
import os
import pickle
import numpy as np

parser = OptionParser()
# parser.add_option('-p', '--path', default = 'histograms/NN_final_80_0_20_18epochs_v3_wp=normal/histList_2018_total_', help = 'path for normal histos')
# parser.add_option('-u', '--pathJECUp', default = 'histograms/NN_final_80_0_20_18epochs_v3_wp=JECUp/histList_2018_total_', help = 'path for JECUp histos')
# parser.add_option('-d', '--pathJECDown', default = 'histograms/NN_final_80_0_20_18epochs_v3_wp=JECDown/histList_2018_total_', help = 'path for JECDown histos')
# parser.add_option('-o', '--output', default = 'shapes/shapeWithJEC.root', help = 'location of output root file')
# parser.add_option('--plot', default = 'samples/2018_total.plot', help = 'location of used plot file')
parser.add_option('-a', '--algo', default = 'NN', help = 'which ML algo do you want to use?') 
options, args = parser.parse_args(sys.argv[1:])


if options.algo == 'NN':

    plot = 'samples/2018_total.plot'

    partPath = 'histograms/withFitWeights/NN_final_80_0_20_18epochs_v3_wp={}_fitWeights/histList_2018_total_'
#    partPath = 'histograms/NN_final_80_0_20_18epochs_v3_wp={}/histList_2018_total_'

    output = 'shapes/shapeFile_NN_withFitWeights.root'
#    output = 'shapes/shapeFile_NN_fineBins.root'

elif options.algo == 'BDT':

    plot = 'samples/2018_total_BDT.plot'

    partPath = 'histograms/BDT_final_80_0_20_v3_wp={}/histList_2018_total_'

    output = 'shapes/shapeFile_BDT_fineBins.root'

else:

    raise ValueError('Please choose a valid ML algo (NN or BDT)')

sources = ['ttZ', 'ttX', 'ttW', 'tt', 'other', 'DY', 'data']
types = ['', '_JECUp', '_JECDown']

# types = ['']

plotList, _, _, _ = np.loadtxt(plot, comments = "%" ,unpack = True, dtype = str, delimiter='\t')

for i in range(len(plotList)):

    plotList[i] = plotList[i].rstrip()

# we want to only keep the modelOutput TH1F

index = np.argwhere(plotList == 'modelOutput')[0][0]
#index = np.argwhere(plotList == 'modelOutput2')[0][0]


outputFile = TFile(output, 'RECREATE')
outputFile.cd()


for kind in types:

    if kind == '':

        path = partPath.format('normal')

    else:

        path = partPath.format(kind.replace('_', ''))
    
    print(path)

    for source in sources:

        print(source)
        histList = pickle.load(file(path + source + '.pkl'))
        hist = histList[index]
       
        if source == 'data':

            source = 'data_obs'
    
        hist.SetName(source + kind)
        print(hist.GetBinContent(20))

        hist.Write()

outputFile.Close()
