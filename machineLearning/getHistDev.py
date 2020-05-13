from ROOT import TFile
from DataCollection import DataCollection
from Dataset import concatenateAndShuffleDatasets
from trainNN import trainNN
import numpy as np
from trainEvalBDT import plotROCAndShapeComparison_NN, plotROCAndShapeComparison_test, getDifBins
import json
import sys
from keras.models import load_model
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

# input_file_path = sys.argv[1]
# epochs = int(sys.argv[2])

# parameter_dict = {}
# with open( input_file_path ) as f:
#     parameter_dict = json.load( f )

# configuration = parameter_dict
# configuration['input_shape'] = ( len(branch_names), )
# configuration['number_of_threads'] = 1


# #configuration['number_of_epochs'] = 200
# configuration['number_of_epochs'] = epochs


inputFile = TFile("../newTrees/reducedTrees/goodTreesTotal/trees_total_2018_nominal.root")

signalTree = inputFile.Get("tree_signal_2018")
bkgTree = inputFile.Get("tree_background_2018")

#validation and test fractions                                                                                                                                                                              
validation_fraction = 0.0
test_fraction = 0.2

# ensure reproducibility

np.random.seed(42)

signal_collection = DataCollection(signalTree, branch_names, validation_fraction, test_fraction, True, 'weight', only_positive_weights = True)
background_collection = DataCollection(bkgTree, branch_names, validation_fraction, test_fraction, False, 'weight', only_positive_weights = True)

training_data = concatenateAndShuffleDatasets(signal_collection.training_set, background_collection.training_set)
validation_data = concatenateAndShuffleDatasets(signal_collection.validation_set, background_collection.validation_set)
test_data = concatenateAndShuffleDatasets(signal_collection.test_set, background_collection.test_set)

#model_name = 'NN_Best_FullData_18epochs'
#model_name = 'NN_final_80_0_20_18epochs_v3'
#model_name = 'NN_gen39_1_80_0_20_{}epochs'.format(epochs)

#trainNN(model_name, configuration, training_data, validation_data, test_data, validation_fraction, signal_collection, background_collection)

totSum = np.zeros(20)
highSum = np.zeros(20)
#totSum = np.zeros((20, 6))
#highSum = np.zeros((20,6))


epochs = range(5, 25)
j = 'final'
for i in epochs:

#    for j in range(1, 7):

 #       print(i, j)

    model_name = 'NN_{}_8020_{}epochs'.format(j, i)
    model = load_model( model_name + '.h5' )

    signal_collection.training_set.addOutputs( model.predict( signal_collection.training_set.samples ) )
    signal_collection.validation_set.addOutputs( model.predict( signal_collection.validation_set.samples ) )
    signal_collection.test_set.addOutputs( model.predict( signal_collection.test_set.samples ) )

    background_collection.training_set.addOutputs( model.predict( background_collection.training_set.samples ) )
    background_collection.validation_set.addOutputs( model.predict( background_collection.validation_set.samples))
    background_collection.test_set.addOutputs( model.predict( background_collection.test_set.samples ) )



    if validation_fraction == 0:

#          plotROCAndShapeComparison_test(signal_collection, background_collection, model_name )

        sumAll, sumHigh = getDifBins(signal_collection, background_collection, model_name )

        totSum[i-5] = sumAll
        highSum[i-5] = sumHigh
        # totSum[i-5][j-1] = sumAll
        # highSum[i-5][j-1] = sumHigh

#           print(totSum)
#            print(highSum)


    else:

        plotROCAndShapeComparison_NN(signal_collection, background_collection, model_name, validation_fraction+test_fraction )


np.save('totsum.npy', totSum)
np.save('highsum.npy', highSum)
