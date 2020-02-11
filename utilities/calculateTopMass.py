import numpy as np
import ROOT
from selectionHelpers import countbJets

topMass_known = 172.9

def selectBest(massMatrix, bjetAmount, skipids = {}):

    # This function loops over the mass matrix and selects the best match wrt the top quark mass.
    # For the second best match, some jetIds which should not be considered are also given as an input.
    
    W_id = None
    bjet_id = None
    diff = 1e6

    for i in range(2): # loops over the W masses, there are always two W's reconstructed

        if i not in skipids:

            for j in range(bjetAmount):

                if j not in skipids:
                    
                    massDifference = np.abs(massMatrix[i,j] - topMass_known)

                    if massDifference  < diff:

                        diff = massDifference

                        W_id = i
                        bjet_id = j


    return massMatrix[W_id,bjet_id], W_id, bjet_id

                    
def topMass(lepton):

    tree = lepton.tree

    bjets = countbJets(lepton)
    bjetAmount = len(bjets)
    
    masses = np.zeros((2, bjetAmount))

    W_vecs = ROOT.TList([lepton.w1_vec, lepton.w2_vec])

    # Loop over all bjets and W's, reconstruct invariant mass of every twobody system

    for i in range(2):

        for j in range(bjetAmount):

            bjet_id = bjets[j]
            
            vec1 = W_vecs[i]
            #vec1 = ROOT.Math.PtEtaPhiEVector()
            vec2 = ROOT.Math.PtEtaPhiEVector()

            #vec1.SetCoordinates(tree._jetPt[W_id], tree._jetEta[W_id], tree._jetPhi[W_id], tree._jetE[W_id])
            vec2.SetCoordinates(tree._jetPt[bjet_id], tree._jetEta[bjet_id], tree._jetPhi[bjet_id], tree._jetE[bjet_id])

            vec1 += vec2

            masses[i,j] = vec1.M()

    # Choose the two invariant masses which are closest resembling the W mass while originating from two different jet pairs
    # we do this by looping over the mass matrix, selecting the first mass, looping again and selecting the second mass

    bestWmass, j1, j2 = selectBest(masses, jetAmount)
    secondWmass, _, _ = selectBest(masses, jetAmount, skipids = {j1, j2})

    return bestWmass, secondWmass
    

