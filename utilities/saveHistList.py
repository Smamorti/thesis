import pickle

def saveHistList(sourceList, histList, output):

    for i in range(len(sourceList)):

        source = sourceList[i]

        pickle.dump(histList[i], file(output.replace('.pkl', '_' + source + '.pkl'), 'w'))

    pickle.dump(histList, file(output, 'w'))
    
