from ROOT import TFile, TTree, TH1F, TList
from utilities.makeBranches import makeBranches
import sys
from makeHists import initializeHist


def fillHists(inputTree, branches_split):

    histList = TList()

    for name in branches_split:

        hist = initializeHist(name[0], name[0], 2, -1, 1)
        hist.StatOverflows(True)
        histList.Add(hist)

    for _ in inputTree:

        for i in range(len(branches_split)):

            variable = branches_split[i][0]

            histList[i].Fill(getattr(inputTree, variable))

    return histList

def calcMeanStddev(histList):

    # calculate all means and stddevs

    means = list()
    stddevs = list()

    for hist in histList:

        means.append(hist.GetMean())
        stddevs.append(hist.GetStdDev())

    return means, stddevs 
    
def normalizeEvents(inputTree, sampleName, year, branches, means, stddevs):

    # create output file and new tree                                                                                                                                                                           
    outputFile = TFile('newTrees/normalizedTrees/tree_' + sampleName + '_' + year + '.root', 'RECREATE')
    outputFile.cd()
    newTree = TTree('tree_' + sampleName, sampleName)

    # define all properties each events posesses in the tree

    variables = makeBranches(newTree, branches)
              
    # loop over original events and add them to new tree

    for _ in inputTree:

        for i in range(len(branches)):

            name = branches[i].split('/')[0]
            
            setattr(variables, name, (getattr(inputTree, name) - means[i]) / stddevs[i])
            
        newTree.Fill()

    # save tree and close file                                                                                                                                                                             

    newTree.AutoSave()
    outputFile.Close()


########                                                                                                                                                                                                   ##MAIN##                                                                                                                                                                                                 
########                                                                                                                                                                                                  

# branches = ['lPt1/F', 'lPt2/F', 'lEta1/F', 'lEta2/F', 'lPhi1/F', 'lPhi2/F', 'DeltaR_1/F', 'DeltaR_b1/F', 'DeltaR_2/F', 'DeltaR_b2/F']
# branches += ['njets/I', 'nbjets/I', 'jetDeepCsv_b1/F']
# branches += ['mW1/F', 'mtop1/F', 'weight/F']

# made all floats as to not give issues after normalization

branches = ['lPt1/F', 'lPt2/F', 'lEta1/F', 'lEta2/F', 'lPhi1/F', 'lPhi2/F', 'DeltaR_1/F', 'DeltaR_b1/F', 'DeltaR_2/F', 'DeltaR_b2/F']
branches += ['njets/F', 'nbjets/F', 'jetDeepCsv_b1/F']
branches += ['mW1/F', 'mtop1/F', 'weight/F']

branches_split = [tuple(branch.split('/')) for branch in branches]

# get input data

year = sys.argv[1].split('.')[0].split('_')[-1]
sampleName = sys.argv[2].lstrip('tree_')
print("Using files from " + year)
print("Current channel: {}".format(sampleName))
rootfile = sys.argv[1]
f = TFile.Open(rootfile)
inputTree = f.Get(sys.argv[2])

# fillhists and calculate means + stddevs

histList = fillHists(inputTree, branches_split)
means, stddevs = calcMeanStddev(histList)

# gets rid of annoying error

del histList


# loop over events, normalize and add to new tree

normalizeEvents(inputTree, sampleName, year, branches, means, stddevs)

f.Close()

