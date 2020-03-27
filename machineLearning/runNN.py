from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
from trainNN import trainNN
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

configuration = {
        'number_of_hidden_layers' : 2,
        'units_per_layer' : 16,
        'optimizer' : 'Nadam',
        'activation' : 'leakyrelu',
        'learning_rate' : 0.1,
        'learning_rate_decay' : 1,
        'dropout_first' : True,
        'dropout_all' : True,
        'dropout_rate' : 0.3,
        'batchnorm_first' : True,
        'batchnorm_hidden' : True,
        'batchnorm_before_activation' : True,
        'number_of_epochs' : 2,#200,
        'batch_size' : 256,
        'input_shape' : ( len(branch_names), ),
        'number_of_threads' : 1 
    }


inputFile = TFile("../newTrees/reducedTrees/goodTreesTotal/trees_total_2018.root")

signalTree = inputFile.Get("tree_signal_total")
bkgTree = inputFile.Get("tree_background_total")

#validation and test fractions                                                                                                                                                                              
validation_fraction = 0.0
test_fraction = 0.0

# ensure reproducibility

np.random.seed(42)

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)
test_data = concatenateAndShuffleDatasets(signal_collection.test_set, background_collection.test_set)

model_name = 'testNN'

trainNN(model_name, configuration, training_data, validation_data, test_data, validation_fraction)
