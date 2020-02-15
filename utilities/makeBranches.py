###
# Code largely copied from: https://github.com/GhentAnalysis/ttg/blob/RunII/tools/python/makeBranches.py
###

from ROOT import gROOT, AddressOf

cType = {
    'b': 'UChar_t',
    'S': 'Short_t',
    's': 'UShort_t',
    'I': 'Int_t',
    'i': 'UInt_t',
    'F': 'Float_t',
    'D': 'Double_t',
    'L': 'Long64_t',
    'l': 'ULong64_t',
    'O': 'Bool_t',
}

def makeBranches(tree, branches):
  
    # new branches are defined in a list as following: [branchName/dataType, ....]

    branches = [tuple(branch.split('/')) for branch in branches]
    gROOT.ProcessLine('struct newVars {' + ';'.join([cType[t] + ' ' + name for name, t in branches]) + ';};')
    from ROOT import newVars
    newVars = newVars()

    # add new branch to the tree

    for name, t in sorted(branches):
        tree.Branch(name, AddressOf(newVars, name), name+ '/' + t)
    return newVars
