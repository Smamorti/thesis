from treeToArray import treeToArray
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from ROOT import TFile
from sklearn.utils import shuffle
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
#from diagnosticPlotting import computeEfficiency, computeROC, backgroundRejection, plotROC, areaUnderCurve, plotOutputShapeComparison
from diagnosticPlotting import *

#evaluate a model from its outputs and weights for signal and background 
def rocAndAUC( signal_dataset, background_dataset, model_name ):
    
    #plot ROC curve and compute ROC integral for validation set 
    eff_signal, eff_background = computeROC(
            signal_dataset.outputs,
                signal_dataset.weights,
                background_dataset.outputs,
                background_dataset.weights,
                num_points = 10000
            )
    plotROC( eff_signal, eff_background, model_name )
    auc = areaUnderCurve(eff_signal, eff_background )
    print('#####################################################')
    print('validation set ROC integral (AUC) = {:.5f}'.format(auc) )
    print('#####################################################')
    

def compareOutputShapes( signal_training_dataset, signal_validation_dataset, background_training_dataset, background_validation_dataset, model_name):

    #compare output shapes 
    plotOutputShapeComparison( 
        signal_training_dataset.outputs, signal_training_dataset.weights,
            background_training_dataset.outputs, background_training_dataset.weights,
        signal_validation_dataset.outputs, signal_validation_dataset.weights,
            background_validation_dataset.outputs, background_validation_dataset.weights,
            model_name
        )


#plot ROC curve, compute AUC and plot shape comparison after adding model predictions to the datasets 
def plotROCAndShapeComparison(signal_collection, background_collection, model_name ):
    rocAndAUC( signal_collection.validation_set, background_collection.validation_set, model_name )
    compareOutputShapes(
        signal_collection.training_set,
        signal_collection.validation_set,
        background_collection.training_set,
        background_collection.validation_set,
        model_name
    )


######
#MAIN#
######



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



inputFile = TFile("../newTrees/reducedTrees/goodTrees_JetKins/trees_2018.root")

signalTree = inputFile.Get("tree_signal")
bkgTree = inputFile.Get("tree_background")

#validation and test fractions                                                                                                                                                                              
validation_fraction = 0.4
test_fraction = 0.2

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)

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

booster = xgb.train( model_parameters, training_matrix, 4000 )

model_name = 'model_jetkins_4000trees'
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


###
# Get some evaluation metrics
###

model_name = 'model_jetkins_4000trees' 
number_of_threads = 1

#load trained classifier 
model = xgb.Booster()
model.load_model( model_name + '.bin' )

#make xgboost DMatrices for predictions 
signal_training_matrix = xgb.DMatrix( signal_collection.training_set.samples, label = signal_collection.training_set.labels, nthread = number_of_threads)
signal_validation_matrix = xgb.DMatrix( signal_collection.validation_set.samples, label = signal_collection.validation_set.labels, nthread = number_of_threads)

background_training_matrix = xgb.DMatrix( background_collection.training_set.samples, label = background_collection.training_set.labels, nthread = number_of_threads)
background_validation_matrix = xgb.DMatrix( background_collection.validation_set.samples, label = background_collection.validation_set.labels, nthread = number_of_threads)

#make predictions 
signal_collection.training_set.addOutputs( model.predict( signal_training_matrix ) )
signal_collection.validation_set.addOutputs( model.predict( signal_validation_matrix ) )

background_collection.training_set.addOutputs( model.predict( background_training_matrix ) )
background_collection.validation_set.addOutputs( model.predict( background_validation_matrix ) )

# get evaluation metrics

plotROCAndShapeComparison(signal_collection, background_collection, model_name )
