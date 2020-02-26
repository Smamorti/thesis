from treeToArray import treeToArray
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from ROOT import TFile
from sklearn.utils import shuffle
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets

branch_names = [
    'lPt1', 'lPt2',
    'lEta1', 'lEta2',
    'lPhi1', 'lPhi2',
    'DeltaR_1', 'DeltaR_b1', 'DeltaR_2', 'DeltaR_b2',
    'njets', 'nbjets', 'jetDeepCsv_b1',
    'mW1', 'mtop1'
    ]

inputFile = TFile("../newTrees/reducedTrees/goodTrees/trees_2018.root")

signalTree = inputFile.Get("tree_signal")
# signal = treeToArray( signalTree, branch_names)

bkgTree = inputFile.Get("tree_background")
# background = treeToArray( bkgTree, branch_names)

# inputFile.Close()

# print(signal.shape)
# print(background.shape)

#validation and test fractions                                                                                                                                                                              
validation_fraction = 0.4
test_fraction = 0.2

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)

print(training_data.samples.shape)
print(validation_data.samples.shape)

####
# model definition
####

training_matrix = xgb.DMatrix( training_data.samples, weight = training_data.weights, label = training_data.labels, nthread = 1, feature_names = branch_names )

model_parameters = {
    'learning_rate' : 0.05,
    'max_depth' : 4,
    'min_child_weight' : 5,
    'subsample' : 1,
    'colsample_bytree' : 0.5,
    'gamma' : 0,
    'alpha' : 0,
    'nthread' : 1
}

booster = xgb.train( model_parameters, training_matrix, 500 )

model_name = 'model'
booster.save_model( model_name + '.bin' )

#plot feature importance 
xgb.plot_importance( booster )
plt.gcf().subplots_adjust( left = 0.22 )
plt.xlabel( 'Number of splittings', fontsize = 16 )
plt.ylabel( 'Feature', fontsize = 16 )
plt.savefig( 'feature_importance_' + model_name + '.pdf' )
plt.savefig( 'feature_importance_' + model_name + '.png' )
plt.clf()

#reset the figure margins for future plots
plt.gcf().subplots_adjust( left = 0.125 )
