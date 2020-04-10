import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

def plot(algo, style, wp, sign, bkg):

    sign = np.array(sign)
    bkg = np.array(bkg)

    tot = sign + bkg
    
    plt.plot(wp, sign, linestyle = style, color = 'red', label = 'signal ({})'.format(algo))
    plt.plot(wp, bkg, linestyle = style, color = 'blue', label = 'background ({})'.format(algo))
    plt.plot(wp, tot, linestyle = style, color = 'purple', label = 'total ({})'.format(algo))

    bkg_nonzero = bkg > 0
    bkg = bkg[bkg_nonzero]

    ratio = sign[:len(bkg)] / bkg

    plt.plot(wp[:len(bkg)], ratio, linestyle = style, color = 'green', label = 'sign/bkg ({})'.format(algo))
    

def plotSignalBkgWRTwp(NN_signal_output, NN_signal_weight, NN_background_output, NN_background_weight, BDT_signal_output, BDT_signal_weight, BDT_background_output, BDT_background_weight):

    NN_signal_output = np.resize(NN_signal_output, (NN_signal_output.shape[0], ))
    NN_background_output = np.resize(NN_background_output, (NN_background_output.shape[0], ))
    
    points = 1000

    min_nn = min(np.min(NN_signal_output), np.min(NN_background_output))
    max_nn = max(np.max(NN_signal_output), np.max(NN_background_output))

    min_bdt = min(np.min(BDT_signal_output), np.min(BDT_background_output))
    max_bdt = max(np.max(BDT_signal_output), np.max(BDT_background_output))

    wp_nn = np.linspace(min_nn, max_nn, points)
    wp_bdt = np.linspace(min_bdt, max_bdt, points)

    signal_nn = []
    background_nn = []
    signal_bdt = []
    background_bdt = []

    for i in range(len(wp_nn)):

        nn_sel_signal = NN_signal_output > wp_nn[i]
        nn_sel_background = NN_background_output > wp_nn[i]
        
        bdt_sel_signal = BDT_signal_output > wp_bdt[i]
        bdt_sel_background = BDT_background_output > wp_bdt[i]
        
        signal_nn.append(np.sum(NN_signal_weight[nn_sel_signal]))
        background_nn.append(np.sum(NN_background_weight[nn_sel_background]))

        signal_bdt.append(np.sum(BDT_signal_weight[bdt_sel_signal]))
        background_bdt.append(np.sum(BDT_background_weight[bdt_sel_background]))

    # plotting

    plot('BDT', 'dashdot', wp_bdt, signal_bdt, background_bdt)
    plot('NN', '-', wp_nn, signal_nn, background_nn)

    plt.ylim(bottom = 0.07) 

    plt.ylabel('Amount of events')
    plt.xlabel('Working point')
    plt.legend(prop={"size":7}, loc = 'upper right')
    plt.savefig('results/signBkgTotal.pdf')

    plt.yscale('log')
    plt.savefig('results/signBkgTotal_log.pdf')
