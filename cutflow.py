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
                
                # Now we implement the last good jet criterion, namely having DeltaR > 0.4 wrt the two prompt leptons
                
                for lep in self.nLight:


                    D_phi = self.tree._jetPhi[i] - self.tree._lPhi[lep]
                    D_eta = self.tree._jetEta[i] - self.tree._lEta[lep]

                    DeltaR = np.sqrt(D_phi**2 + D_eta**2)
                    #print(DeltaR)
                    if DeltaR < 0.4:
                        
                        break
                    
                    if lep == self.nLight[-1]:

                        validJets.append(i)

        if len(validJets) >= 5:

            return True, self.nLight, validJets

        return False, self.nLight, validJets

    def nbjets(self):

        # this function assumes that you FIRST applied the njets cut, which is the logical order

        validbjets = []

        for i in self.nJets:

            if self.tree._jetDeepCsv_b[i] > 0.4941:

                validbjets.append(i)

        if validbjets:

            return True, self.nLight, self.nJets

        return False, self.nLight, self.nJets

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
######## UTILITIES ########                                                                                                                                                                          
###########################


def writeToFile(f, array, delimiter = "&"):

    np.savetxt(f, np.array(array).T, delimiter = delimiter, fmt = "%s")

def weight_TotalEvents(filename, xSec, lumi = 59.74):

    hCounter = ROOT.TH1F("hCounter","Events Counter",1 ,0 ,1 )
    hCounter = filename.Get("blackJackAndHookers/hCounter")
    totalEvents = hCounter.GetBinContent(1)

    return 1000 * xSec * lumi / totalEvents, totalEvents

def cutflow(f, xSec, cutList, year):

    filename = ROOT.TFile.Open(f)

    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    weight, initialEvents = weight_TotalEvents(filename, xSec, lumi)
    tree = filename.Get("blackJackAndHookers/blackJackAndHookersTree")

    counts = list(np.zeros(len(cutList)))
    counts_w = list(np.zeros(len(cutList)))
    

    progress = 0
    entries = tree.GetEntries()


    for _ in tree:

#        progress += 1 # To stop testing, just comment this line out. Maybe have it as an argument or so?

        if progress / float(entries) > 0.01:

            break



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

    filename.Close()

    return counts, counts_w

###########################                                                                                                                                                                                
########## MAIN ###########                                                                                                                                                                             
###########################                                                                                                                                                                               


stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"

year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)


channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str)

xSecs = xSecs.astype(float)

cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "justTwoLeptons", "twoOS", "njets", "nbjets", "twoSF", "onZ"]


cutflowList = []
sources = [" "]

targetFile = open("cutflowResults/cutflowAllFiles.txt", "a")

for i in range(len(files)):

    f = files[i]
    print("Working on file number {}".format(i))
    print(f)
    print(channels_stack[i])
    events, weighted_events = cutflow(f, xSecs[i], cutList, year = year)

    sources.append(texList[i])
    sources.append(texList[i] + "_weighted")

    cutflowList.append(events)
    cutflowList.append(weighted_events)
    

cutflowList = np.around(cutflowList, 2).astype(str)

# Remove unneeded zeroes after the decimal point

for i in range(cutflowList.shape[0]):
    for j in range(cutflowList.shape[1]):

        if int(float(cutflowList[i,j])) == float(cutflowList[i,j]):

            cutflowList[i,j] = cutflowList[i,j].replace(".0", "")



cutList.insert(0,"Initial event count")

cutflowList = np.insert(cutflowList, 0, cutList, axis = 0)
cutflowList = np.insert(cutflowList, 0, sources, axis = 1)

print(cutflowList.shape)

writeToFile("cutflowResults/cutflowAllFiles.txt", cutflowList, delimiter = "&")
