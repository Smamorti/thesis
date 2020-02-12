import numpy as np
from selectionHelpers import countbJets

topMass_known = 172.9

def selectBest(massMatrix, bjetAmount, skipids = (None, None)):

    # This function loops over the mass matrix and selects the best match wrt the top quark mass.
    # For the second best match, some jetIds which should not be considered are also given as an input.
    
    W_id = None
    bjet_id = None
    diff = 1e6

    for i in range(2): # loops over the W masses, there are always two W's reconstructed

        if i != skipids[0]:

            for j in range(bjetAmount):

                if j != skipids[1]:
                    
                    # If the mass is zero, no suitable W-bjet pair was found in this instance!
                    
                    if int(massMatrix[i,j]) != 0:

                        massDifference = np.abs(massMatrix[i,j] - topMass_known)

                        if massDifference < diff:

                            diff = massDifference

                            W_id = i
                            bjet_id = j

    if W_id != None:

        return massMatrix[W_id,bjet_id], W_id, bjet_id

    return None, None, None
                    
def topMass(lepton):


    bjets = countbJets(lepton)
    bjetAmount = len(bjets)
    jets = lepton.goodJets

    masses = np.zeros((2, bjetAmount))
    
    # Create a list with the W vectors in it; first W uses first two jets, second W second pair of jets

    wVecs = [lepton.jetVecs[lepton.WjetIds[0]] + lepton.jetVecs[lepton.WjetIds[1]], lepton.jetVecs[lepton.WjetIds[2]] + lepton.jetVecs[lepton.WjetIds[3]]]

    # Loop over all bjets and W's, reconstruct invariant mass of every twobody system    

    for i in range(2):

        for j in range(bjetAmount):

            bjet_id = bjets[j]

            # to pick the right jet, we have to find the according jetId AND make sure that we did not use it in the W mass calculation!
            
            jetId = jets.index(bjet_id)
        
            if jetId not in lepton.WjetIds:

                vec1 = wVecs[i]
                vec1 += lepton.jetVecs[jetId]

                masses[i,j] = vec1.M()

    # Choose the (at most) two invariant masses which are closest resembling the top mass while originating from a W and a btagged jet
    # we do this by looping over the mass matrix, selecting the first mass, looping again and selecting the second mass

    bestTopMass, w1, bjet1 = selectBest(masses, bjetAmount)
    secondTopMass, _, _ = selectBest(masses, bjetAmount, skipids = (w1, bjet1))

    return bestTopMass, secondTopMass
    

