from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
from trainEvalBDT import *

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
    'mW1', 'mtop1'
    ]

#inputFile = TFile("../newTrees/reducedTrees/goodTrees_JetKins/trees_2018.root")
inputFile = TFile("../newTrees/reducedTrees/goodTreesTotal/trees_total_2018.root")

signalTree = inputFile.Get("tree_signal_total")
bkgTree = inputFile.Get("tree_background_total")

#validation and test fractions                                                                                                                                                                              
validation_fraction = 0.4
test_fraction = 0.2

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)

model_name = 'model_test_2'

trainBDT( training_data.samples, training_data.labels, train_weights = training_data.weights, 
          feature_names = branch_names, model_name = model_name, number_of_trees = 100, learning_rate = 0.1,  
          max_depth = 10, min_child_weight = 1, subsample = 0.5, 
          colsample_bytree = 1, gamma = 0, alpha = 0, number_of_threads = 1)

evalBDT(model_name, signal_collection, background_collection)



