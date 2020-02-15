import numpy as np
from ROOT.Math import PtEtaPhiEVector


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
    
    bjets = list()
    jetVecs = list()
    bjetVecs = list()
    
    for jet in jets:

        vec = PtEtaPhiEVector()
        vec.SetCoordinates(tree._jetPt[jet], tree._jetEta[jet], tree._jetPhi[jet], tree._jetE[jet])

        if tree._jetDeepCsv_b[jet] > 0.4941:

            jets.remove(jet)
            bjets.append(jet)
            bjetVecs.append(vec)

        else:

            jetVecs.append(vec)


    jetAmount = len(jets)    

    if jetAmount < 2:

        return None, None, (None, None, None, None), bjetVecs

    masses = np.zeros((jetAmount, jetAmount))

    # Loop over all jets, reconstruct invariant mass of every two-jet system

    # jetVecs = list()

    # for i in range(jetAmount):

    #     jet = jets[i]
    #     vec = PtEtaPhiEVector()
    #     vec.SetCoordinates(tree._jetPt[jet], tree._jetEta[jet], tree._jetPhi[jet], tree._jetE[jet])
    #     jetVecs.append(vec)

    for i in range(jetAmount):

        for j in range(i+1, jetAmount):

            jet1 = jetVecs[i]
            jet1 += jetVecs[j]
            
            # jet2 += jet1

            masses[i,j] = jet1.M()

    # Choose the two invariant masses which are closest resembling the W mass while originating from two different jet pairs
    # we do this by looping over the mass matrix, selecting the first mass, looping again and selecting the second mass

    bestWmass, j1, j2 = selectBest(masses, jetAmount)

    if jetAmount < 4:

        return bestWmass, None, (j1, j2, None, None), bjetVecs

    secondWmass, j3, j4 = selectBest(masses, jetAmount, skipids = {j1, j2})

    return bestWmass, secondWmass, (j1, j2, j3, j4), bjetVecs
    

