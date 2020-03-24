#name of input root file, relative to the directory of this script                                                                                                         
root_file_name = '../thesis/newTrees/reducedTrees/goodTreesTotal/trees_total_2018.root'

#names of trees that contain signal and background events                                                                                                                                                
signal_tree_name = 'tree_signal_total'
background_tree_name = 'tree_background_total'

#list of variables to be used in training (corresponding to branches in the tree)
list_of_branches = [
    'lPt1', 'lPt2',
    'lEta1', 'lEta2',
    'lPhi1', 'lPhi2',
    'DeltaR_1', 'DeltaR_b1', 'DeltaR_2', 'DeltaR_b2',
    'njets', 'nbjets', 'jetDeepCsv_b1',
    'mW1', 'mtop1',
    'jetPt1', 'jetEta1', 'jetPhi1',
    'jetPt2', 'jetEta2', 'jetPhi2',
    'jetPt3', 'jetEta3', 'jetPhi3',
    'jetPt4', 'jetEta4', 'jetPhi4',
    'jetPt5', 'jetEta5', 'jetPhi5',
    'MET', 'H_t',
    'I_rel1', 'I_rel2'
    ]

#branch that indicates the event weights 
weight_branch = 'weight'

#use only positive weights in training or not 
only_positive_weights = True

#validation and test fractions
validation_fraction = 0.2
test_fraction = 0.0

#try to fix the error regarding signal_parameters                                                                                                                       

signal_parameters = None
parameter_shortcut_connection = None # is this necessary?                                                                                                                               

#use genetic algorithm or grid-scan for optimization
use_genetic_algorithm = False

number_of_threads = 1
high_memory = False

if use_genetic_algorithm:

    population_size = 200

    #ranges of neural network parameters for the genetic algorithm to scan
    #This is just an example, for real use cases it is probably best to reduce the amount of options!

    parameter_ranges = {
        'number_of_hidden_layers' : [2, 3, 4, 5, 6, 7, 8, 9, 10],
        'units_per_layer' : list( range(16, 1024) ),
        'optimizer' : ['RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam'],
        'activation' : [ 'prelu', 'selu', 'leakyrelu', 'relu' ],
        'learning_rate' : (0.01, 1),
        'learning_rate_decay' : (0.9, 1),
        'dropout_first' : (False, True),
        'dropout_all' : (False, True),
        'dropout_rate' : (0, 0.5),
        'batchnorm_first' : (False, True),
        'batchnorm_hidden' : (False, True),
        'batchnorm_before_activation' : (False, True),
        'number_of_epochs' : [200],
        'batch_size' : list( range( 32, 512 ) )
    }


else:
    
    #all parameter values to be covered by the grid-scan. Redundant configurations are automatically removed.
    #This is just an example, for real use cases one has to reduce the amount of options!
    # parameter_values = {
    #     'num_hidden_layers' : [2, 3, 4, 5, 6, 7, 8, 9, 10],
    #     'units_per_layer' : [16, 32, 64, 128, 256, 512],
    #     'optimizer' : ['Nadam'],
    #     'actviation' : [ 'prelu', 'selu', 'leakyrelu', 'relu' ],
    #     'learning_rate' : [0.1, 1, 0.01],
    #     'learning_rate_decay' : [1, 0.99, 0.95],
    #     'dropout_first' : [False, True],
    #     'dropout_all' : [False, True],
    #     'dropout_rate' : [0.5, 0.3],
    #     'batchnorm_first' : [False, True],
    #     'batchnorm_hidden' : [False, True],
    #     'batchnorm_before_activation' : [False, True],
    #     'number_of_epochs' : [200],
    #     'batch_size' : [256, 512]
    # }
    parameter_values = {
        'number_of_hidden_layers' : [2],
        'units_per_layer' : [16],
        'optimizer' : ['Nadam'],
        'activation' : [ 'prelu', 'selu', 'leakyrelu', 'relu', 'relu'],
        'learning_rate' : [0.1],
        'learning_rate_decay' : [1],
        'dropout_first' : [True],
        'dropout_all' : [True],
        'dropout_rate' : [0.3],
        'batchnorm_first' : [True],
        'batchnorm_hidden' : [True],
        'batchnorm_before_activation' : [True],
        'number_of_epochs' : [200],
        'batch_size' : [256]
    }
