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
    'jetPt5', 'jetEta5', 'jetPhi5'
    ]   



                                                                                                                                                          
#branch that indicates the event weights 
#weight_branch = 'weight'
weight_branch = 'weight'

#use only positive weights in training or not 
only_positive_weights = True

#validation and test fractions
validation_fraction = 0.4
test_fraction = 0.2

#number of threads to use when training
number_of_threads = 1

#try to fix the error regarding signal_parameters

signal_parameters = None
parameter_shortcut_connection = None # is this necessary?


#use genetic algorithm or grid-scan for optimization
use_genetic_algorithm = True
high_memory = False

if use_genetic_algorithm:

    population_size = 500

    #ranges of neural network parameters for the genetic algorithm to scan
    parameter_ranges = {
        'number_of_trees' : list( range(100, 10000) ),
		'learning_rate' : (0.001, 1),
		'max_depth' : list(range(2, 10) ),
		'min_child_weight' : (1, 20),
		'subsample' : (0.1, 1),
		'colsample_bytree' : (0.5, 1),
		'gamma' : (0, 1),
		'alpha' : (0, 1)
	}

else:
    parameter_values = {
        'number_of_trees' : [500, 1000, 2000, 4000, 8000],
        	'learning_rate' : [0.01, 0.05, 0.1, 0.2, 0.5],
        	'max_depth' : [2, 3, 4, 5, 6],
        	'min_child_weight' : [1, 5, 10],
        	'subsample' : [1],
        	'colsample_bytree' : [0.5, 1],
        	'gamma' : [0],
        	'alpha' : [0]
        }
    # parameter_values = {
    #     'number_of_trees' : [500],#, 1000, 2000, 4000, 8000],
    #     	'learning_rate' : [0.05],#, 0.01, 0.1, 0.2, 0.5],
    #     	'max_depth' : [2, 3, 4, 5, 6],
    #     	'min_child_weight' : [1],#, 5, 10],
    #     	'subsample' : [1],
    #     	'colsample_bytree' : [0.5],#, 1],
    #     	'gamma' : [0],
    #     	'alpha' : [0]
    #     }
