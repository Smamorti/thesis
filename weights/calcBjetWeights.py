from ROOT import TFile, TF1, gROOT, TList
import ROOT
import numpy as np
import sys
from optparse import OptionParser
import os

######

# 1) only have udsg in csv file, for other SF = 1?
# 2) what if the jet eta/pt does not fall within the required ranges?
#        remember that for every jet the pt is > 30 and abs(eta) < 2.4
#        --> should I care about jet pt/eta? 
# 3) basically same question, but for the discriminant value



#####


## TO DO 

# Read in the csv ONCE when starting the making of histos
# From the csv, select the formula(s) corresponding to the region we want to look for
#    For example: loose tagging, inclusive and the up-correction leaves you w/ only 1 formula!
#
# In the csv file, one should not care about the eta values or discriminant values
# formula purely based on hadronFalvor and pt range
#
# sysType: add to arg parser
# measurementType: to do some pre-cleaning, we will give ALL arrays to final program, just less entries
# operatingPoint: probably not worth adding to argparser, only keep loose, hardcode
#
# make function "getBtagArrays" --> returns measurementType, pt low, pt up, hadronFlavor and formulas
#


# bTagEff_loose_udsg
# bTagEff_loose_charm
# bTagEff_loose_beauty
# open these in another place, probably leptonPlots.py!


parser = OptionParser()
parser.add_option("-c", "--csv", default = "DeepCSV_94XSF_WP_V4_B_F.csv", help = "input csv file?")
options, args = parser.parse_args(sys.argv[1:])

def getWeightFormula(formula, i):

    gROOT.ProcessLine('#include <string>')
    gROOT.ProcessLine('TF1 f'+str(i)+'("f'+str(i)+'", '+formula.strip()+');')     

    return getattr(ROOT, 'f'+str(i))

def getBtagArrays(sysType):

    csvFile = "DeepCSV_94XSF_WP_V4_B_F.csv"

    OperatingPoint, measurementType, sysTypes, jetFlavor, etaMin, etaMax, ptMin, ptMax, discrMin, discrMax, formulas= np.loadtxt(options.csv, unpack = True, skiprows = 1, delimiter = ', ', dtype = str)

    keepThese = (sysTypes == sysType) & (measurementType == 'comb') & (OperatingPoint== '0')
#    keepThese = (sysTypes == sysType) & ((measurementType == 'incl') | (measurementType == 'comb'))& (OperatingPoint== '0')

    forms = formulas[keepThese]

    mesTypes = measurementType[keepThese]

    ptLow = ptMin[keepThese]

    ptHigh = ptMax[keepThese]

    hadronFlavor = jetFlavor[keepThese]

    tformulas = TList()

    for i in range(len(forms)):

        f = getWeightFormula(forms[i], i)

        tformulas.Add(f)
    
    inclForm = (sysTypes == sysType) & (measurementType == 'incl') & (OperatingPoint== '0')

    inclFormula = getWeightFormula(formulas[inclForm][0], 'incl')

    return mesTypes, hadronFlavor, ptLow, ptHigh, tformulas, inclFormula


# def calcSF(tree, nJets, measurementTypes, jetFlavors, ptLow, ptHigh, tformulas, inclusiveFormula, JEC):

#     # hardcoded that there is always just one formula for the inclusive part!

#     SFs = []

#     for i in nJets:

#         jetFlavor = tree._jetHadronFlavor[i]
        
#         if JEC == 'nominal':

#             jetPt = tree._jetPt[i]

#         elif JEC == 'up':

#             jetPt = tree._jetPt_JECUp[i]

#         elif JEC == 'down':

#             jetPt = tree._jetPt_JECDown[i]

#         if jetFlavor == 0:

#             SF = inclusiveFormula.Eval(jetPt)

#         else:

#             if jetFlavor == 4:

#                 valid = (jetFlavors == 1)

#             else:

#                 valid == (jetFlavors == 0)

#             ptMax = ptHigh[valid]
#             tforms = tformulas[valid]
        

#             print(ptHigh)
#             print(valid)
#             print(ptMax)

#             j = 0

#             while jetPt > ptMax[j] and j < len(ptMax) - 1:

#                 j += 1

#             SF = tforms[j].Eval(jetPt)

#         SFs.append(SF)

#     return SFs
        
# def calcEfficiencies(tree, nJets, udsgHist, cHist, bHist, JEC):

#     effList = []

#     for i in nJets:
        
#         jetFlavor = tree._jetHadronFlavor[i]

#         if JEC == 'nominal':

#             jetPt = tree._jetPt[i]

