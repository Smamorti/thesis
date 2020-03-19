#prevent matplotlib from using xwindows which is not available when submitting jobs to worker nodes 
import matplotlib
matplotlib.use('Agg')

#import necessary libraries 
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb

    
def makeOutput(model_name, signal_collection, background_collection):

    number_of_threads = 1

    #load trained classifier                                                                                                                                                   \
                                                                                                                                                                                
    model = xgb.Booster()
    model.load_model( 'models/' + model_name + '.bin' )

    #make xgboost DMatrices for predictions                                                                                                                                    \
                                                                                                                                                                                
    signal_training_matrix = xgb.DMatrix( signal_collection.training_set.samples, label = signal_collection.training_set.labels, nthread = number_of_threads)
    signal_validation_matrix = xgb.DMatrix( signal_collection.validation_set.samples, label = signal_collection.validation_set.labels, nthread = number_of_threads)
    signal_test_matrix = xgb.DMatrix( signal_collection.test_set.samples, label = signal_collection.test_set.labels, nthread = number_of_threads)

    background_training_matrix = xgb.DMatrix( background_collection.training_set.samples, label = background_collection.training_set.labels, nthread = number_of_threads)
    background_validation_matrix = xgb.DMatrix( background_collection.validation_set.samples, label = background_collection.validation_set.labels, nthread = number_of_threads)
    background_test_matrix = xgb.DMatrix( background_collection.test_set.samples, label = background_collection.test_set.labels, nthread = number_of_threads)

    #make predictions                                                                                                                                                          \
                                                                                                                                                                                
    signal_collection.training_set.addOutputs( model.predict( signal_training_matrix ) )
    signal_collection.validation_set.addOutputs( model.predict( signal_validation_matrix ) )
    signal_collection.test_set.addOutputs( model.predict( signal_test_matrix ) )

    background_collection.training_set.addOutputs( model.predict( background_training_matrix ) )
    background_collection.validation_set.addOutputs( model.predict( background_validation_matrix ) )
    background_collection.test_set.addOutputs( model.predict( background_test_matrix ) )


def plotOutputShapeComparison( outputs_signal_training, weights_signal_training, 
    outputs_background_training, weights_background_training, 
    outputs_signal_testing, weights_signal_testing, 
    outputs_background_testing, weights_background_testing,
    model_name
    ):

    min_output = min( np.min(outputs_signal_training), np.min(outputs_background_training), np.min(outputs_signal_testing), np.min(outputs_background_testing ) )
    max_output = max( np.max(outputs_signal_training), np.max(outputs_background_training), np.max(outputs_signal_testing), np.max(outputs_background_testing ) )
    
    addHist( outputs_background_training, weights_background_training, 30, min_output, max_output, 'Background (training set)', color='red')
    addHist( outputs_background_testing, weights_background_testing, 30, min_output, max_output, 'Background (validation set)', color = 'purple')
    addHist( outputs_signal_training, weights_signal_training, 30, min_output, max_output, 'Signal (training set)', color='blue')
    addHist( outputs_signal_testing, weights_signal_testing, 30, min_output, max_output, 'Signal (validation set)', color='green')

    plt.xlabel( 'Model output', fontsize = 16 )
    plt.ylabel( 'Normalized events', fontsize = 16 )
    plt.legend(ncol=2, prop={'size': 10})

    bottom, top = plt.ylim()
    plt.ylim( 0,  top*1.2)
    plt.savefig('shapeComparison_' + model_name + '.pdf')

    print("Saved figure with name {}".format('shapeComparison_' + model_name + '.pdf'))

    plt.clf()
    
def plotSearchWP( outputs_signal_training, weights_signal_training,
    outputs_background_training, weights_background_training,
    outputs_signal_testing, weights_signal_testing,
    outputs_background_testing, weights_background_testing,
    model_name
    ):

    nbins = 30
    signalPercentage = 0.80

    min_output = min( np.min(outputs_signal_training), np.min(outputs_background_training), np.min(outputs_signal_testing), np.min(outputs_background_testing ) )
    max_output = max( np.max(outputs_signal_training), np.max(outputs_background_training), np.max(outputs_signal_testing), np.max(outputs_background_testing ) )


    x = np.linspace(min_output, max_output, 1000)
    y = [signalPercentage for _ in x]
    plt.plot(x, y, label = 'cumulated events = {}'.format(signalPercentage), color = 'fuchsia')
    

    n, bins = addHist( outputs_background_training, weights_background_training, nbins, min_output, max_output, 'Background (training set)', color='red', cumulative = -1)
    n, bins = addHist( outputs_background_testing, weights_background_testing, nbins, min_output, max_output, 'Background (test set)', color = 'purple', cumulative = -1)
    n, bins = addHist( outputs_signal_training, weights_signal_training, nbins, min_output, max_output, 'Signal (training set)', color='blue', cumulative = -1)
    n, bins = addHist( outputs_signal_testing, weights_signal_testing, nbins, min_output, max_output, 'Signal (test set)', color='green', cumulative = -1)

    i = 0

    while n[i] > signalPercentage:
        i += 1
        
    plt.axvline(x=0.5 * ( bins[i] + bins[i+1] ), label = "{}% point at x={}".format(80, 0.5 * ( bins[i] + bins[i+1] )), color = 'orange')


    plt.xlabel( 'Model output', fontsize = 16 )
    plt.ylabel( 'Normalized events', fontsize = 16 )


    plt.legend(ncol=2, prop={'size': 10})
    bottom, top = plt.ylim()
    plt.ylim( 0,  top*1.2)
    plt.savefig('cumulative_' + model_name + '.pdf')

    print("Saved figure with name {}".format('cumulative_' + model_name + '.pdf'))

    plt.clf()


def binWidth(num_bins, min_bin, max_bin):
    return float( max_bin - min_bin) / num_bins


def addHist( data, weights, num_bins, min_bin, max_bin, label, color = 'blue', cumulative = False):
    bin_width = binWidth( num_bins, min_bin, max_bin )
    n, bins, _ = plt.hist(data, bins=num_bins, range=(min_bin, max_bin), weights = weights/np.sum(weights), label = label, histtype='step', lw=2, color=color, cumulative = cumulative)
    bin_errors = errors( data, weights, num_bins, min_bin, max_bin)
    bin_centers = 0.5*(bins[1:] + bins[:-1]) 
    plt.errorbar(bin_centers, n, yerr=bin_errors, fmt='none', ecolor=color)

    return n, bins


def errors( data, weights, num_bins, min_bin, max_bin ):
    bin_errors = np.zeros( num_bins )
    bin_width = binWidth( num_bins, min_bin, max_bin )
    for i, entry in enumerate(data):
        bin_number = int( (entry - min_bin) // bin_width )
        if bin_number == num_bins :
            bin_number = num_bins - 1
        weight_entry =  weights[i]
        bin_errors[bin_number] += weight_entry*weight_entry
    bin_errors = (bin_errors ** 0.5)
    scale = np.sum(weights)
    bin_errors /= scale
    return bin_errors 
