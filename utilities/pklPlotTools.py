from __future__ import division
from ROOT import TCanvas, TLegend, THStack, TList, TPaveText, TPolyLine
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

#def makeLegend(typeList, histList, texDict, dataList, position = (0.8, 0.7, 0.89, 0.89)):
def makeLegend(typeList, histList, texDict, dataList, position = (0.8, 0.685, 0.89, 0.875)):

    leg = TLegend(position[0], position[1], position[2], position[3], '', 'NBNDC')

    leg.SetBorderSize(0)

    for i in range(len(typeList)):

        source = typeList[i]
        label = texDict[source]

        leg.AddEntry(histList[i][0], label, "f")

    leg.AddEntry(dataList[0], "data", "ep")

    return leg


# def makeCanvas(horizontal, vertical):

#     c = TCanvas("c", "c", 550 * horizontal, 400 * vertical)
#     c.Divide(horizontal, vertical)

#     return c

def getPad(canvas, number):

    pad = canvas.cd(number)
    pad.SetLeftMargin(gStyle.GetPadLeftMargin())
    pad.SetRightMargin(gStyle.GetPadRightMargin())
    pad.SetTopMargin(gStyle.GetPadTopMargin())
    pad.SetBottomMargin(gStyle.GetPadBottomMargin())

    return pad

def makeCanvas(yRatioWidth, yWidth):

    #canvas = TCanvas("c", "c", 200, 10, 550, yWidth) #500 for hist, 200 for data/mc
    canvas = TCanvas("c", "c", 550, yWidth) 
    yBorder = yRatioWidth / yWidth

    bottomMargin = yWidth/float(yRatioWidth)*gStyle.GetPadBottomMargin()

#    canvas.Divide(1, 2, 0, 0)
    canvas.Divide(1, 2)
    canvas.topPad = getPad(canvas, 1)
    canvas.topPad.SetBottomMargin(0)
    canvas.topPad.SetPad(canvas.topPad.GetX1(), yBorder, canvas.topPad.GetX2(), canvas.topPad.GetY2())
    canvas.bottomPad = getPad(canvas, 2)
    canvas.bottomPad.SetTopMargin(0)
    canvas.bottomPad.SetBottomMargin(bottomMargin)
    canvas.bottomPad.SetPad(canvas.bottomPad.GetX1(), canvas.bottomPad.GetY1(), canvas.bottomPad.GetX2(), yBorder)

    return canvas

def fillSubCanvas(subCanvas, hist, xlabel, ylabel, leg, leg2, title = None, logscale = 1, ymax = 0):

    #subCanvas.SetLogy(logscale)

    if title:

        subCanvas.SetTitle(title)


    if not logscale:

        hist.SetMinimum(0.000001)
    
    hist.SetMaximum(ymax)
    hist.Draw("HIST")

    hist.GetXaxis().SetTitle(xlabel)
    hist.GetYaxis().SetTitle(ylabel)
#    hist.GetYaxis().SetLimits(0.1, ymax)

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

def drawDataMC(summedHist, dataHist, c, xlabel):

    ratioHist = dataHist.Clone()

    ratioHist.Divide(summedHist)

    # for i in range(1, ratioHist.GetNbinsX()):

    #     print(ratioHist.GetBinContent(i))

    ratioHist.Draw("P0 E1 X0")
    
    ratioHist.GetXaxis().SetTitle(xlabel)
    ratioHist.GetYaxis().SetTitle("Data/MC")
    ratioHist.GetYaxis().SetLimits(0.5, 1.5)

    c.Update()

def makeRatio(summedHist, dataHist):

    ratioHist = dataHist.Clone()

    ratioHist.Divide(summedHist)

    return ratioHist

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

def makeSummedHist(histList):

    summedList = TList()

    for hist in histList[0]:

        summedList.Add(hist.Clone())
    
    for source in histList[1:]:

        for j in range(len(source)):

            summedList[j].Add(source[j])

    return summedList

def fillStacked(sources, stackedList):

    for source in sources:

        sourceHists = pickle.load(file(source))

        for j in range(len(stackedList)):

            stackedList[j].Add(sourceHists[j])

        del sourceHists

def findYMax(hist, dataHist):

    max_value  = max(hist.GetMaximum(), dataHist.GetMaximum())

    return 1.1 * max_value

    
