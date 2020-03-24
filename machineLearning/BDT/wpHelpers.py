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

def purityAndEfficiency(model_name, signal_collection, background_collection):

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
    sOsqrtSB = []
    # loop over a set number of points within the range of min and max BDT output to make purity and efficiency curves

    model_outputs = np.linspace(min_output, max_output, 10000)

    for model_output in model_outputs[:-1]: #skip last value, would be division by zero

        # for this given model output value, calculate purity and efficiency

        signal_selected = (signal_outputs > model_output)
        background_selected = (background_outputs > model_output)
        background_notSelected = np.invert(background_selected)

        n_sel_sign = np.sum(signal_weights[signal_selected])
        n_sel_bkg = np.sum(background_weights[background_selected])
        n_notSel_bkg = np.sum(background_weights[background_notSelected])

        p = n_sel_sign / (n_sel_sign + n_sel_bkg)
        purity.append(p)

        eps = n_sel_sign / n_all_sign
        efficiency.append(eps)

        temp = n_sel_sign / np.sqrt((n_sel_sign + n_sel_bkg))
        sOsqrtSB.append(temp)

        # if n_notSel_bkg == 0:

        #     print(0)
        #     print(np.where(model_outputs == model_output))
        # elif model_output > 0:

        #     ratio = n_sel_sign / np.sqrt(n_notSel_bkg)
        #     sbr.append(ratio)

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
    sOsqrtSB.append(0)

    # plot purity and efficiency, as well as their product

    purity = np.array(purity)
    efficiency = np.array(efficiency)

    # purity

    plt.plot(model_outputs, purity, 'b', lw=2)
    plt.ylabel('Purity')
    plt.xlabel('Model Output')

    plt.grid(True)

    plt.savefig('results/purity_' + model_name + '.pdf')
    plt.savefig('results/purity_' + model_name + '.png')

    plt.clf()

    # efficiency

    plt.plot(model_outputs, efficiency, 'b', lw=2)
    plt.ylabel('Efficiency')
    plt.xlabel('Model Output')

    plt.grid(True)

    plt.savefig('results/efficiency_' + model_name + '.pdf')
    plt.savefig('results/efficiency_' + model_name + '.png')
    
    plt.clf()

    # purity * efficiency

    plt.plot(model_outputs, purity*efficiency, 'b', lw=2)
    plt.ylabel('Purity*Efficiency')
    plt.xlabel('Model Output')

    plt.grid(True)

    plt.savefig('results/purityXefficiency_' + model_name + '.pdf')
    plt.savefig('results/purityXefficiency_' + model_name + '.png')
    
    plt.clf()

    # signal / sqrt(bkg)
    
    plt.plot(model_outputs[:len(sbr)], sbr, 'b', lw=2)
    plt.ylabel('Signal / Sqrt(Background)')
    plt.xlabel('Model Output')
    plt.grid(True)

    plt.savefig('results/signalSqrtBkgRatio_' + model_name + '.pdf')
    plt.savefig('results/signalSqrtBkgRatio_' + model_name + '.png')

    plt.clf()

    # signal / sqrt(bkg + signal)                                                                                                                                                                                                                    
    plt.plot(model_outputs[:len(ssbr)], ssbr, 'b', lw=2)
    plt.ylabel('Signal / Sqrt(Background + Signal)')
    plt.xlabel('Model Output')
 
    plt.grid(True)

    plt.savefig('results/signalSqrtBkg+SignRatio_' + model_name + '.pdf')
    plt.savefig('results/signalSqrtBkg+SignRatio_' + model_name + '.png')

    plt.clf()

    # purity + signal / sqrt(bkg)                                                                                                                                                                                                         
                                  
    maximum_index = np.argmax(purXeff_sbr)

    plt.axvline(model_outputs[maximum_index], color = 'red', label = 'Maximal for model output {}'.format(model_outputs[maximum_index]))
                                                                                                                                                                                                       
    plt.plot(model_outputs[:len(purXeff_sbr)], purXeff_sbr, 'b', lw=2)
    plt.ylabel('Purity*Efficiency + Signal/sqrt(bkg)')
    plt.xlabel('Model Output')
    plt.legend(loc = 'lower left')
    plt.grid(True)

    plt.savefig('results/purXeff_sbr_' + model_name + '.pdf')
    plt.savefig('results/purXeff_sbr_' + model_name + '.png')

    plt.clf()



    # purityXeff and sign/sqrt(bkg)

    plt.plot(model_outputs[:len(sbr)], sbr, 'b', lw=2, label = 'Signal/sqrt(bkg)')
    plt.plot(model_outputs, purity*efficiency, 'red', lw=2, label = 'PurityXEfficiency')
#plt.ylabel('')
    plt.xlabel('Model Output')
    plt.legend()
    plt.grid(True)

    plt.savefig('results/purANDsbr_' + model_name + '.pdf')
    plt.savefig('results/purANDsbr_' + model_name + '.png')

    plt.clf()


    # purityXeff and sign/sqrt(bkg) (scaled)                                                                                                                                                                                                      
    print(np.amax(purity*efficiency) / np.amax(sbr))
    scaling = np.amax(purity*efficiency) / np.amax(sbr)
    new = np.multiply(sbr, scaling)
    plt.plot(model_outputs[:len(sbr)], new, 'b', lw=2, label = 'Signal/sqrt(bkg)')
    plt.plot(model_outputs, purity*efficiency, 'red', lw=2, label = 'PurityXEfficiency')

    plt.xlabel('Model Output')
    plt.legend(loc = 'lower left')
    plt.grid(True)

    plt.savefig('results/purANDsbr_Scaled_' + model_name + '.pdf')
    plt.savefig('results/purANDsbr_Scaled_' + model_name + '.png')

    plt.clf()

    # purity + signal / sqrt(bkg)  (scaled)                                                                                                                                                                                                    
    summed = new + (purity*efficiency)[:len(new)]

    maximum_index = np.argmax(summed)

    plt.axvline(model_outputs[maximum_index], color = 'red', label = 'Maximal for model output {}'.format(model_outputs[maximum_index]))
    
    plt.title(r'Purity*Efficiency + Signal/$\sqrt{bkg}$ (scaled)')

    plt.plot(model_outputs[:len(summed)], summed, 'b', lw=2)
    plt.ylabel(r'Purity*Efficiency + Signal/$\sqrt{bkg}$')
    plt.xlabel('Model Output')
    plt.legend(loc = 'lower left')
    plt.grid(True)

    plt.savefig('results/purXeff_sbr_Scaled' + model_name + '.pdf')
    plt.savefig('results/purXeff_sbr_Scaled' + model_name + '.png')

    plt.clf()

    # signal / sqrt(signal+bkg)                                                                                                                                                                                                                               

    plt.plot(model_outputs, sOsqrtSB, 'b', lw=2)
    plt.ylabel(r'Signal/$\sqrt{(signal+bkg)}$')
    plt.xlabel('Model Output')

    plt.grid(True)

    plt.savefig('results/sOsqrtSB_' + model_name + '.pdf')
    plt.savefig('results/sOsqrtSB_' + model_name + '.png')

    plt.clf()
