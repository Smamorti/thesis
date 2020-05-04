from ROOT import TFile, TF1, gROOT, TList, TCanvas
import ROOT
import numpy as np


def loadBtagHists(f):

    udsg = f.Get("bTagEff_loose_udsg").Clone()
    c = f.Get("bTagEff_loose_charm").Clone()
    b = f.Get("bTagEff_loose_beauty").Clone()

    return udsg, c, b


def getWeightFormula(formula, i):

    gROOT.ProcessLine('#include <string>')
    gROOT.ProcessLine('TF1 f'+str(i)+'("f'+str(i)+'", '+formula.strip()+');')     

    return getattr(ROOT, 'f'+str(i))

def getBtagArrays(csvFile, sysType):

    OperatingPoint, measurementType, sysTypes, jetFlavor, etaMin, etaMax, ptMin, ptMax, discrMin, discrMax, formulas= np.loadtxt(csvFile, unpack = True, skiprows = 1, delimiter = ', ', dtype = str)

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


def calcBtagWeight(tree, nJets, udsgHist, cHist, bHist, jetFlavors,ptLow, ptHigh, tformulas, inclusiveFormula, JEC):

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

        croppedPt = min( max(25, jetPt), 599 )
        croppedEta = min( eta , 2.39 )

        if jetFlavor == 0:

            eff = udsgHist.GetBinContent(udsgHist.FindBin(croppedPt, croppedEta))
            SF = inclusiveFormula.Eval(jetPt)

        else:

            if jetFlavor == 4:

                eff = cHist.GetBinContent(cHist.FindBin(croppedPt, croppedEta))
                valid = (jetFlavors == '1')


            elif jetFlavor == 5:

                eff = bHist.GetBinContent(bHist.FindBin(croppedPt, croppedEta))
                valid = (jetFlavors == '0')
        
            ptLow = ptLow.astype(float)
            ptHigh = ptHigh.astype(float)


            for k in range(len(ptHigh)):

                if valid[k]:

                    if ptLow[k] < jetPt < ptHigh[k]:

                        index = k
                        break

                    elif jetPt > np.amax(ptHigh):

                        maxVals = np.argwhere(ptHigh == np.amax(ptHigh))

                        index = maxVals[0][0] if valid[maxVals[0][0]] else maxVals[1][0]
                        break

            # if jetPt > 1000:
            if not valid[index]:
                print('--------------------------')
                print(jetFlavor)
                print(jetFlavors)

                print(ptHigh)
                print(valid)

                print(ptLow[index], jetPt, ptHigh[index])
                
                print(index)
                print(valid[index])
            

            SF = tformulas[index].Eval(jetPt)
            
        pMC, pData = updateBtagWeight(tree, i, eff, SF, pMC, pData)


    return pData / pMC



def updateBtagWeight(tree, i, eff, SF, pMC, pData):

    if tree._jetDeepCsv_b[i] > 0.4941:

        pMC *= eff
        pData *= (SF * eff)

    else:

        pMC *= (1 - eff)
        pData *= (1 - SF * eff)

    return pMC, pData



# for testing

if __name__ == "__main__":

    # u, c, b = loadBtagHists("bTagEff_looseLeptonCleaned_2018.root")

    rootfile = "bTagEff_looseLeptonCleaned_2018.root"

    f = TFile.Open(rootfile)

    l = loadBtagHists(f)

    udsg, c, b = l

#    udsg, c, b = loadBtagHists(f)

    can = TCanvas("c2e","c2e",600,400)

    udsg.Draw("E")
    c.Draw("E SAME")
    b.Draw("E SAME")

    can.SaveAs("test2DHists.pdf")

    measurementTypes, jetFlavors, ptLow, ptHigh, tformulas, inclFormula = getBtagArrays(sysType = 'up')

    print(measurementTypes)
    print(jetFlavors)
    print(ptLow)
    print(ptHigh)

    print(inclFormula.Eval(50))

    for x in tformulas:

        print(x.Eval(50))

