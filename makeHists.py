import ROOT
from plotVariables import lepton
from plotVariables import goodJet
from plotVariables import diLeptonMass
import plotVariables
import numpy as np
#from progressBar import progressbar

def initializeHist(hist, name, nbins, llim, ulim):

    hist = ROOT.TH1F(name," ", nbins, llim, ulim)
    return hist

def initializeStacked(hist, name):

    hist = ROOT.THStack(name," ")
    return hist

def calcWeight(filename, xSec, lumi = 41.53):

    hCounter = ROOT.TH1F("hCounter","Events Counter",1 ,0 ,1 )
    hCounter = filename.Get("blackJackAndHookers/hCounter")
    totalEvents = hCounter.GetBinContent(1)

    return 1000 * xSec * lumi / totalEvents #times 1000 because cross section is given in picobarn and not in femtobarn!  


def makeLeptonList(tree, gen_nL):

    leptons = np.array([[[0, 0], [0, 0]],[[0, 0], [0, 0]],[[0, 0], [0, 0]]]) # gen leptons, naming is temporary

    for g in range(gen_nL):


        if tree._gen_lMomPdg[g] == 23:

            if leptons[tree._gen_lFlavor[g],0,1] and not leptons[tree._gen_lFlavor[g],1,1]: # checks if there is already a charge for the first lepton of this flavor, and None for the second lepton   

                if leptons[tree._gen_lFlavor[g],0,1] != tree._gen_lCharge[g]:

                    leptons[tree._gen_lFlavor[g],1,0] = g #set number and charge of first lepton of this flavor                                                                                         
                    leptons[tree._gen_lFlavor[g],1,1] = tree._gen_lCharge[g] #set number and charge of first lepton of this flavor                                                                      


            else:
                leptons[tree._gen_lFlavor[g],0,0] = g #set number and charge of first lepton of this flavor                                                                                             
                leptons[tree._gen_lFlavor[g],0,1] = tree._gen_lCharge[g] #set number and charge of first lepton of this flavor                                                                          

    return leptons



def calcZMass(tree, leptonList):

    invMass = 0

    for j in range(3):
        if leptonList[j,1,1]:
            
            a = leptonList[j,0,0]
            b = leptonList[j,1,0]

            vec1 = ROOT.Math.PtEtaPhiEVector()
            vec2 = ROOT.Math.PtEtaPhiEVector()

            vec1.SetCoordinates(tree._gen_lPt[a], tree._gen_lEta[a], tree._gen_lPhi[a], tree._gen_lE[a])
            vec2.SetCoordinates(tree._gen_lPt[b], tree._gen_lEta[b], tree._gen_lPhi[b], tree._gen_lE[b])

            vec1 += vec2
            invMass = vec1.M()

    return invMass # returns 0 if no invMass could be calculated

def passJetCuts(tree, nJets):

    if nJets < 5:
        
        return False

    jetIds = []
    bjetIds = []

    for j in range(nJets):
        
        if goodJet(tree, j):

            jetIds.append(j)

            if tree._jetDeepCsv_b[j] > 0.4941:

                bjetIds.append(j)

        if len(jetIds) >= 5 and bjetIds:

            return True

    return False


def passEta(tree, _nLight):

    if np.absolute(tree._lEta[_nLight]) > 2.5:

        return False

    if tree._lFlavor[_nLight] == 1:

        if np.absolute(tree._lEta[_nLight]) > 2.4:

            return False

    return True

def passLeptonCuts(tree, _nLight):

#        and tree._lIsPrompt[_nLight]
    if (tree._leptonMvatZq[_nLight] > 0.4 
       and tree._lPt[_nLight] > 20
        and tree._lPOGLoose[_nLight]
        and passEta(tree, _nLight)
        ):
        return True
    return False


