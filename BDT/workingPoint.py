from wpHelpers import makeOutput, plotOutputShapeComparison, plotSearchWP
from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
#from trainEvalBDT import *
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

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

#np.random.seed()

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)
test_data = concatenateAndShuffleDatasets(signal_collection.test_set, background_collection.test_set)

#print(training_data.weights)

#model_name = 'alpha=0p556325710785_colsampleBytree=0p870766472573_gamma=0p488195039022_learningRate=0p0087743285049_maxDepth=3_minChildWeight=10p0575232606_numberOfTrees=3240_subsample=0p5327601619'
model_name = 'isThisTheSame'
# trainBDT( training_data.samples, training_data.labels, train_weights = training_data.weights, 
#           feature_names = branch_names, model_name = model_name, number_of_trees = 1000, learning_rate = 0.01,  
#           max_depth = 5, min_child_weight = 10, subsample = 1, 
#           colsample_bytree = 0.5, gamma = 0, alpha = 0, number_of_threads = 1)

#evalBDT(model_name, signal_collection, background_collection)

makeOutput(model_name, signal_collection, background_collection)

plotOutputShapeComparison(
    signal_collection.training_set.outputs, signal_collection.training_set.weights,
    background_collection.training_set.outputs, background_collection.training_set.weights,
    signal_collection.validation_set.outputs, signal_collection.validation_set.weights,
    background_collection.validation_set.outputs, background_collection.validation_set.weights,
    model_name
    )

plotSearchWP(
    signal_collection.training_set.outputs, signal_collection.training_set.weights,
    background_collection.training_set.outputs, background_collection.training_set.weights,
    signal_collection.validation_set.outputs, signal_collection.validation_set.weights,
    background_collection.validation_set.outputs, background_collection.validation_set.weights,
    model_name
    )

