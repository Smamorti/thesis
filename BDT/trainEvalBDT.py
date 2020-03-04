from diagnosticPlotting import *
import xgboost as xgb

def trainBDT( train_data, train_labels, train_weights = None, feature_names = None, model_name = 'model', number_of_trees = 100, learning_rate = 0.1,  max_depth = 2, min_child_weight = 1, subsample = 0.5, colsample_bytree = 1, gamma = 0, alpha = 0, number_of_threads = 1):
    
    #convert training data to dmatrix
    training_matrix = xgb.DMatrix( train_data, weight = train_weights, label = train_labels, nthread = number_of_threads, feature_names = feature_names )
    
    model_parameters = {
        'learning_rate' : learning_rate,
        'max_depth' : max_depth,
        'min_child_weight' : min_child_weight,
        'subsample' : subsample,
        'colsample_bytree' : colsample_bytree,
        'gamma' : gamma,
        'alpha' : alpha,
        'nthread' : number_of_threads
    }

    booster = xgb.train( model_parameters, training_matrix, number_of_trees )

    booster.save_model( 'models/' + model_name + '.bin' )

    #plot feature importance                                                                                                                                                                                    
    xgb.plot_importance( booster )
    plt.gcf().subplots_adjust( left = 0.22 )
    plt.xlabel( 'Number of splittings', fontsize = 16 )
    plt.ylabel( 'Feature', fontsize = 16 )
    plt.savefig( 'results/feature_importance_' + model_name + '.pdf' )
    plt.savefig( 'results/feature_importance_' + model_name + '.png' )
    plt.clf()

    #reset the figure margins for future plots                                                                                                                                                                  
    plt.gcf().subplots_adjust( left = 0.125 )

def evalBDT(model_name, signal_collection, background_collection):
     
    number_of_threads = 1

    #load trained classifier                                                                                                                                                                                    
    model = xgb.Booster()
    model.load_model( 'models/' + model_name + '.bin' )

    #make xgboost DMatrices for predictions                                                                                                                                                                     
    signal_training_matrix = xgb.DMatrix( signal_collection.training_set.samples, label = signal_collection.training_set.labels, nthread = number_of_threads)
    signal_validation_matrix = xgb.DMatrix( signal_collection.validation_set.samples, label = signal_collection.validation_set.labels, nthread = number_of_threads)
    signal_test_matrix = xgb.DMatrix( signal_collection.test_set.samples, label = signal_collection.test_set.labels, nthread = number_of_threads)

    background_training_matrix = xgb.DMatrix( background_collection.training_set.samples, label = background_collection.training_set.labels, nthread = number_of_threads)
    background_validation_matrix = xgb.DMatrix( background_collection.validation_set.samples, label = background_collection.validation_set.labels, nthread = number_of_threads)
    background_test_matrix = xgb.DMatrix( background_collection.test_set.samples, label = background_collection.test_set.labels, nthread = number_of_threads)

    #make predictions                                                                                                                                                                                           
    signal_collection.training_set.addOutputs( model.predict( signal_training_matrix ) )
    signal_collection.validation_set.addOutputs( model.predict( signal_validation_matrix ) )
    signal_collection.test_set.addOutputs( model.predict( signal_test_matrix ) )

    background_collection.training_set.addOutputs( model.predict( background_training_matrix ) )
    background_collection.validation_set.addOutputs( model.predict( background_validation_matrix ) )
    background_collection.test_set.addOutputs( model.predict( background_test_matrix ) )

    # get evaluation metrics                                                                                                                                                                               

    plotROCAndShapeComparison(signal_collection, background_collection, model_name )
    plotROCAndShapeComparison_test(signal_collection, background_collection, model_name + '_test' )


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

def plotROCAndShapeComparison_test(signal_collection, background_collection, model_name ):
    rocAndAUC( signal_collection.test_set, background_collection.test_set, model_name )
    compareOutputShapes(
        signal_collection.training_set,
        signal_collection.test_set,
        background_collection.training_set,
        background_collection.test_set,
        model_name
    )
