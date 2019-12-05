#
# generate a cutflow table
#

import ROOT
from plotVariables import lepton
from plotVariables import goodJet
from plotVariables import diLeptonMass
import plotVariables
import numpy as np

###########################                                                                                                                                                                                 
########## CUTS ###########                                                                                                                                                                                 
###########################                                                                                                                                                                                 

def lMVA(tree, _nLight):

    return tree._leptonMvatZq[_nLight] > 0.4



def weight_TotalEvents(filename, xSec, lumi = 59.74):

    hCounter = ROOT.TH1F("hCounter","Events Counter",1 ,0 ,1 )
    hCounter = filename.Get("blackJackAndHookers/hCounter")
    totalEvents = hCounter.GetBinContent(1)

    return 1000 * xSec * lumi / totalEvents, totalEvents

def cutflow(f, xSec, year):

    filename = ROOT.TFile.Open(f)

    if year == "2017":
        lumi = 41.53
    elif year == "2018":
        lumi = 59.74

    weight, initialEvents = weight_TotalEvents(filename, xSec, lumi)
    tree = filename.Get("blackJackAndHookers/blackJackAndHookersTree")

    afterMVA = 0
    afterMVA_w = 0
    
    for _ in tree:

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


        for i in range(nLight):

            if not lMVA(tree, i):
                break
            
            if i == nLight - 1:
                afterMVA += 1
                afterMVA_w += tree._weight * weight

    print(tree.GetEntries())
    print(initialEvents)
    print(afterMVA)    
    print(afterMVA_w)


stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"

year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)


channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str)

xSecs = xSecs.astype(float)


cutflow("/user/mniedzie/Work/ntuples_ttz_2L_ttZ_2018/_ttZ_DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_MiniAOD2018.root", xSecs[1], year)


###########################                                                                                                                                                                               
########## CUTS ###########                                                                                                                                                                               
###########################

def lMVA(tree, nLight):

    return tree._leptonMvatZq[_nLight] > 0.4
