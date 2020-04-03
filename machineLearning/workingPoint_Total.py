from wpHelpers import makeOutputNN, plotOutputShapeComparison, plotSearchWP, wpMetrics, BDTandNN, makeOutputBDT
from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets, Dataset
from trainEvalBDT import *
import numpy as np

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
test_fraction = 0.0

# ensure reproducibility

np.random.seed(42)

# BDT part

signal_collection_BDT = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True, wp = True)
background_collection_BDT = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True, wp = True)

# training_data = concatenateAndShuffleDatasets(signal_collection_BDT.training_set, background_collection_BDT.training_set)
# validation_data = concatenateAndShuffleDatasets(signal_collection_BDT.validation_set, background_collection_BDT.validation_set)
# test_data = concatenateAndShuffleDatasets(signal_collection_BDT.test_set, background_collection_BDT.test_set)

model_name_BDT = 'BDT_final_fullData'


makeOutputBDT(model_name_BDT, signal_collection_BDT, background_collection_BDT)
# plotROCAndShapeComparison(signal_collection_BDT, background_collection_BDT, model_name_BDT )

BDT  = wpMetrics(model_name_BDT, signal_collection_BDT, background_collection_BDT, 'BDT')

# NN part

signal_collection_NN = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True, wp = True)
background_collection_NN = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True, wp = True)

# training_data = concatenateAndShuffleDatasets(signal_collection_NN.training_set, background_collection_NN.training_set)
# validation_data = concatenateAndShuffleDatasets(signal_collection_NN.validation_set, background_collection_NN.validation_set)
# test_data = concatenateAndShuffleDatasets(signal_collection_NN.test_set, background_collection_NN.test_set)

#model_name_NN = 'testNN80-20'
model_name_NN = 'NN_Best_FullData_18epochs'

makeOutputNN(model_name_NN, signal_collection_NN, background_collection_NN)
# plotROCAndShapeComparison(signal_collection_NN, background_collection_NN, model_name_NN )

NN  = wpMetrics(model_name_NN, signal_collection_NN, background_collection_NN, 'NN')

# make combined plots

BDTandNN(BDT, NN)

