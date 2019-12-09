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

        validnLight = []

        for i in self.nLight:

            if self.tree._leptonMvatZq[i] > 0.4:

                validnLight.append(i)

        if len(validnLight) >= 2:

            return True, validnLight

        return False, validnLight

    def twoPtLeptons(self):

        validnLight = []
        n30 = 0

        for i in self.nLight:

            if self.tree._lPt[i] > 20:

                validnLight.append(i)

                if self.tree._lPt[i] > 30:

                    n30 += 1

        if len(validnLight) >= 2 and n30 >= 1:

            return True, validnLight

        return False, validnLight

    def lPogLoose(self):

        validnLight = []

        for i in self.nLight:

            if self.tree._lPOGLoose[i]:

                validnLight.append(i)

        if len(validnLight) >= 2:

            return True, validnLight

        return False, validnLight

    def lEta(self):

        validnLight = []

        for i in self.nLight:

            if np.absolute(self.tree._lEta[i]) <= 2.4:

                validnLight.append(i)
                
            elif self.tree._lFlavor[i] == 1 and np.absolute(self.tree._lEta[i]) <= 2.5:
                # other eta requirement for muons

                validnLight.append(i)
                
        if len(validnLight) >= 2:

            return True, validnLight

        return False, validnLight

    def twoOS(self):

        # checks that there are at least one positively and one negatively charged lepton in the remaining selection

        posNeg = np.ones(2)

        for i in self.nLight:
            
            posNeg[self.tree._lFlavor[i]] = 0

            if not np.any(posNeg):

                return True, self.nLight

        return False, self.nLight

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

    cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "twoOS"]
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

        event = cuts(tree, range(nLight))

        for i in range(len(cutList)):

            # from here on out, nLight is an array with all valid nLight values

            validEvent, nLight = getattr(cuts, cutList[i])(event)

            if validEvent:

                counts[i] += 1
                counts_w[i] += tree._weight * weight
                event = cuts(tree, nLight)


            else:
                
                break
                
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
