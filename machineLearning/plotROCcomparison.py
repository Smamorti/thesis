import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from diagnosticPlotting import computeROC, backgroundRejection, areaUnderCurve
from wpHelpers import makeOutputNN, makeOutputBDT
from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
from utils import plotSignalBkgWRTwp

branch_names = [
    'lPt1', 'lPt2',
    'lEta1', 'lEta2',
    'lPhi1', 'lPhi2',
    'DeltaR_1', 'DeltaR_b1', 'DeltaR_2', 'DeltaR_b2',
    'njets', 'nbjets', 'jetDeepCsv_b1',
    'jetPt1', 'jetEta1', 'jetPhi1',
    'jetPt2', 'jetEta2', 'jetPhi2',
    'jetPt3', 'jetEta3', 'jetPhi3',
    'jetPt4', 'jetEta4', 'jetPhi4',
    'jetPt5', 'jetEta5', 'jetPhi5',
    'mW1', 'mtop1',
    'MET', 'H_t',
    'I_rel1', 'I_rel2'
    ]

inputFile = TFile("../newTrees/reducedTrees/goodTreesTotal/trees_total_2018.root")

signalTree = inputFile.Get("tree_signal_total")
bkgTree = inputFile.Get("tree_background_total")

#validation and test fractions                                                                                
 
validation_fraction = 0.2
test_fraction = 0.2

# ensure reproducibility

np.random.seed(42)

signal_collection_BDT = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True, wp = True)
background_collection_BDT = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True, wp = True)

np.random.seed(42) # needed to reset the seed!!!

signal_collection_NN = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True, wp = True)
background_collection_NN = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True, wp = True)



# models

NN_model = 'NN_final_602020_run2'
BDT_model = 'BDT_final_602020'

# make outputs

makeOutputNN(NN_model, signal_collection_NN, background_collection_NN)
makeOutputBDT(BDT_model, signal_collection_BDT, background_collection_BDT)

print(signal_collection_NN.validation_set.outputs.shape)
print(background_collection_NN.validation_set.outputs.shape)
print(signal_collection_BDT.validation_set.outputs.shape)
print(background_collection_BDT.validation_set.outputs.shape)

print(np.sum(signal_collection_NN.validation_set.weights))
print(np.sum(background_collection_NN.validation_set.weights))
print(np.sum(signal_collection_BDT.validation_set.weights))
print(np.sum(background_collection_BDT.validation_set.weights))



# compute ROCs

eff_signal_NN, eff_background_NN = computeROC(
            np.resize(signal_collection_NN.validation_set.outputs, (signal_collection_NN.validation_set.outputs.shape[0], )),
                signal_collection_NN.validation_set.weights,
             np.resize(background_collection_NN.validation_set.outputs, (background_collection_NN.validation_set.outputs.shape[0], )),
                background_collection_NN.validation_set.weights,
                num_points = 10000
            )

eff_signal_BDT, eff_background_BDT = computeROC(
        signal_collection_BDT.validation_set.outputs,
        signal_collection_BDT.validation_set.weights,
        background_collection_BDT.validation_set.outputs,
        background_collection_BDT.validation_set.weights,
        num_points = 10000
            )

AUC_NN = areaUnderCurve(eff_signal_NN, eff_background_NN)
AUC_BDT = areaUnderCurve(eff_signal_BDT, eff_background_BDT)

print(AUC_NN)
print(AUC_BDT)

plt.plot( eff_signal_NN, backgroundRejection(eff_background_NN) , 'b', lw=2, label = 'NN (AUC = {})'.format(np.round(AUC_NN, 3)))
plt.plot( eff_signal_BDT, backgroundRejection(eff_background_BDT) , 'r', lw=2, label = 'BDT (AUC = {})'.format(np.round(AUC_BDT, 3)))


plt.xlabel( 'Signal efficiency', fontsize = 16 )
plt.ylabel( 'Background rejection', fontsize = 16 )

plt.legend(prop={"size":8})

plt.grid(True)
plt.savefig('results/roc_comparison.pdf')
plt.savefig('results/roc_comparison.png')

plt.clf()



plotSignalBkgWRTwp(
    signal_collection_NN.validation_set.outputs, 
    signal_collection_NN.validation_set.weights,
    background_collection_NN.validation_set.outputs,
    background_collection_NN.validation_set.weights,
    signal_collection_BDT.validation_set.outputs,
    signal_collection_BDT.validation_set.weights,
    background_collection_BDT.validation_set.outputs,
    background_collection_BDT.validation_set.weights
    )
