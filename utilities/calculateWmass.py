import numpy as np
import ROOT


Wmass_known = 80.379

def selectBest(massMatrix, jetAmount, skipids = {}):

    # This function loops over the mass matrix and selects the best match wrt the W mass.
    # For the second best match, some jetIds which should not be considered are also given as an input.
    
    j1 = None
    j2 = None
    diff = 1e6

    for i in range(jetAmount):

        if i not in skipids:

            for j in range(i+1, jetAmount):

                if j not in skipids:
                    
                    massDifference = np.abs(massMatrix[i,j] - Wmass_known)

                    if massDifference  < diff:

                        diff = massDifference

                        j1 = i
                        j2 = j


    return massMatrix[j1,j2], j1, j2

                    
def Wmass(lepton):

    tree = lepton.tree

    jets = lepton.goodJets
    jetAmount = len(jets)
    
    masses = np.zeros((jetAmount, jetAmount))

    # Loop over all jets, reconstruct invariant mass of every two-jet system

    for i in range(jetAmount):

        for j in range(i+1, jetAmount):

            jet1 = jets[i]
            jet2 = jets[j]

            vec1 = ROOT.Math.PtEtaPhiEVector()
            vec2 = ROOT.Math.PtEtaPhiEVector()

            vec1.SetCoordinates(tree._jetPt[jet1], tree._jetEta[jet1], tree._jetPhi[jet1], tree._jetE[jet1])
            vec2.SetCoordinates(tree._jetPt[jet2], tree._jetEta[jet2], tree._jetPhi[jet2], tree._jetE[jet2])

            vec1 += vec2

            masses[i,j] = vec1.M()

    # Choose the two invariant masses which are closest resembling the W mass while originating from two different jet pairs
    # we do this by looping over the mass matrix, selecting the first mass, looping again and selecting the second mass

    bestWmass, j1, j2 = selectBest(masses, jetAmount)
    secondWmass, _, _ = selectBest(masses, jetAmount, skipids = {j1, j2})

    return bestWmass, secondWmass
    

