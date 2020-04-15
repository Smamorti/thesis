from ROOT import TCanvas, TLegend, THStack, TList, TPaveText
import ROOT.gStyle as gStyle
import ROOT.gPad as gPad
import pickle
import numpy as np

def countSignal(inputFile, histList, typeList, xLabelList):
    
    index_signal = typeList.index('ttZ')
    index_SR = np.where(xLabelList == 'SR')[0][0]

    inputName = inputFile.split('/')[1]

    hist = histList[index_signal][index_SR]


    print('----------------------------------------------------------------------')

    print('Amount of signal events for {}:'.format(inputName))

    print('=5 jets, =1 bjet: {}'.format(np.around(hist.GetBinContent(1), 2)))
    print('=5 jets, >=2 bjets: {}'.format(np.around(hist.GetBinContent(2), 2)))
    print('>=6 jets, =1 bjet: {}'.format(np.around(hist.GetBinContent(3), 2)))
    print('>=6 jets, >=2 bjets: {}'.format(np.around(hist.GetBinContent(4), 2)))

    print('Total amount of signal events: {}'.format(np.around(hist.GetBinContent(1) + hist.GetBinContent(2) + hist.GetBinContent(3) + hist.GetBinContent(4), 2)))

    print('----------------------------------------------------------------------')


def countSignBkg(inputFile, histList, typeList, xLabelList):

    wp = inputFile.split('/')[1].split('_')[-1].replace('wp=', '')
    index_SR = np.where(xLabelList == 'SR')[0][0]

    index_signal = typeList.index('ttZ')

    hist = histList[index_signal][index_SR]

    totSign = hist.GetBinContent(1) + hist.GetBinContent(2) + hist.GetBinContent(3) + hist.GetBinContent(4)

    totEvents = 0

    for i in range((len(histList))):


        tempHist = histList[i][index_SR]
        totEvents += tempHist.GetBinContent(1) + tempHist.GetBinContent(2) + tempHist.GetBinContent(3) + tempHist.GetBinContent(4) 

    bkgEvents = totEvents - totSign

    print('{}\t{}\t{}\t{}\t{}'.format(wp, totSign, bkgEvents, totSign/bkgEvents, totEvents))

def makePath(histListPath):

    if not 'wp' in histListPath:

        return 'plots'

    else:
        
        algo = histListPath.split('/')[1]

        return 'plots/{}'.format(algo)

def makeLegend(typeList, histList, texDict, position = (0.8, 0.7, 0.89, 0.89)):

    leg = TLegend(position[0], position[1], position[2], position[3], '', 'NBNDC')

    leg.SetBorderSize(0)

    for i in range(len(typeList)):

        source = typeList[i]
        label = texDict[source]

        leg.AddEntry(histList[i][0], label, "f")

    return leg


def makeCanvas(horizontal, vertical):

    c = TCanvas("c", "c", 550 * horizontal, 400 * vertical)
    c.Divide(horizontal, vertical)

    return c

def fillSubCanvas(subCanvas, hist, xlabel, ylabel, leg, leg2, title = None, logscale = 1):

    subCanvas.SetLogy(logscale)

    if title:

        subCanvas.SetTitle(title)

    hist.Draw("HIST")

    hist.GetXaxis().SetTitle(xlabel)
    hist.GetYaxis().SetTitle(ylabel)

    # hardcoded for now                                                                                                                                                                                     
    if xlabel == "flavComp":

        hist.GetXaxis().SetBinLabel(1, "ee")
        hist.GetXaxis().SetBinLabel(2, "#mu#mu")
        leg2.Draw()

    elif xlabel== "SR":

        hist.GetXaxis().SetBinLabel(1, "=5 jets,=1 bjets")
        hist.GetXaxis().SetBinLabel(2, "=5 jets,>=2 bjets")
        hist.GetXaxis().SetBinLabel(3, ">=6 jets,=1 bjets")
        hist.GetXaxis().SetBinLabel(4, ">=6 jets,>=2 bjets")
        leg.Draw()
    # hardcoded for now                                                                                                                                                                                     
    elif xlabel == "leptonMVA l1" or xlabel == "leptonMVA l2" or xlabel == "leptonMVA" or xlabel == "model output":

        leg2.Draw()

    else:

        leg.Draw()

    subCanvas.Update()

