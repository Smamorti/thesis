from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
from trainEvalBDT import *
import json
import sys

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


input_file_path = sys.argv[1]

parameter_dict = {}
with open( input_file_path ) as f:
    parameter_dict = json.load( f )

inputFile = TFile("../newTrees/reducedTrees/goodTreesTotal/trees_total_2018_nominal.root")

signalTree = inputFile.Get("tree_signal_2018")
bkgTree = inputFile.Get("tree_background_2018")


#validation and test fractions                                                                                                                                                                              
validation_fraction = 0.2
test_fraction = 0.2

# ensure reproducibility

np.random.seed(42)

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)
test_data = concatenateAndShuffleDatasets(signal_collection.test_set, background_collection.test_set)

model_name = sys.argv[1].replace(".json", "").replace("jsons/", "")

trainBDT(training_data.samples, training_data.labels, train_weights = training_data.weights, feature_names = branch_names, model_name = model_name, alpha= parameter_dict['alpha'], colsample_bytree= parameter_dict['colsample_bytree'], gamma= parameter_dict['gamma'], learning_rate= parameter_dict['learning_rate'], max_depth= parameter_dict['max_depth'], min_child_weight= parameter_dict['min_child_weight'], number_of_trees= parameter_dict['number_of_trees'], subsample= parameter_dict['subsample'], number_of_threads = 1)


# model_name = 'BDT_gen1_9_602020'

# trainBDT(training_data.samples, training_data.labels, train_weights = training_data.weights, feature_names = branch_names, model_name = model_name, alpha= 0.24381717415896353, colsample_bytree= 0.5942614980268284, gamma= 0.38452327994920754, learning_rate= 0.20379440652737038, max_depth= 3, min_child_weight= 3.5265307141035, number_of_trees= 3495, subsample= 0.376355753917916, number_of_threads = 1)


# trainBDT( training_data.samples, training_data.labels, train_weights = training_data.weights, 
#           feature_names = branch_names, model_name = model_name, number_of_trees = 3351, learning_rate = 0.00890837798958, max_depth = 3, min_child_weight = 10.6625443577, subsample = 0.532977100111, colsample_bytree = 0.872556671469, gamma = 0.44060113248, alpha = 0.700171854761, number_of_threads = 1)


evalBDT(model_name, signal_collection, background_collection)

#evalBDT_fullData(model_name, signal_collection, background_collection)
