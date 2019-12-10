#
# generate a cutflow table
#

import ROOT
from plotVariables import lepton
from plotVariables import goodJet
from plotVariables import diLeptonMass
import numpy as np

###########################                                                                                                                                                                              
########## CUTS ###########                                                                                                                                                                              
###########################                                                                                                                                                                               

class cuts:

    def __init__(self, tree, nLight, nJets):

        self.tree = tree
        self.nLight = nLight
        self.nJets = nJets

    def lMVA(self):

        validnLight = []

        for i in self.nLight:

            if self.tree._leptonMvatZq[i] > 0.4:

                validnLight.append(i)

        if len(validnLight) >= 2:

            return True, validnLight, self.nJets

        return False, validnLight, self.nJets

    def twoPtLeptons(self):

        validnLight = []
        n30 = 0

        for i in self.nLight:

            if self.tree._lPt[i] > 20:

                validnLight.append(i)

                if self.tree._lPt[i] > 30:

                    n30 += 1

        if len(validnLight) >= 2 and n30 >= 1:

            return True, validnLight, self.nJets

        return False, validnLight, self.nJets

    def lPogLoose(self):

        validnLight = []

        for i in self.nLight:

            if self.tree._lPOGLoose[i]:

                validnLight.append(i)

        if len(validnLight) >= 2:

            return True, validnLight, self.nJets

        return False, validnLight, self.nJets

    def lEta(self):

        validnLight = []

        for i in self.nLight:

            if np.absolute(self.tree._lEta[i]) <= 2.4:

                validnLight.append(i)
                
            elif self.tree._lFlavor[i] == 1 and np.absolute(self.tree._lEta[i]) <= 2.5:
                # other eta requirement for muons

                validnLight.append(i)
                
        if len(validnLight) >= 2:

            return True, validnLight, self.nJets

        return False, validnLight, self.nJets

    def twoOS(self):

        # checks that there are at least one positively and one negatively charged lepton in the remaining selection

        posNeg = np.ones(2)
        
    
        for i in self.nLight:
            
            # 0 is charge -1, 1 is charge 1
            position = 0 if self.tree._lCharge[i] == -1 else 1
            posNeg[position] = 0

            if not np.any(posNeg):

                return True, self.nLight, self.nJets

        return False, self.nLight, self.nJets

    def njets(self):

        validJets = []

        for i in self.nJets:

            if goodJet(self.tree, i):

                validJets.append(i)

        if len(validJets) > 5:

            return True, self.nLight, validJets

        return False, self.nLight, validJets

    def nbjets(self):

        # this function assumes that you FIRST applied the njets cut, which is the logical order

        validbjets = []

        for i in self.nJets:

            if self.tree._jetDeepCsv_b[i] > 0.4941:

                validbjets.append(i)

        if validbjets:

            return True, self.nLight, validbjets

        return False, self.nLight, validbjets

    def justTwoLeptons(self):

        # if at this point there are more than two leptons remaining, discard the event!
        # note that this does assume you applied all other leptons cuts beforehand!
        # the previous cuts already eliminate the events with less than two leptons, so we don't have to worry about those!

        if len(self.nLight) > 2:

            return False, self.nLight, self.nJets

        return True, self.nLight, self.nJets

    def twoSF(self):

        # this assumes that there already are only 2 leptons left!

        if self.tree._lFlavor[self.nLight[0]] == self.tree._lFlavor[self.nLight[1]]:

            return True, self.nLight, self.nJets

        return False, self.nLight, self.nJets

    def onZ(self):

        #check mll requirement          

        lepton1 = lepton(self.tree, self.nLight[0], checknJets = False)    
        lepton2 = lepton(self.tree, self.nLight[1], checknJets = False)

        if 81 < diLeptonMass(lepton1, lepton2) < 101:

            return True, self.nLight, self.nJets

        return False, self.nLight, self.nJets


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

    cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "twoOS", "njets", "nbjets", "justTwoLeptons", "twoSF", "onZ"]
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

        event = cuts(tree, range(nLight), range(nJets))

        for i in range(len(cutList)):

            # from here on out, nLight is an array with all valid nLight values

            validEvent, nLight, nJets = getattr(cuts, cutList[i])(event)

            if validEvent:

                counts[i] += 1
                counts_w[i] += tree._weight * weight
                event = cuts(tree, nLight, nJets)


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
#cutflow("/user/mniedzie/Work/ntuples_ttz_2L_ttZ_2018/_ttZ_TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_MiniAOD2018.root", xSecs[2], year)

