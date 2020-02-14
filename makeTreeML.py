from ROOT import TFile, TTree
from utilities.makeBranches import makeBranches
from cuts import cuts
from makeHists import calcWeight
from plotVariables import lepton, calculateDeltaR
import numpy as np
import sys


def makeTree(inputFile, sampleName, branches, year, xSec):

    # read inputTree

    inputTree = inputFile.Get("blackJackAndHookers/blackJackAndHookersTree")

    # create output file and new tree

    outputFile = TFile('newTrees/tree_' + sampleName + '_' + year + '_.root', 'RECREATE')
    outputFile.cd()
    newTree = TTree('tree_' + sampleName, sampleName)

    # define all properties each events posesses in the tree

    variables = makeBranches(newTree, branches)

    # loop over the events, apply cuts, if all cuts apply: fill tree

    fillTree(inputFile, inputTree, newTree, variables, year, xSec)

    # save tree and close file

    newTree.AutoSave()
    outputFile.Close()

def fillTree(inputFile, inputTree, newTree, variables, year, xSec):

    # loop over all events, apply cuts, if all cuts apply: fill tree

    cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "justTwoLeptons", "twoOS", "njets", "nbjets", "twoSF", "onZ"]

    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74


    t = inputTree

    weight = calcWeight(inputFile, xSec, lumi)

    count = t.GetEntries()

    print(count)
    progress = 0

    for _ in t:

        # to quickly test the program                                                                                                                                                                       
        progress += 1 # To stop testing, just comment this line out. Maybe have it as an argument or so?                                                                                                    
        if progress / float(count) > 0.01:

            break

        # make script compatible with both 2017 and 2018 files                                                                                                                                              
        if type(t._nL) == int:

            nL = t._nL
            gen_nL = t._gen_nL
            nLight = t._nLight
            nJets = t._nJets

        else:

            nL = ord(t._nL)
            gen_nL = ord(t._gen_nL)
            nLight = ord(t._nLight)
            nJets = ord(t._nJets)

        event = cuts(t, range(nLight), range(nJets))

        for i in range(len(cutList)):

            # from here on out, nLight is an array with all valid nLight values                                                                                                                             
            validEvent, nLight, nJets = getattr(cuts, cutList[i])(event)

            if validEvent:

                event = cuts(t, nLight, nJets)
                
                # if the last cut was succesfull, we want to add the event to the new tree

                if i == len(cutList) - 1:
                   
                    variables.weight = t._weight * weight
                    variables.lPt1 = t._lPt[nLight[0]]
                    variables.lPt2 = t._lPt[nLight[1]]
                    variables.lEta1 = t._lEta[nLight[0]]
                    variables.lEta2 = t._lEta[nLight[1]]
                    variables.lPhi1 = t._lPhi[nLight[0]]
                    variables.lPhi2 = t._lPhi[nLight[1]]
                    variables.njets = len(nJets)
                    
                    nbjets = 0
                    
                    for i in nJets:

                        if t._jetDeepCsv_b[i] > 0.4941:

                            nbjets += 1

                    variables.nbjets = nbjets
                    variables.jetDeepCsv_b1 = t._jetDeepCsv_b[nJets[0]] #jetDeepCsv_b of leading jet
                   
                    
                    # make two lepton objects to calculate DeltaR, mW, mtop

                    lepton1 = lepton(t, nLight[0], checknJets = True, calcWmass = True, nJets = nJets)
                    lepton2 = lepton(t, nLight[1], checknJets = False)

                    # calculate all DeltaR values

                    variables.DeltaR_1 = calculateDeltaR(lepton1, lepton1, b = False)
                    variables.DeltaR_2 = calculateDeltaR(lepton1, lepton2, b = False)
                    variables.DeltaR_b1 = calculateDeltaR(lepton1, lepton1, b = True)
                    variables.DeltaR_b2 = calculateDeltaR(lepton1, lepton2, b = True)
                   
                    # calculate W and top mass
                   
                    mW1 = lepton.bestWmass(lepton1)
                    mtop1 = lepton.bestTopMass(lepton1)

                    if not mtop1:

                        mtop1 = 1000
                        
                    variables.mW1 = mW1
                    variables.mtop1 = mtop1

                    newTree.Fill()
            else:

                break

########
##MAIN##
########
            
                    
branches = ['lPt1/F', 'lPt2/F', 'lEta1/F', 'lEta2/F', 'lPhi1/F', 'lPhi2/F', 'DeltaR_1/F', 'DeltaR_b1/F', 'DeltaR_2/F', 'DeltaR_b2/F']
branches += ['njets/I', 'nbjets/I', 'jetDeepCsv_b1/F']
branches += ['mW1/F', 'mtop1/F', 'weight/F']


stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"

channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str)

# find out which file is used (This could be better, for instance through matching channel names 
#instead of trusting that they are in the same order in the .stack and .conf files!)

i = np.where(files == sys.argv[1])[0][0]

xSecs = xSecs.astype(float)
year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)
f = TFile.Open(files[i])
print("Working on file number {}: {}".format(i, channels_stack[i]))

makeTree(f, channels_stack[i], branches, year, xSecs[i])

f.Close()

print("Finished!")
