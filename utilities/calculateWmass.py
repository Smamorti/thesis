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
    JEC = lepton.JEC
    jets = lepton.goodJets
    jetAmount = len(jets)
    
    masses = np.zeros((jetAmount, jetAmount))

    # Loop over all jets, reconstruct invariant mass of every two-jet system

    jetVecs = list()

    for i in range(jetAmount):

        jet = jets[i]
        vec = PtEtaPhiEVector()

        if JEC == 'nominal':

            pt = tree._jetPt[jet]

        elif JEC == 'up':

            pt = tree._jetPt_JECUp[jet]

        elif JEC == 'down':

            pt = tree._jetPt_JECDown[jet]

        else:

            raise ValueError('invalid JEC option')

        vec.SetCoordinates(pt, tree._jetEta[jet], tree._jetPhi[jet], tree._jetE[jet])
        jetVecs.append(vec)

    for i in range(jetAmount):

        for j in range(i+1, jetAmount):

            jet1 = jetVecs[i]
            jet1 += jetVecs[j]
            
            # jet2 += jet1

            masses[i,j] = jet1.M()

    # Choose the two invariant masses which are closest resembling the W mass while originating from two different jet pairs
    # we do this by looping over the mass matrix, selecting the first mass, looping again and selecting the second mass

    bestWmass, j1, j2 = selectBest(masses, jetAmount)
    secondWmass, j3, j4 = selectBest(masses, jetAmount, skipids = {j1, j2})

    return bestWmass, secondWmass, (j1, j2, j3, j4), jetVecs