def twoPromptLeptons(tree, nLight):

    nPrompt = 0
    promptIds = []
    for j in range(nLight):

        if passLeptonCuts(tree, j):

            nPrompt += 1
            promptIds.append(j)

        if nPrompt > 2:
            
            return False

    if nPrompt == 2:
        
        # check leading lepton pt requirement

        if tree._lPt[promptIds[0]] > 30:
            
            # Check OSSF requirement

            if tree._lFlavor[promptIds[0]] == tree._lFlavor[promptIds[1]] and tree._lCharge[promptIds[0]] == -1 * tree._lCharge[promptIds[1]]:

                #check mll requirement
                lepton1 = lepton(tree, promptIds[0]) # put other properties in this class as well?              
                lepton2 = lepton(tree, promptIds[1], checknJets = False)

                if 81 < diLeptonMass(lepton1, lepton2) < 101:

                    return lepton1, lepton2

    return False


def fillHist(f, xSec, histList, plotList, histZMass, year, seperateZ = False, histListNotZ = None): 

    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    
    weight = calcWeight(f, xSec, lumi)
    tree = f.Get("blackJackAndHookers/blackJackAndHookersTree")
    
    count = tree.GetEntries()


    #progressbar(range(count))

    print(count)
    progress = 0

    for _ in tree:

        # make script compatible with both 2017 and 2018 files

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
        
        # to quickly test the program

        progress += 1 # To stop testing, just comment this line out. Maybe have it as an argument or so?

        if progress / float(count) > 0.01:
            
            break

        # Calculate the Z mass using gen leptons
        
        # For now, skip calculation of Z mass using gen leptons

        # leptons = makeLeptonList(tree, gen_nL)  
        # invMass = calcZMass(tree, leptons)

        # if invMass:
            
        #     #index [0] temporary?
        #     histZMass[0].Fill(invMass, weight * tree._weight)
   

        # maybe put some of this in a seperate function?

        leptons = None

        if passJetCuts(tree, nJets):

            leptons = twoPromptLeptons(tree, nLight)

        if leptons:
            
            #lepList = [[], []]
#            print(tree._lMomPdgId[promptIds[0]] == 23)
            lepton1 = leptons[0] # put other properties in this class as well?
            lepton2 = leptons[1] 
            for k in range(len(plotList)):
                    
                    # if seperateZ:

                    #     # insert way to differentiate Z and non Z leptons

                    #     if Z:

                    #         hist = histList[k]

                    #     else:
                    #         hist = histListNotZ[k]

                hist = histList[k]
                    
                getattr(plotVariables, plotList[k])(lepton1, lepton2, hist, tree._weight * weight)
    for hist in histList:

        print(hist.GetEntries())
                

def fillStacked( histList):
    
    for i in range(len(histList) - 1):
        
        for j in range(len(histList[-1])):
                    
            histList[-1][j].Add(histList[i][j])

def fillColor(histList, colorList):

 
    for i in range(len(colorList)): # loop over different sources
        
        for j in range(len(histList[i])): # loop over different histograms
        
            histList[i][j].SetFillColor(colorList[i])

def makeLegend(nameList, histList):
    
    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    for i in range(len(nameList)):
        
        label = nameList[i]
        leg.AddEntry(histList[i][0], label, "f")
       
    return leg

def fillTList(channels, plotList, binList, extra = ""):

    #
    # Makes a TList of TLists: A TList per source, bundled together into one TList
    # Fills the TLists per source with the desired histograms, given by the plotList
    # In the end, a TList with Stacked histograms is added
    # The binlist is a list of tuples, each containing the amount of bins, ulim and llim per element in the plotList
    # The extra string is there to for instance choose wether you want an extra part to the name or not (such as Z or notZ)
    #

    tlist = ROOT.TList()

    for channel in channels:

        temp = ROOT.TList()
        

        for i in range(len(plotList)):

            nbins, ulim, llim = binList[i]
            name = "h_" + plotList[i] + "_" + channel + extra
            temp.Add(initializeHist(name, plotList[i] + "_" + channel + extra, nbins, ulim, llim))

        tlist.Add(temp)
    
    temp = ROOT.TList()
        
    for i in range(len(plotList)):
        
        name = "h_" + plotList[i] + "_Stacked" + extra
        temp.Add(ROOT.THStack(name, " "))

    tlist.Add(temp)

    return tlist

