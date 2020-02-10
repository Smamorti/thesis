import numpy as np
import ROOT
from  utilities import calculateWmass as W

class lepton:


    def __init__(self, tree, nLight, checknJets = True, calcWmass = False):
        self.tree = tree
        self.nLight = nLight

        if checknJets:

            self.goodJets = self.countJets()

        if calcWmass:

            w1, w2 = W.Wmass(self)
            self.bestWmass = w1
            self.secondWmass = w2

    def countJets(self):

        goodJets = []

        for j in range(self.nJets()):

            if goodJet(self.tree, j):

                goodJets.append(j)

        return goodJets

    def tree(self):

        return self.tree

    def test(self):

        return self.nLight

    def bestWmass(self):

        return self.bestWmass

    def secondWmass(self):

        return self.secondWmass

    def lPt(self):

        return self.tree._lPt[self.nLight]

    def lFlavor(self):

        return self.tree._lFlavor[self.nLight]

    def lCharge(self):

        return self.tree._lCharge[self.nLight]

    def lMatchPdgId(self):

        return self.tree._lMatchPdgId[self.nLight]

    def lEta(self):

        return self.tree._lEta[self.nLight]

    def lPhi(self):

        return self.tree._lPhi[self.nLight]

    def lE(self):

        return self.tree._lE[self.nLight]
    
    def MET(self):

        return self.tree._met

    def nJets(self):
        
        if type(self.tree._nJets) == int:

            return self.tree._nJets

        else:

            return ord(self.tree._nJets)

    def leptonMVA(self):

#        return self.tree._leptonMvatZqTTV[self.nLight]
        return self.tree._leptonMvatZq[self.nLight]

    def lMomPdg(self):

        return self.tree._lMomPdgId[self.nLight]


    def fillLepList(self): #later add gen_nl?
                                                                                         
        return [self.nLight, self.lFlavor(), self.lCharge(), self.lMatchPdgId()]#, _gen_lMomPdg]                                                                                                

###########################
#### VARIABLES TO PLOT ####
###########################

def leading_leptonMVA(l1, l2, hist, totalWeight):

    hist.Fill(lepton.leptonMVA(l1), totalWeight)

def subleading_leptonMVA(l1, l2, hist, totalWeight):

    hist.Fill(lepton.leptonMVA(l2), totalWeight)

def leading_lPt(l1, l2, hist, totalWeight):

    hist.Fill(lepton.lPt(l1), totalWeight)

def subleading_lPt(l1, l2, hist, totalWeight):

    hist.Fill(lepton.lPt(l2), totalWeight)

def leading_lEta(l1, l2, hist, totalWeight):

    hist.Fill(np.absolute(lepton.lEta(l1)), totalWeight)
    
def subleading_lEta(l1, l2, hist, totalWeight):

    hist.Fill(np.absolute(lepton.lEta(l2)), totalWeight)

def nJets(l1, l2, hist, totalWeight):

    hist.Fill(len(l1.goodJets), totalWeight)

def m_ll(l1, l2, hist, totalWeight):

    hist.Fill(diLeptonMass(l1, l2), totalWeight)
    
def flavComp(l1, l2, hist, totalWeight):

    if lepton.lFlavor(l1) == 0: #ee

        hist.Fill(0, totalWeight)

    else: #mumu

        hist.Fill(1, totalWeight)

def nbJets(l1, l2, hist, totalWeight):

    hist.Fill(len(countbJets(l1)), totalWeight)

def MET(l1, l2, hist, totalWeight):

    hist.Fill(lepton.MET(l1), totalWeight)

def leading_DeltaR(l1, l2, hist, totalWeight):

    hist.Fill(calculateDeltaR(l1, l1, b = False), totalWeight)

def leading_DeltaR_b(l1, l2, hist, totalWeight):

    hist.Fill(calculateDeltaR(l1, l1, b = True), totalWeight)

def subleading_DeltaR(l1, l2, hist, totalWeight):

    hist.Fill(calculateDeltaR(l1, l2, b = False), totalWeight)

def subleading_DeltaR_b(l1, l2, hist, totalWeight):

    hist.Fill(calculateDeltaR(l1, l2, b = True), totalWeight)

def Zmass(l1, l2, hist, totalWeight):


    if lepton.lMomPdg(l1) == 23 and lepton.lMomPdg(l2) == 23:

        hist.Fill(diLeptonMass(l1, l2), totalWeight)
        
def bestW(l1, l2, hist, totalWeight):

    hist.Fill(lepton.bestWmass(l1), totalWeight)

def secondW(l1, l2, hist, totalWeight):

    hist.Fill(lepton.secondWmass(l1), totalWeight)

        


###########################                                                                                                                                                                                
######## UTILITIES ########                                                                                                                                                                                
########################### 

# maybe move this to seperate .py file?

def goodJet(tree, j):

    if (tree._jetIsTight[j]
        and tree._jetPt[j] > 30
        and np.absolute(tree._jetEta[j]) < 2.4
        ):

        return True

    return False


def countbJets(l1):
    
    nbjets = []

    for j in l1.goodJets:

        if l1.tree._jetDeepCsv_b[j] > 0.4941:

            nbjets.append(j)

    return nbjets

def calculateDeltaR(l1, lep, b = False):

    # The l1 is to access the jets
    # The lep is the lepton for which we are calculating the DeltaR (leading=l1, subleading=l2)

    DeltaR = 1000
    jets = l1.goodJets
    
    if b:

        jets = countbJets(l1)
        
    for jet in jets:

        D_phi = l1.tree._jetPhi[jet] - lepton.lPhi(lep)
        D_eta = l1.tree._jetEta[jet] - lepton.lEta(lep)
        
        D_r = np.sqrt(D_phi**2 + D_eta**2)
        DeltaR = np.minimum(D_r, DeltaR)
        
    return DeltaR

def diLeptonMass(l1, l2):

    vec1 = ROOT.Math.PtEtaPhiEVector()
    vec2 = ROOT.Math.PtEtaPhiEVector()

    vec1.SetCoordinates(lepton.lPt(l1), lepton.lEta(l1), lepton.lPhi(l1), lepton.lE(l1))
    vec2.SetCoordinates(lepton.lPt(l2), lepton.lEta(l2), lepton.lPhi(l2), lepton.lE(l2))

    vec1 += vec2

    return vec1.M()
