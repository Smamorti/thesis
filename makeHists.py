from __future__ import division
import ROOT
from plotVariables import lepton, goodJet, diLeptonMass
import plotVariables
import numpy as np
import time
from cuts import cuts

def initializeHist(hist, name, nbins, llim, ulim):

    hist = ROOT.TH1F(name," ", nbins, llim, ulim)
    hist.Sumw2()
    return hist

def initializeStacked(hist, name):

    hist = ROOT.THStack(name," ")
    return hist

def calcWeight(filename, xSec, lumi = 41.53):

    hCounter = ROOT.TH1F("hCounter","Events Counter",1 ,0 ,1 )
    hCounter = filename.Get("blackJackAndHookers/hCounter")
    totalEvents = hCounter.GetBinContent(1)

    return 1000 * xSec * lumi / totalEvents #times 1000 because cross section is given in picobarn and not in femtobarn!  

def addOverflowbin(hist):

    nbins = hist.GetNbinsX()
    hist.SetBinContent(nbins, hist.GetBinContent(nbins) + hist.GetBinContent(nbins + 1))
    

def fillHist(f, xSec, histList, plotList, year, seperateZ = False, histListNotZ = None): 

    start = time.time()

    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    
    weight = calcWeight(f, xSec, lumi)
    tree = f.Get("blackJackAndHookers/blackJackAndHookersTree")
    
    count = tree.GetEntries()

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

#        progress += 1 # To stop testing, just comment this line out. Maybe have it as an argument or so?

        if progress / float(count) > 0.01:
            
            break


        #for MVA plot
        cutList = ["lPogLoose", "twoPtLeptons", "lEta", "justTwoLeptons", "twoOS", "njets", "nbjets", "twoSF", "onZ"]
        #cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "justTwoLeptons", "twoOS", "njets", "nbjets", "twoSF", "onZ"]
   
        leptons = None
        event = cuts(tree, range(nLight), range(nJets))

        for i in range(len(cutList)):

            # from here on out, nLight is an array with all valid nLight values                                                                                                                           
   
            validEvent, nLight, nJets = getattr(cuts, cutList[i])(event)

            if validEvent:

                event = cuts(tree, nLight, nJets)
                
                if i == len(cutList) - 1:

                    lepton1 = lepton(tree, nLight[0], checknJets = True, calcWmass = True, nJets = nJets)
                    lepton2 = lepton(tree, nLight[1], checknJets = False)
                    
                    for k in range(len(plotList)):

                        hist = histList[k]

                        getattr(plotVariables, plotList[k])(lepton1, lepton2, hist, tree._weight * weight)
                        
                    #getattr(plotVariables, "geen2W")(lepton1, lepton2, hist, tree._weight * weight)
            else:

                break

    for hist in histList:
        
        #addOverflowbin(hist)
        print("Entries: {}".format(hist.GetEntries()))
        
        totalContent = 0
        
        nbins = hist.GetNbinsX()

        for bin in range(nbins + 2): #including under- and overflowbin
        
            totalContent += hist.GetBinContent(bin)

        print("Total hist content: {}".format(totalContent))
                
    print("Time elapsed: {} seconds".format((time.time() - start)))
        

def fillStacked( histList):
    
    for i in range(len(histList) - 1):
        
        for j in range(len(histList[-1])):
                    
            histList[-1][j].Add(histList[i][j])

def fillColor(histList, colorList):

 
    for i in range(len(colorList)): # loop over different sources
        
        for j in range(len(histList[i])): # loop over different histograms
        
            histList[i][j].SetFillColor(colorList[i])

def makeLegend(nameList, histList, position = (0.7, 0.7, 0.9, 0.9)):
    
    #x1, y1, x2, y2 = position[0], position[1], position[2], position[3]
    leg = ROOT.TLegend(position[0], position[1], position[2], position[3])
    
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

