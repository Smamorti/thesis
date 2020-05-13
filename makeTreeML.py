from __future__ import division
from ROOT import TFile, TTree
from utilities.makeBranches import makeBranches
from weights.calcBjetWeights import getBtagArrays, loadBtagHists, calcBtagWeight
from cuts import cuts
from makeHists import calcWeight
from plotVariables import lepton, calculateDeltaR, H_t
import numpy as np
import sys
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-c", "--conf", default = "samples/signal_2018_v3.conf", help = "conf file")
parser.add_option("-s", "--source", default = "signal_2018", help = "signal or background?")
parser.add_option("-y", "--year", default = 2018, help = "year")
parser.add_option("--pileupFile", default = "weights/pileup/pileup_nominal_total.root")
parser.add_option("-b","--btagType", default = 'central', help = 'central, up or down?')
options, args = parser.parse_args(sys.argv[1:])


def makeTree(inputFiles, sampleName, branches, year, xSecs, pileupWeights, btagArrays, btagHists):

    print("Currently working on the {} samples".format(sampleName))

    # create output file and new tree                                                                                                                                                                     

    outputFile = TFile('newTrees/reducedTrees/tree_' + sampleName + '_nominal.root', 'RECREATE')
    outputFile.cd()
    newTree = TTree('tree_' + sampleName, sampleName)

    # define all properties each events posesses in the tree
    
    variables = makeBranches(newTree, branches)

    # use all different sign/bkg sources to fill the tree

    for i in range(len(inputFiles)):

        inputFile = TFile.Open(inputFiles[i])
        print("Working on file number {} out of {}".format(i+1, len(inputFiles)))

        # read inputTree
        
        inputTree = inputFile.Get("blackJackAndHookers/blackJackAndHookersTree")

        # loop over the events, apply cuts, if all cuts apply: fill tree

        fillTree(inputFile, inputTree, newTree, variables, year, xSecs[i], pileupWeights, btagArrays, btagHists)
        inputFile.Close()

    # save tree and close file

    newTree.AutoSave()
    outputFile.Close()


def fillTree(inputFile, inputTree, newTree, variables, year, xSec, pileupWeights, btagArrays, btagHists):

    JEC = 'nominal'

    # loop over all events, apply cuts, if all cuts apply: fill tree

    cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "justTwoLeptons", "twoOS", "njets", "nbjets", "twoSF", "onZ"]
    year = str(year)
    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    t = inputTree

    weight = calcWeight(inputFile, xSec, lumi)

    count = t.GetEntries()

    print(count)

    # setup progressbar                                                                                                                                                                                   
    toolbar_width = 100

    sys.stdout.write("Progress: [%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['                                                                                                                        
    progress = 0
    toolbarProgress = 0

    measurementTypes, jetFlavors, ptLow, ptHigh, tformulas, inclusiveFormula = btagArrays
    udsgHist, cHist, bHist = btagHists


    for _ in t:

        progress += 1
        
        total = count

        # to stop testing, comment the following three lines out                                                                                                                                           

        # total = count * 0.01

        # if progress / float(count) > 0.01:

        #     break

        if progress / total > toolbarProgress / toolbar_width:
            toolbarProgress += 1
            sys.stdout.write("-")
            sys.stdout.flush()

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

                    btagFactor = calcBtagWeight(t, nJets, udsgHist, cHist, bHist, jetFlavors, ptLow, ptHigh, tformulas, inclusiveFormula, JEC)

                    

                    variables.weight = t._weight * weight * pileupWeights.GetBinContent(int(t._nTrueInt)) * btagFactor
                    variables.lPt1 = t._lPt[nLight[0]]
                    variables.lPt2 = t._lPt[nLight[1]]
                    variables.lEta1 = t._lEta[nLight[0]]
                    variables.lEta2 = t._lEta[nLight[1]]
                    variables.lPhi1 = t._lPhi[nLight[0]]
                    variables.lPhi2 = t._lPhi[nLight[1]]
                    variables.I_rel1 = t._relIso[nLight[0]]
                    variables.I_rel2 = t._relIso[nLight[1]]
                    
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

                    # add all jet properties

                    variables.jetPt1 = t._jetPt[nJets[0]]
                    variables.jetEta1 = t._jetEta[nJets[0]]
                    variables.jetPhi1 = t._jetPhi[nJets[0]]
                    
                    variables.jetPt2 = t._jetPt[nJets[1]]
                    variables.jetEta2 = t._jetEta[nJets[1]]
                    variables.jetPhi2 = t._jetPhi[nJets[1]]
                    
                    variables.jetPt3 = t._jetPt[nJets[2]]
                    variables.jetEta3 = t._jetEta[nJets[2]]
                    variables.jetPhi3 = t._jetPhi[nJets[2]]
                    
                    variables.jetPt4 = t._jetPt[nJets[3]]
                    variables.jetEta4 = t._jetEta[nJets[3]]
                    variables.jetPhi4 = t._jetPhi[nJets[3]]
                    
                    variables.jetPt5 = t._jetPt[nJets[4]]
                    variables.jetEta5 = t._jetEta[nJets[4]]
                    variables.jetPhi5 = t._jetPhi[nJets[4]]
                    
                    # calculate H_t^miss and add it to tree, also add MET
                    
                    variables.H_t = H_t(lepton1)

                    variables.MET = t._met

                    # Fill tree

                    newTree.Fill()
            else:

                break

    sys.stdout.write("]\n") # this ends the progress bar

########
##MAIN##
########
            
                    
branches = ['lPt1/F', 'lPt2/F', 'lEta1/F', 'lEta2/F', 'lPhi1/F', 'lPhi2/F', 'DeltaR_1/F', 'DeltaR_b1/F', 'DeltaR_2/F', 'DeltaR_b2/F']
branches += ['njets/I', 'nbjets/I', 'jetDeepCsv_b1/F']
branches += ['jetPt1/F', 'jetEta1/F', 'jetPhi1/F']
branches += ['jetPt2/F', 'jetEta2/F', 'jetPhi2/F']
branches += ['jetPt3/F', 'jetEta3/F', 'jetPhi3/F']
branches += ['jetPt4/F', 'jetEta4/F', 'jetPhi4/F']
branches += ['jetPt5/F', 'jetEta5/F', 'jetPhi5/F']
branches += ['mW1/F', 'mtop1/F', 'weight/F']
branches += ['MET/F', 'H_t/F']
branches += ['I_rel1/F', 'I_rel2/F']

channels_conf, files, xSecs = np.loadtxt(options.conf, comments = "%", unpack = True, dtype = str)
xSecs = xSecs.astype(float)

if type(files) == np.string_:

    # in this case, there is only one sample, however the script requires lists, so we give it lists

    files = [files]
    xSecs = [xSecs]

# load pileup weights                                                                                              
f = TFile.Open(options.pileupFile)

pileupWeights = f.Get("pileup")

# load arrays needed to calculate btag arrays                                                                      
csvFile = "weights/DeepCSV_94XSF_WP_V4_B_F.csv"
btagArrays = getBtagArrays(csvFile, options.btagType)
btagFile = TFile.Open("weights/bTagEff_looseLeptonCleaned_2018.root")
btagHists = loadBtagHists(btagFile)





makeTree(files, options.source, branches, options.year, xSecs, pileupWeights = pileupWeights, btagArrays = btagArrays, btagHists = btagHists)


print("Finished!")
