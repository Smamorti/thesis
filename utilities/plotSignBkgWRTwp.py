import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt



def plot(algo, style):

    wp, sign, bkg, ratio, tot = np.loadtxt('../txtfiles/signBkg{}.txt'.format(algo), unpack = True, comments = '#')

    plt.plot(wp, sign, linestyle = style, color = 'red', label = 'signal ({})'.format(algo))
    plt.plot(wp, bkg, linestyle = style, color = 'blue', label = 'background ({})'.format(algo))
    plt.plot(wp, ratio, linestyle = style, color = 'green', label = 'sign/bkg ({})'.format(algo))
    plt.plot(wp, tot, linestyle = style, color = 'purple', label = 'total ({})'.format(algo))


plot('BDT', 'dashdot')
plot('NN', '-')


plt.ylabel('Amount of events')
plt.xlabel('Working point')
plt.xlim(0.3, 1)
plt.legend(prop={"size":8}, loc = 'upper left')
plt.savefig('../plots/signBkgTotal.pdf')

plt.yscale('log')
plt.savefig('../plots/signBkgTotal_log.pdf')
