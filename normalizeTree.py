from ROOT import TFile, TTree, TH1F, TList, gROOT
from utilities.makeBranches import makeBranches
import sys
from makeHists import initializeHist

gROOT.SetBatch(True)

# branches = ['lPt1/F', 'lPt2/F', 'lEta1/F', 'lEta2/F', 'lPhi1/F', 'lPhi2/F', 'DeltaR_1/F', 'DeltaR_b1/F', 'DeltaR_2/F', 'DeltaR_b2/F']
# branches += ['njets/I', 'nbjets/I', 'jetDeepCsv_b1/F']
# branches += ['mW1/F', 'mtop1/F', 'weight/F']

# made all floats as to not give issues after normalization

branches = ['lPt1/F', 'lPt2/F', 'lEta1/F', 'lEta2/F', 'lPhi1/F', 'lPhi2/F', 'DeltaR_1/F', 'DeltaR_b1/F', 'DeltaR_2/F', 'DeltaR_b2/F']
branches += ['njets/F', 'nbjets/F', 'jetDeepCsv_b1/F']
branches += ['mW1/F', 'mtop1/F', 'weight/F']

f = TFile.Open("newTrees/tree_DY_2018_.root")
inputTree = f.Get("tree_DY")

#branches = ['njets/I']

branches_split = [tuple(branch.split('/')) for branch in branches]

entries = inputTree.GetEntries()

histList = TList()

for name in branches_split:
    
    hist = initializeHist(name[0], name[0], 2, -1, 1)
    hist.StatOverflows(True)
    histList.Add(hist)

for _ in inputTree:

    for i in range(len(branches_split)):

        variable = branches_split[i][0]

        print(getattr(inputTree, variable))

        histList[i].Fill(getattr(inputTree, variable))

means = list()
stddevs = list()

for hist in histList:

    means.append(hist.GetMean())
    stddevs.append(hist.GetStdDev())

print(branches)
print(means)
print(stddevs)

# gets rid of annoying error

del histList
