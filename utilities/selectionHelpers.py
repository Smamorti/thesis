import numpy as np
from ROOT.Math import PtEtaPhiEVector

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

    vec1 = PtEtaPhiEVector()
    vec2 = PtEtaPhiEVector()

    vec1.SetCoordinates(lepton.lPt(l1), lepton.lEta(l1), lepton.lPhi(l1), lepton.lE(l1))
    vec2.SetCoordinates(lepton.lPt(l2), lepton.lEta(l2), lepton.lPhi(l2), lepton.lE(l2))

    vec1 += vec2

    return vec1.M()