def getRatioLine(xmin, xmax):

    line = TPolyLine(2)
    line.SetPoint(0, xmin, 1.)
    line.SetPoint(1, xmax, 1.)
    line.SetLineWidth(1)
    return line

def plot(plotList, histList, dataList, summedList, xLabelList, yLabelList, leg, leg2, title =  "", logscale = 1, year = "2018", folder = 'plots/'):

    yWidth = 700
    yRatioWidth = 200

    for i in range(len(plotList)):
        
        if logscale:
            scale = "log"
        else:
            scale = "linear"

#        c = makeCanvas(1, 1)
        
        c = makeCanvas(yRatioWidth, yWidth)

        c.SetLeftMargin(0.5)
        c.Update()


        filename = "{}/Hist_{}_{}_{}".format(folder, year, plotList[i], scale)

        ymax = findYMax(histList[i], dataList[i])
 
#        c.cd(1)
        c.topPad.cd()      

        gPad.SetLeftMargin(0.125)
        gPad.SetLogy(logscale)
        
        fillSubCanvas(c, histList[i], xLabelList[i], yLabelList[i], leg, leg2, title, logscale, ymax)

        dataList[i].Draw("SAME P0 E1 X0")

        c.Update()


        c.bottomPad.cd()

        gPad.SetLeftMargin(0.125)


        c.SetLogy(0)
        ratioHist = makeRatio(summedList[i], dataList[i])
        ratioHist.SetStats(0)
        # ratioHist.GetYaxis().SetLimits(0.5, 1.5)
        ratioHist.SetMaximum(1.7)
        ratioHist.SetMinimum(0.3)
        ratioHist.Draw("E1 X0")

        ratioHist.GetYaxis().SetTitle("Data / MC")
        ratioHist.GetXaxis().SetTitle(xLabelList[i])
#        ratioHist.GetXaxis().SetTitleSize(.10)
#        ratioHist.GetXaxis().SetTitleOffset(3.2)
#        ratioHist.GetYaxis().SetTitleOffset(histList[i].GetYaxis().GetTitleOffset())
        ratioHist.GetYaxis().SetTitleOffset(0.61)
        # ratioHist.GetXaxis().SetTickLength( 0.03*2 )
        # ratioHist.GetYaxis().SetTickLength( 0.043 )
 
        ratioHist.GetXaxis().SetTitleSize( (yWidth / yRatioWidth - 1) * histList[i].GetXaxis().GetTitleSize() )
        ratioHist.GetYaxis().SetTitleSize( 0.085 )
#        ratioHist.GetYaxis().SetTitleSize( histList[i].GetYaxis().GetTitleSize() )

        
        ratioHist.GetXaxis().SetTickLength( (yWidth / yRatioWidth - 1) * histList[i].GetXaxis().GetTickLength() )
        ratioHist.GetYaxis().SetTickLength( histList[i].GetYaxis().GetTickLength() )

        ratioHist.GetXaxis().SetLabelSize( (yWidth / yRatioWidth - 1) * histList[i].GetXaxis().GetLabelSize() )
        ratioHist.GetYaxis().SetLabelSize( (yWidth / yRatioWidth - 1) * histList[i].GetYaxis().GetLabelSize() )

        ratioHist.GetYaxis().SetNdivisions(505)
        
        if xLabelList[i] == "flavComp":

            ratioHist.GetXaxis().SetBinLabel(1, "ee")
            ratioHist.GetXaxis().SetBinLabel(2, "#mu#mu")

        elif xLabelList[i] == "SR":

            ratioHist.GetXaxis().SetBinLabel(1, "=5 jets,=1 bjets")
            ratioHist.GetXaxis().SetBinLabel(2, "=5 jets,>=2 bjets")
            ratioHist.GetXaxis().SetBinLabel(3, ">=6 jets,=1 bjets")
            ratioHist.GetXaxis().SetBinLabel(4, ">=6 jets,>=2 bjets")


        ratioLine = getRatioLine(histList[i].GetXaxis().GetXmin(), histList[i].GetXaxis().GetXmax())
        ratioLine.Draw()
    
#        drawDataMC(summedList[i], dataList[i], c, xLabelList[i])

        c.Update()

        # set ticks on all sides

        gPad.SetTickx()
        gPad.SetTicky()
        
        c.Update()


        c.cd(1)
        
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