def differentOrder(histList, i, hist, order = [2, 0, 1]):

    for j in order:

        hist.Add(histList[j][i])

def initializeStacked(hist, name):

    hist = THStack(name," ")
    return hist

def makeStackedList(plotList):

    temp = TList()

    for i in range(len(plotList)):

        name = "h_" + plotList[i] + "_Stacked"
        temp.Add(THStack(name, " "))

    return temp

def makeHistList(sources):

    temp = TList()

    for source in sources:

        sourceHists = pickle.load(file(source))
        
        temp.Add(sourceHists)

    return temp

def fillStacked(sources, stackedList):

    for source in sources:

        sourceHists = pickle.load(file(source))

        for j in range(len(stackedList)):

            stackedList[j].Add(sourceHists[j])

        del sourceHists

def plot(plotList, histList, xLabelList, yLabelList, leg, leg2, title =  "", logscale = 1, year = "2018", folder = 'plots/'):

    for i in range(len(plotList)):
        
        if logscale:
            scale = "log"
        else:
            scale = "linear"

        c = makeCanvas(1, 1)
        filename = "{}/Hist_{}_{}_{}".format(folder, year, plotList[i], scale)
        fillSubCanvas(c, histList[i], xLabelList[i], yLabelList[i], leg, leg2, title, logscale)

        # workingPoint = "0.50"
        # wp = TPaveText()
        # wp.SetX1NDC(0.25)
        # wp.SetY1NDC()
        # wp.SetX2NDC()
        # wp.SetY2NDC()

        # TO DO: Add option to customize text!

        text1 = "CMS Preliminary"
        label1 = TPaveText()
        label1.SetX1NDC(gStyle.GetPadLeftMargin()-0.043)
        label1.SetY1NDC(1.0-gStyle.GetPadTopMargin())
        label1.SetX2NDC(1.0-gStyle.GetPadRightMargin())
        label1.SetY2NDC(1.0)

        #label1.SetTextFont(42)
        label1.AddText(text1)
        label1.SetFillStyle(0)
        label1.SetBorderSize(0)
        label1.SetTextSize(0.04)
        label1.SetTextAlign(13)
        label1.Draw()

        text2 = " %2.1f fb^{-1} (#sqrt{s} = %2.f TeV)" % (59.74, 13)
        label2 = TPaveText()
        label2.SetX1NDC(gStyle.GetPadLeftMargin())
        label2.SetY1NDC(1.0-gStyle.GetPadTopMargin())
        label2.SetX2NDC(1.0-gStyle.GetPadRightMargin() + 0.043)
        label2.SetY2NDC(1.0)

        label2.SetTextFont(42)
        label2.AddText(text2)
        label2.SetFillStyle(0)
        label2.SetBorderSize(0)
        label2.SetTextSize(0.04)
        label2.SetTextAlign(33)
        label2.Draw()

        c.Update()
        
        gPad.SetTickx()
        gPad.SetTicky()
        
        c.Update()

        c.SaveAs(filename + ".pdf")
        c.SaveAs(filename + ".png")
        c.Close()

        # # hardcoded (for now?)

        # if xLabelList[i] == "m(ll) (GeV)":

        #     hist = THStack(xLabelList[i]," ")
        #     differentOrder(histList, i, hist, order = [2, 0, 1])

        #     c = makeCanvas(1, 1)
        #     filename = "plots/Hist_{}_{}_{}_{}".format(year, plotList[i], scale, "ttunder")
        #     fillSubCanvas(c, hist, xLabelList[i], yLabelList[i], leg, leg2, title, logscale)
        #     c.SaveAs(filename + ".pdf")
        #     c.SaveAs(filename + ".png")
        #     c.Close()
