from __future__ import division
from plotVariables import lepton, goodJet, diLeptonMass
import plotVariables
import numpy as np
import time
from cuts import cuts
import sys
from ROOT import TFile, TH1F, THStack, TLegend, TList
from utilities.makeParamArray import makeParamArray

def initializeHist(hist, name, nbins, llim, ulim):

    hist = TH1F(name," ", nbins, llim, ulim)
    hist.Sumw2()
    return hist

def initializeStacked(hist, name):

    hist = THStack(name," ")
    return hist

def calcWeight(filename, xSec, lumi = 59.74, fitWeight = None):

    hCounter = TH1F("hCounter","Events Counter",1 ,0 ,1 )
    hCounter = filename.Get("blackJackAndHookers/hCounter")
    totalEvents = hCounter.GetBinContent(1)

    #times 1000 because cross section is given in picobarn and not in femtobarn!  

    if fitWeight:

        return 1000 * xSec * lumi * fitWeight/ totalEvents

    else:

        return 1000 * xSec * lumi / totalEvents

def addOverflowbin(hist):

    nbins = hist.GetNbinsX()
    hist.SetBinContent(nbins, hist.GetBinContent(nbins) + hist.GetBinContent(nbins + 1))

def fillHist(channels, xSecDict, locationDict, histList, plotList, year, testing, printHists, model, algo, workingPoint, useWorkingPoint, isData = False, fitWeight = None, pileupWeights = None, JEC = 'nominal'):


    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    for k in range(len(channels)):

        start = time.time()

        channel = channels[k]

        if isData:

            f = TFile.Open(channel)

            weight = 1

        else:

            f = TFile.Open(locationDict[channel])

            weight = calcWeight(f, xSecDict[channel], lumi, fitWeight = fitWeight)

        tree = f.Get("blackJackAndHookers/blackJackAndHookersTree")

        count = tree.GetEntries()

        print(count)

        # setup progressbar

        toolbar_width = 100

        sys.stdout.write("File %d/%d. Progress: [%s]" % (k+1, len(channels), " " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['  
        progress = 0
        toolbarProgress = 0

        total = count

        if testing == 'yes':

            total *= 0.01

        for _ in tree:

            # make script compatible with both 2017 and 2018 files

            if type(tree._nL) == int:

                nL = tree._nL
                
                if not isData:
                    gen_nL = tree._gen_nL
                
                nLight = tree._nLight
                nJets = tree._nJets

            else:

                nL = ord(tree._nL)
                
                if not isData:
                    gen_nL = ord(tree._gen_nL)
                
                nLight = ord(tree._nLight)
                nJets = ord(tree._nJets)

            progress += 1

            if progress / float(count) > 0.01 and testing == 'yes':
                print(progress / float(count))
                break

            if progress / total > toolbarProgress / toolbar_width:
                toolbarProgress += 1
                sys.stdout.write("-")
                sys.stdout.flush()

            if isData:

                # if we are dealing with a data event, we want to check for the triggers first!

                if not (tree._passTrigger_e or tree._passTrigger_ee or tree._passTrigger_m or tree._passTrigger_mm):

                    continue

            cutList = ["lPogLoose", "lMVA", "twoPtLeptons", "lEta", "justTwoLeptons", "twoOS", "njets", "nbjets", "twoSF", "onZ"]

            leptons = None
            event = cuts(tree, range(nLight), range(nJets), JEC)

            for i in range(len(cutList)):

                # from here on out, nLight is an array with all valid nLight values                                                                                 
                validEvent, nLight, nJets = getattr(cuts, cutList[i])(event)

                if validEvent:

                    event = cuts(tree, nLight, nJets, JEC)

                    if i == len(cutList) - 1:
                        
                        # for plotting the model output, make an exception in the plotvariables thingy

                        # make array of used parameters in model training

                        if '.h5' in algo:

                            output = model.predict(makeParamArray(tree, nLight, nJets, JEC))[0][0]

                        else:

                            from xgboost import DMatrix

                            matrix = DMatrix(makeParamArray(tree, nLight, nJets, JEC))
                            output = model.predict(matrix)

                        lepton1 = lepton(tree, nLight[0], JEC, checknJets = True, calcWmass = True, nJets = nJets)
                        lepton2 = lepton(tree, nLight[1], JEC, checknJets = False)

                        for k in range(len(plotList)):

                            hist = histList[k]

                            if plotList[k] == 'modelOutput' or plotList[k] == 'modelOutput2':

                                if isData:

                                    getattr(plotVariables, plotList[k])(hist, weight, output)

                                else:

                                    getattr(plotVariables, plotList[k])(hist, tree._weight * weight * pileupWeights.GetBinContent(int(tree._nTrueInt)), output )


                            else:

                                if isData:

                                        getattr(plotVariables, plotList[k])(lepton1, lepton2, hist, weight)

                                else:

                                    getattr(plotVariables, plotList[k])(lepton1, lepton2, hist, tree._weight * weight * pileupWeights.GetBinContent(int(tree._nTrueInt)))               

                else:

                    break

        sys.stdout.write("]\n") # this ends the progress bar

        f.Close()

        print("Time elapsed: {} seconds".format((time.time() - start)))

    if printHists == 'yes':

        for hist in histList:

            #addOverflowbin(hist)
            print("Entries: {}".format(hist.GetEntries()))

            totalContent = 0

            nbins = hist.GetNbinsX()

            for bin in range(nbins + 2): #including under- and overflowbin

                totalContent += hist.GetBinContent(bin)

            print("Total hist content: {}".format(totalContent))
                
    
def fillStacked( histList):
    
    for i in range(len(histList) - 1):
        
        for j in range(len(histList[-1])):
                    
            histList[-1][j].Add(histList[i][j])

def fillColor(histList, colorDict, typeList): 

    for i in range(len(typeList)): # loop over different sources
        
        source = typeList[i]

        for j in range(len(histList[i])): # loop over different histograms
        
            histList[i][j].SetFillColor(colorDict[source])


def makeLegend(typeList, histList, texDict, dataList, position = (0.8, 0.7, 0.9, 0.9)):
    
    leg = TLegend(position[0], position[1], position[2], position[3])
    
    for i in range(len(typeList)):
    
        source = typeList[i]
        label = texDict[source]

        leg.AddEntry(histList[i][0], label, "f")
       
    leg.AddEntry(dataList[0][0], "data", "f")

    return leg



# def makeLegend(typeList, histList, texDict, position = (0.8, 0.7, 0.9, 0.9)):
    
#     leg = TLegend(position[0], position[1], position[2], position[3])
    
#     for i in range(len(typeList)):
    
#         source = typeList[i]
#         label = texDict[source]

#         leg.AddEntry(histList[i][0], label, "f")
       
#     return leg



def fillTList(channels, plotList, binList, extra = ""):

    #
    # Makes a TList of TLists: A TList per source, bundled together into one TList
    # Fills the TLists per source with the desired histograms, given by the plotList
    # In the end, a TList with Stacked histograms is added
    # The binlist is a list of tuples, each containing the amount of bins, ulim and llim per element in the plotList
    # The extra string is there to for instance choose wether you want an extra part to the name or not (such as Z or notZ)
    #

    tlist = TList()

    for channel in channels:

        temp = TList()

        for i in range(len(plotList)):

            nbins, llim, ulim = binList[i]
            name = "h_" + plotList[i] + "_" + channel + extra
            temp.Add(initializeHist(name, plotList[i] + "_" + channel + extra, nbins, llim, ulim))

        tlist.Add(temp)
    
    temp = TList()
        
    for i in range(len(plotList)):
        
        name = "h_" + plotList[i] + "_Stacked" + extra
        temp.Add(THStack(name, " "))

    tlist.Add(temp)

    return tlist