#         elif JEC == 'up':

#             jetPt = tree._jetPt_JECUp[i]

#         elif JEC == 'down':

#             jetPt = tree._jetPt_JECDown[i]

#         eta = np.absolute(tree._jetEta[i])

#         if jetFlavor == 0:

#             effList.append(udsgHist.GetbinContent(jetPt, eta))

#         elif jetFlavor == 4:

#             effList.append(cHist.GetbinContent(jetPt, eta))

#         elif jetFlavor == 5:

#             effList.append(bHist.GetbinContent(jetPt, eta))

#     return effList




# def calcEffandSR(tree, nJets, udsgHist, cHist, bHist, jetFlavors, ptHigh, tformulas, inclusiveFormula, JEC):

#     effList = []
#     SFs = []

#     for i in nJets:
        
#         jetFlavor = tree._jetHadronFlavor[i]

#         if JEC == 'nominal':

#             jetPt = tree._jetPt[i]

#         elif JEC == 'up':

#             jetPt = tree._jetPt_JECUp[i]

#         elif JEC == 'down':

#             jetPt = tree._jetPt_JECDown[i]

#         eta = np.absolute(tree._jetEta[i])

#         if jetFlavor == 0:

#             effList.append(udsgHist.GetbinContent(jetPt, eta))
#             SF = inclusiveFormula.Eval(jetPt)

#         else:

#             if jetFlavor == 4:

#                 effList.append(cHist.GetbinContent(jetPt, eta))
#                 valid = (jetFlavors == 1)


#             else:

#                 effList.append(bHist.GetbinContent(jetPt, eta))
#                 valid == (jetFlavors == 0)


#             ptMax = ptHigh[valid]
#             tforms = tformulas[valid]
        
#             print(ptHigh)
#             print(valid)
#             print(ptMax)

#             j = 0

#             while jetPt > ptMax[j] and j < len(ptMax) - 1:

#                 j += 1

#             SF = tforms[j].Eval(jetPt)
            
#         SFs.append(SF)


#     return effList, SFs




def calcBtagWeight(tree, nJets, udsgHist, cHist, bHist, jetFlavors, ptHigh, tformulas, inclusiveFormula, JEC):

    pMC = 1
    pData = 1

    for i in nJets:
        
        jetFlavor = tree._jetHadronFlavor[i]

        if JEC == 'nominal':

            jetPt = tree._jetPt[i]

        elif JEC == 'up':

            jetPt = tree._jetPt_JECUp[i]

        elif JEC == 'down':

            jetPt = tree._jetPt_JECDown[i]

        eta = np.absolute(tree._jetEta[i])

        if jetFlavor == 0:

            eff = udsgHist.GetbinContent(jetPt, eta)
            SF = inclusiveFormula.Eval(jetPt)

        else:

            if jetFlavor == 4:

                eff = cHist.GetbinContent(jetPt, eta)
                valid = (jetFlavors == 1)


            else:

                eff = bHist.GetbinContent(jetPt, eta)
                valid == (jetFlavors == 0)


            ptMax = ptHigh[valid]
            tforms = tformulas[valid]
        
            print(ptHigh)
            print(valid)
            print(ptMax)

            j = 0

            while jetPt > ptMax[j] and j < len(ptMax) - 1:

                j += 1

            SF = tforms[j].Eval(jetPt)
            
        pMC, pData = updateBtagWeight(tree, i, eff, SF, pMC, pData)


    return pData / pMC



def updateBtagWeight(tree, i, eff, SF, pMC, pData):

    if tree._jetDeepCsv_b[i] > 0.4941:

        pMC *= eff
        pData *= (SF * eff)

    else:

        pMC *= (1 - eff)
        pData *= (1 - Sf * eff)

    return pMC, pData

# def calcBtagWeight(tree, nJets, effList, SFlist):

#     pMC = 1
#     pData = 1

#     for i in nJets:

#         if tree._jetDeepCsv_b[i] > 0.4941:

#             pMC *= effList[i]
#             pData *= (SFlist[i] * effList[i])

#         else:

#             pMC *= (1 - effList[i])
#             pData *= (1 - SFlist[i]* effList[i])

#     return pData / pMC


# for testing

if __name__ == "__main__":

    measurementTypes, jetFlavors, ptLow, ptHigh, tformulas, inclFormula = getBtagArrays(sysType = 'up')

    print(measurementTypes)
    print(jetFlavors)
    print(ptLow)
    print(ptHigh)

    print(inclFormula.Eval(50))

    for x in tformulas:

        print(x.Eval(50))

