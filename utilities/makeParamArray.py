import numpy as np
import sys
sys.path.append("..")
from plotVariables import lepton, calculateDeltaR, H_t

def makeParamArray(tree, nLight, nJets, JEC):

    paramList = []

    # branch_names = [
    # 'lPt1', 'lPt2',
    # 'lEta1', 'lEta2',
    # 'lPhi1', 'lPhi2',
    # 'DeltaR_1', 'DeltaR_b1', 'DeltaR_2', 'DeltaR_b2',
    # 'njets', 'nbjets', 'jetDeepCsv_b1',
    # 'jetPt1', 'jetEta1', 'jetPhi1',
    # 'jetPt2', 'jetEta2', 'jetPhi2',
    # 'jetPt3', 'jetEta3', 'jetPhi3',
    # 'jetPt4', 'jetEta4', 'jetPhi4',
    # 'jetPt5', 'jetEta5', 'jetPhi5',
    # 'mW1', 'mtop1',
    # 'MET', 'H_t',
    # 'I_rel1', 'I_rel2'
    # ]


    # maybe try to use the lepton classes to speed this up? but first try to get it to work 

    paramList.append(tree._lPt[nLight[0]])
    paramList.append(tree._lPt[nLight[1]])
    paramList.append(tree._lEta[nLight[0]])
    paramList.append(tree._lEta[nLight[1]])
    paramList.append(tree._lPhi[nLight[0]])
    paramList.append(tree._lPhi[nLight[1]])

    # make two lepton objects to calculate DeltaR, mW, mtop                                                                                                                                                                 

    lepton1 = lepton(tree, nLight[0], JEC, checknJets = True, calcWmass = True, nJets = nJets)
    lepton2 = lepton(tree, nLight[1], JEC, checknJets = False)

    # calculate all DeltaR values                                                                                                                                                                                           

    paramList.append(calculateDeltaR(lepton1, lepton1, b = False))
    paramList.append(calculateDeltaR(lepton1, lepton1, b = True))
    paramList.append(calculateDeltaR(lepton1, lepton2, b = False))
    paramList.append(calculateDeltaR(lepton1, lepton2, b = True))


    paramList.append(len(nJets))


    nbjets = 0

    for i in nJets:

        if tree._jetDeepCsv_b[i] > 0.4941:

            nbjets += 1

    paramList.append(nbjets)
    paramList.append(tree._jetDeepCsv_b[nJets[0]]) #jetDeepCsv_b of leading jet                                                                                                                                        

    # add all jet properties                                                                                   

    if JEC == 'nominal':

        pt0 = tree._jetPt[nJets[0]]
        pt1 = tree._jetPt[nJets[1]]
        pt2 = tree._jetPt[nJets[2]]
        pt3 = tree._jetPt[nJets[3]]
        pt4 = tree._jetPt[nJets[4]]

    elif JEC == 'up':

        pt0 = tree._jetPt_JECUp[nJets[0]]
        pt1 = tree._jetPt_JECUp[nJets[1]]
        pt2 = tree._jetPt_JECUp[nJets[2]]
        pt3 = tree._jetPt_JECUp[nJets[3]]
        pt4 = tree._jetPt_JECUp[nJets[4]]

    elif JEC == 'down':

        pt0 = tree._jetPt_JECDown[nJets[0]]
        pt1 = tree._jetPt_JECDown[nJets[1]]
        pt2 = tree._jetPt_JECDown[nJets[2]]
        pt3 = tree._jetPt_JECDown[nJets[3]]
        pt4 = tree._jetPt_JECDown[nJets[4]]

    else:

        raise ValueError('invalid JEC option')                                                                                                             

    paramList.append(pt0)
    paramList.append(tree._jetEta[nJets[0]])
    paramList.append(tree._jetPhi[nJets[0]])

    paramList.append(pt1)
    paramList.append(tree._jetEta[nJets[1]])
    paramList.append(tree._jetPhi[nJets[1]])

    paramList.append(pt2)
    paramList.append(tree._jetEta[nJets[2]])
    paramList.append(tree._jetPhi[nJets[2]])

    paramList.append(pt3)
    paramList.append(tree._jetEta[nJets[3]])
    paramList.append(tree._jetPhi[nJets[3]])

    paramList.append(pt4)
    paramList.append(tree._jetEta[nJets[4]])
    paramList.append(tree._jetPhi[nJets[4]])


    # calculate W and top mass                                                                                                                                                                                              

    mW1 = lepton.bestWmass(lepton1)
    mtop1 = lepton.bestTopMass(lepton1)

    if not mtop1:

        mtop1 = 1000

    paramList.append(mW1)
    paramList.append(mtop1)


    # calculate H_t^miss and add it to tree, also add MET and iso                                                                                                                                                                 
    paramList.append(tree._met)
    paramList.append(H_t(lepton1))

    paramList.append(tree._relIso[nLight[0]])
    paramList.append(tree._relIso[nLight[1]])
    
    return np.reshape(np.array(paramList), (1, len(paramList), ))
