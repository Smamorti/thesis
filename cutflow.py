#
# generate a cutflow table
#

import ROOT
from plotVariables import lepton
from plotVariables import goodJet
from plotVariables import diLeptonMass
import plotVariables
import numpy as np

###########################                                                                                                                                                                              
########## CUTS ###########                                                                                                                                                                              
###########################                                                                                                                                                                               

class cuts:

    def __init__(self, tree, nLight):

        self.tree = tree
        self.nLight = nLight

    def lMVA(self):

        n = 0

        for i in range(self.nLight):

            if self.tree._lPt[i] > 20:

                n += 1

            if n >= 2:

                return True

        return False

    def twoPtLeptons(self):

        n20 = 0
        n30 = 0

        for i in range(self.nLight):

            if self.tree._lPt[i] > 20:

                n20 += 1

                if self.tree._lPt[i] > 30:

                    n30 += 1

            if n20 >= 2 and n30 >= 1:

                return True

        return False

###########################                                                                                                                                                                                
########## MAIN ###########                                                                                                                                                                               
###########################


def weight_TotalEvents(filename, xSec, lumi = 59.74):

    hCounter = ROOT.TH1F("hCounter","Events Counter",1 ,0 ,1 )
    hCounter = filename.Get("blackJackAndHookers/hCounter")
    totalEvents = hCounter.GetBinContent(1)

    return 1000 * xSec * lumi / totalEvents, totalEvents

def cutflow(f, xSec, year):

    filename = ROOT.TFile.Open(f)

    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    weight, initialEvents = weight_TotalEvents(filename, xSec, lumi)
    tree = filename.Get("blackJackAndHookers/blackJackAndHookersTree")

    cutList = ["lMVA", "twoPtLeptons"]
    counts = np.zeros(len(cutList))
    counts_w = np.zeros(len(cutList))
    
    for _ in tree:

        if type(tree._nL) == int:

            nL = tree._nL
            gen_nL = tree._gen_nL
            nLight = tree._nLight
            nJets = tree._nJets

        else:

            nL = ord(tree._nL)
            gen_nL = ord(tree._gen_nL)
            nLight = ord(tree._nLight)
            nJets = ord(tree._nJets)

        event = cuts(tree, nLight)

        for i in range(len(cutList)):

            if getattr(cuts, cutList[i])(event):

                counts[i] += 1
                counts_w[i] += tree._weight * weight

            else:
                
                break

        # if lMVA(tree, nLight):

        #     afterMVA += 1
        #     afterMVA_w += tree._weight * weight


        #     if twoPtLeptons(tree, nLight):

        #         lPt += 1
        #         lPt_w += tree._weight * weight

            # if lMVA(tree, nLight):

            #     afterMVA += 1
            #     afterMVA_w += tree._weight * weight
                
    counts = np.insert(counts, 0, tree.GetEntries())
    counts_w = np.insert(counts_w, 0, initialEvents)

    print(counts)
    print(counts_w)

stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"

year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)


channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str)

xSecs = xSecs.astype(float)


cutflow("/user/mniedzie/Work/ntuples_ttz_2L_ttZ_2018/_ttZ_DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_MiniAOD2018.root", xSecs[1], year)


###########################                                                                                                                                                                               
########## CUTS ###########                                                                                                                                                                               
###########################

def lMVA(tree, nLight):

    return tree._leptonMvatZq[_nLight] > 0.4
