#prevent matplotlib from using xwindows which is not available when submitting jobs to worker nodes 
import matplotlib
matplotlib.use('Agg')

#import necessary libraries 
import matplotlib.pyplot as plt
import numpy as np
import xgboost as xgb
from keras.models import load_model

def makeOutputNN(model_name, signal_collection, background_collection):

    #load trained classifier                                                                                                                                                   \                                                            
    model = load_model( 'models/' + model_name + '.h5' )
#    model.summary()

    #make predictions                                                                                                                                                          \                                                            
    signal_collection.training_set.addOutputs( model.predict( signal_collection.training_set.samples ) )
 #   print(signal_collection.training_set.outputs)
    signal_collection.validation_set.addOutputs( model.predict( signal_collection.validation_set.samples ) )
    signal_collection.test_set.addOutputs( model.predict( signal_collection.test_set.samples ) )

    background_collection.training_set.addOutputs( model.predict( background_collection.training_set.samples ) )
    background_collection.validation_set.addOutputs( model.predict( background_collection.validation_set.samples ) )
    background_collection.test_set.addOutputs( model.predict( background_collection.test_set.samples ) )
    
def makeOutputBDT(model_name, signal_collection, background_collection):

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

def wpMetrics(model_name, signal_collection, background_collection, algo):

    signal_outputs = signal_collection.training_set.outputs
    signal_weights = signal_collection.training_set.weights
    background_outputs = background_collection.training_set.outputs
    background_weights = background_collection.training_set.weights

    min_output = min( np.min(signal_outputs), np.min(background_outputs) )
    max_output = max( np.max(signal_outputs), np.max(background_outputs) )

    n_all_sign = np.sum(signal_weights)

    purity = []
    efficiency = []
    sbr = []
    ssbr = []
    purXeff_sbr = []

    # loop over a set number of points within the range of min and max BDT output to make purity and efficiency curves

    model_outputs = np.linspace(min_output, max_output, 10000)

    for model_output in model_outputs[:-1]: #skip last value, would be division by zero

        # for this given model output value, calculate purity and efficiency

        signal_selected = signal_outputs > model_output
        background_selected = (background_outputs > model_output)
        background_notSelected = np.invert(background_selected)

        try:

            n_sel_sign = np.sum(signal_weights[signal_selected])
            n_sel_bkg = np.sum(background_weights[background_selected])
            n_notSel_bkg = np.sum(background_weights[background_notSelected])

        except IndexError:

            
            signal_selected = np.reshape(signal_selected, (signal_selected.shape[0],))
            background_selected = np.reshape(background_selected, (background_selected.shape[0],))
            background_notSelected = np.reshape(background_notSelected, (background_notSelected.shape[0],))
            
            n_sel_sign = np.sum(signal_weights[signal_selected])
            n_sel_bkg = np.sum(background_weights[background_selected])
            n_notSel_bkg = np.sum(background_weights[background_notSelected])
            

        p = n_sel_sign / (n_sel_sign + n_sel_bkg)
        purity.append(p)

        eps = n_sel_sign / n_all_sign
        efficiency.append(eps)

        if n_sel_bkg != 0:

            ratio = n_sel_sign / np.sqrt(n_sel_bkg)
            sbr.append(ratio)

            purXeff_sbr.append(p*eps+ratio)

        if n_sel_bkg + n_sel_sign != 0:

            ratio = n_sel_sign / np.sqrt(n_sel_bkg + n_sel_sign)
            ssbr.append(ratio)

    # add values for maximum value of model output --> 0

    purity.append(0)
    efficiency.append(0)
    sbr.append(0)

    # prepare arrays for plotting

    purity = np.array(purity)
    efficiency = np.array(efficiency)

    scaling = np.amax(purity*efficiency) / np.amax(sbr)
    new = np.multiply(sbr, scaling)

    summed = new + (purity*efficiency)[:len(new)]

    maximum_index = np.argmax(summed)

    # purityXeff and sign/sqrt(bkg) (scaled) and sum        

    plotTotal(model_outputs, maximum_index, purity, efficiency, summed, sbr, new, algo)

    plt.xlabel('Model Output')
    plt.legend(loc = 'best', prop={'size': 10})
    plt.grid(True)

    plt.savefig('results/total_' + model_name + '.pdf')
    plt.savefig('results/total_' + model_name + '.png')

    plt.clf()

    # purity

    plotPurity(model_outputs, maximum_index, purity, algo)

    plt.ylabel('Purity')
    plt.xlabel('Model Output')

    plt.grid(True)

    plt.savefig('results/purity_' + model_name + '.pdf')
    plt.savefig('results/purity_' + model_name + '.png')

    plt.clf()

    # efficiency

    plotEfficiency(model_outputs, maximum_index, efficiency, algo)

    plt.ylabel('Efficiency')
    plt.xlabel('Model Output')

    plt.grid(True)

    plt.savefig('results/efficiency_' + model_name + '.pdf')
    plt.savefig('results/efficiency_' + model_name + '.png')
    
    plt.clf()

    # signal / sqrt(bkg)

    plotSbr(model_outputs, maximum_index, sbr, algo)

    plt.ylabel('Signal / Sqrt(Background)')
    plt.xlabel('Model Output')
    plt.grid(True)

    plt.savefig('results/signalSqrtBkgRatio_' + model_name + '.pdf')
    plt.savefig('results/signalSqrtBkgRatio_' + model_name + '.png')

    plt.clf()

    return {'purity': purity, 'efficiency': efficiency, 'sbr': sbr, 'summed' : summed, 'model_outputs': model_outputs, 'maximum_index' : maximum_index, 'sbr_scaled' : new}

