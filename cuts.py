from plotVariables import lepton
from plotVariables import goodJet
from plotVariables import diLeptonMass
import numpy as np

class cuts:

    def __init__(self, tree, nLight, nJets, JEC = 'nominal'):

        self.tree = tree
        self.nLight = nLight
        self.nJets = nJets
        self.JEC = JEC

    def lMVA(self):

        validnLight = []

        for i in self.nLight:

#            if self.tree._leptonMvatZq[i] > 0.4:
            if self.tree._leptonMvaTTH[i] > 0.4:

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
                
            elif self.tree._lFlavor[i] == 0 and np.absolute(self.tree._lEta[i]) <= 2.5:
                # other eta requirement for electrons

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

            if goodJet(self.tree, i, self.JEC):
                
                # Now we implement the last good jet criterion, namely having DeltaR > 0.4 wrt the two prompt leptons
                
                for lep in self.nLight:


                    D_phi = self.tree._jetPhi[i] - self.tree._lPhi[lep]
                    D_eta = self.tree._jetEta[i] - self.tree._lEta[lep]

                    DeltaR = np.sqrt(D_phi**2 + D_eta**2)
                    #print(DeltaR)
                    if DeltaR < 0.4:
                        
                        break
                    
                    if lep == self.nLight[-1]:
                        #print(DeltaR)
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

        lepton1 = lepton(self.tree, self.nLight[0], self.JEC, checknJets = False)    
        lepton2 = lepton(self.tree, self.nLight[1], self.JEC, checknJets = False)

        if 81 < diLeptonMass(lepton1, lepton2) < 101:

            return True, self.nLight, self.nJets

        return False, self.nLight, self.nJets
