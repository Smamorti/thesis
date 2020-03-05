import numpy as np
import matplotlib.pyplot as plt

def plotRange( array ):

    if type(array[0]) == np.bool_:

        upper_bound = 1
        lower_bound = 0

    elif type(array[0]) == np.unicode_:

        upper_bound = len(set(array)) + 1
        lower_bound = 1

    else:

        lower_bound = np.min( array )
        upper_bound = np.max( array )

    print( 'max = {}'.format( upper_bound ) )

    variation =( upper_bound - lower_bound )
    excess_space = variation*0.1


    lower_bound = (lower_bound - excess_space ) if lower_bound > 0 else ( lower_bound + excess_space )
    upper_bound = (upper_bound + excess_space ) if upper_bound > 0 else ( upper_bound - excess_space )

    return lower_bound, upper_bound
        

def scatterPlot( x_array, x_label, y_array, y_label, plot_file_name ):


    plt.xlabel( x_label )
    plt.ylabel( y_label )
    print( '~~~~~~~~~~~~~~~~~~~~~' )
    print( plot_file_name )
    
    if 'generation' in plot_file_name:

        index = plot_file_name.rfind('/')
        plot_file_name = plot_file_name[:index] + '_' + plot_file_name[index+1:]

    print( plot_file_name )
    print( plotRange( y_array ) )
    print( plotRange( x_array ) )
    plt.xlim( plotRange( x_array ) )
    plt.ylim( plotRange( y_array ) )

    if type(x_array[0]) == np.unicode_:

        labels = list(set(x_array))
        num_labels = [i + 1 for i in range(len(labels))]
        x_array_new = [num_labels[labels.index(j)] for j in x_array]

        # print(x_array)
        # print(x_array_new)
        # print(labels)
        # print(num_labels)

        plt.xticks(x_array_new, x_array)
        plt.scatter( x_array_new, y_array )

    else:

        plt.scatter(x_array, y_array)

    if not '.' in plot_file_name:
        plot_file_name += '.pdf'
    plt.savefig( plot_file_name )
    plot_file_name = plot_file_name.replace('.pdf', '.png')
    plt.savefig( plot_file_name )
    plt.clf()