def plotEfficiency(model_outputs, maximum_index, efficiency, algo, color = 'b', vlineColor = 'red'):

    plt.axvline(str(model_outputs[maximum_index])[:4], color = vlineColor, label = '{} Maximum at {}'.format(algo, str(model_outputs[maximum_index])[:4]))
    plt.plot(model_outputs, efficiency, color = color, lw=2, label = algo)

def plotPurity(model_outputs, maximum_index, purity, algo, color = 'b', vlineColor = 'red'):

    plt.axvline(str(model_outputs[maximum_index])[:4], color = vlineColor, label = '{} Maximum at {}'.format(algo, str(model_outputs[maximum_index])[:4]))
    plt.plot(model_outputs, purity, color = color, lw=2, label = algo)

def plotSbr(model_outputs, maximum_index, sbr, algo, color = 'b', vlineColor = 'red'):

    plt.axvline(str(model_outputs[maximum_index])[:4], color = vlineColor, label = '{} Maximum at {}'.format(algo, str(model_outputs[maximum_index])[:4]))
    plt.plot(model_outputs[:len(sbr)], sbr, color = color, lw=2, label = algo)


def plotTotal(model_outputs, maximum_index, purity, efficiency, summed, sbr, sbr_scaled, algo, style = '-'):

    plt.axvline(model_outputs[maximum_index], color = 'gold' , linestyle = style, label = '{} Maximum at {}'.format(algo, str(model_outputs[maximum_index])[:4]))
    plt.plot(model_outputs[:len(sbr)], sbr_scaled, 'b', linestyle = style,  lw=2, label = r'Signal/$\sqrt{bkg}$'+' ({})'.format(algo)) 
    plt.plot(model_outputs, purity*efficiency, 'red', linestyle = style, lw=2, label = r'Purity$\cdot$Efficiency ({})'.format(algo))
    plt.plot(model_outputs[:len(summed)], summed, 'green', linestyle = style, lw=2, label = r'Sum ({})'.format(algo))
    

def BDTandNN(BDT, NN):

    # purity plot

    plotPurity(NN['model_outputs'], NN['maximum_index'], NN['purity'], 'NN', color = 'b')
    plotPurity(BDT['model_outputs'], BDT['maximum_index'], BDT['purity'], 'BDT', color = 'green', vlineColor = 'gold')
    
    plt.ylabel('Purity')
    plt.xlabel('Model Output')
    plt.legend(loc = 'best', prop={'size': 10})
    plt.grid(True)

    plt.savefig('results/purity_comparison.pdf')
    plt.savefig('results/purity_comparison.png')

    plt.clf()

    # efficiency plot

    plotEfficiency(NN['model_outputs'], NN['maximum_index'], NN['efficiency'], 'NN', color = 'b')
    plotEfficiency(BDT['model_outputs'], BDT['maximum_index'], BDT['efficiency'], 'BDT', color = 'green', vlineColor = 'gold')
    
    plt.ylabel('Efficiency')
    plt.xlabel('Model Output')
    plt.legend(loc = 'best', prop={'size': 10})
    plt.grid(True)

    plt.savefig('results/efficiency_comparison.pdf')
    plt.savefig('results/efficiency_comparison.png')

    plt.clf()


    # sbr plot

    plotSbr(NN['model_outputs'], NN['maximum_index'], NN['sbr'], 'NN', color = 'b')
    plotSbr(BDT['model_outputs'], BDT['maximum_index'], BDT['sbr'], 'BDT', color = 'green', vlineColor = 'gold')
   
    plt.ylabel('Signal / Sqrt(Background)')
    plt.xlabel('Model Output')
    plt.legend(loc = 'best', prop={'size': 10})
    plt.grid(True)

    plt.savefig('results/sbr_comparison.pdf')
    plt.savefig('results/sbr_comparison.png')

    plt.clf()


    # total plot
    
    plotTotal(NN['model_outputs'], NN['maximum_index'], NN['purity'], NN['efficiency'], NN['summed'], NN['sbr'], NN['sbr_scaled'], 'NN', '--')
    plotTotal(BDT['model_outputs'], BDT['maximum_index'], BDT['purity'], BDT['efficiency'], BDT['summed'], BDT['sbr'], BDT['sbr_scaled'], 'BDT', '-')
    
    plt.xlabel('Model Output')
    plt.legend(loc = 'best', prop={'size': 10})
    plt.grid(True)

    plt.savefig('results/total_comparison'  + '.pdf')
    plt.savefig('results/total_comparison'  + '.png')

    plt.clf()
