from __future__ import division
from ROOT import TFile, TH1D, TLegend, gROOT, THStack, TList
import numpy as np
import sys
from optparse import OptionParser
import os
from makeHists import addOverflowbin, fillTList, calcWeight, fillStacked, fillColor
from utilities.inputParser import readStack, readConf
from utilities.saveHistList import saveHistList
from utilities.pklPlotTools import makeSummedHist, makeRatio
import pickle


parser = OptionParser()
parser.add_option("-c", "--conf", default = "samples/2018_total_v3.conf", help = "conf file")
parser.add_option("-s", "--stack", default = "samples/2018_total.stack", help = "stack file")
parser.add_option("-t", "--testing", default = "no", help = "Run in test mode (1% of the data) or not?")
parser.add_option("-d", "--dataFile", default = "weights/dataPuHist_2018Inclusive_central.root", help = "Location of data file?")
parser.add_option("-r", "--rootFilesExists", default = "yes", help = "Histograms already created or not?")
parser.add_option("-m", "--MC", default = "weights/MC_nTrueInt.root", help = "")
parser.add_option("-o", "--outputFile", default = "weights/pileup/pileup_nominal.root", help = '')
options, args = parser.parse_args(sys.argv[1:])


def fillHist(channels, xSecDict, locationDict, histList, testing):

    for k in range(len(channels)):

        channel = channels[k]

        f = TFile.Open(locationDict[channel])

        weight = calcWeight(f, xSecDict[channel], 59.74)

        tree = f.Get("blackJackAndHookers/blackJackAndHookersTree")

        count = tree.GetEntries()

        print(count)

        # setup progressbar                                                                                       

        toolbar_width = 100

        sys.stdout.write("File %d/%d. Progress: [%s]" % (k+1, len(channels), " " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))
        progress = 0
        toolbarProgress = 0

        total = count

        if testing == 'yes':

            total *= 0.01

        for _ in tree:

            progress += 1

            if progress / float(count) > 0.01 and testing == 'yes':
                print(progress / float(count))
                break

            if progress / total > toolbarProgress / toolbar_width:
                toolbarProgress += 1
                sys.stdout.write("-")
                sys.stdout.flush()

            histList[0].Fill(tree._nTrueInt, tree._weight * weight)

        print('{} events: {}'.format(channel, histList[0]))


def getMCScale(rootfile, sources):

    mc = TFile.Open(rootfile)
    
    sumHist = mc.Get("nTrueInt_{}".format(sources[0])).Clone()

    for source in sources[1:]:

        sumHist.Add(mc.Get("nTrueInt_{}".format(source)))

    integral = sumHist.Integral()

    return 1 / integral

def normalizeMC(rootfile, sources, histList):

    scale = getMCScale(rootfile, sources)

#    histList = fillTList(sources, ['nTrueInt'], [(100, 0, 100)])
    mc = TFile.Open(rootfile)
    

    for i in range(len(sources)):
        
        hist = mc.Get("nTrueInt_{}".format(sources[i])).Clone()
        hist.Scale(scale)
        print(hist)
 
        temp = TList()
        temp.Add(hist)
        histList.Add(temp)

#       histList[i][0] = hist

    temp = TList()
    stack = THStack("nTrueInt", " ")
    temp.Add(stack)
    histList.Add(temp)

    fillColor(histList, colorDict, typeList)
    fillStacked(histList)
    
    saveHistList(sources, histList, 'weights/pkl/MC.pkl')

def makeWeight(outputfile, source, hist, data):

    outputfile = outputfile.replace('.root', '_{}.root'.format(source))

    # normalize hist

    integral = hist.Integral()

    hist.Scale(1/integral)

    print(hist.Integral())
    print(data.Integral())

    

    weightHist, _, _, _ = makeRatio(hist, data, "Data/MC")

    output = TFile.Open(outputfile, 'RECREATE')
    output.cd()
    
    weightHist.Write()
    output.Close()

    temp = TList()
    t2 = TList()
    t2.Add(hist)
    temp.Add(t2)
    saveHistList([source], temp, 'weights/pkl/ratio.pkl')

## MAIN

typeList, sourceDict, texDict, colorDict = readStack(options.stack)

if options.rootFilesExists != "yes":

    locationDict, xSecDict = readConf(options.conf)

    histList = fillTList(typeList, ['nTrueInt'], [(100, 0, 100)])


    for i in range(len(typeList)):

        source = typeList[i]

        print('Currently working on {}.'.format(source))

        channels = sourceDict[source]
        print(channels)

        fillHist(channels, xSecDict, locationDict, histList[i], testing = options.testing)

    fillColor(histList, colorDict, typeList)
    fillStacked(histList)

    d = TFile.Open(options.dataFile)

    dataHist = d.Get('pileup')
    dataHist.SetName('data')

    dataList = fillTList(['data'], ['nTrueInt'], [(100, 0, 100)])


    dataList[0][0] = dataHist

    dataList[0][0].SetMarkerStyle(20)
    dataList[0][0].SetMarkerColor(1)
    dataList[0][0].SetLineColor(1)
    dataList[0][0].SetMarkerSize(0.5)

    saveHistList(["data"], dataList, 'data.pkl')
    saveHistList(typeList, histList, 'MC.pkl')

else:

    # we already made the rootfiles

    data = TFile.Open(options.dataFile)
    dataHist = data.Get('pileup')

    totData = dataHist.Integral()

    dataHist.Scale(1/totData)

    print(dataHist.Integral())

    dataHist.SetMarkerStyle(20)
    dataHist.SetMarkerColor(1)
    dataHist.SetLineColor(1)
    dataHist.SetMarkerSize(0.5)

    dataList = fillTList(['data'], ['nTrueInt'], [(100, 0, 100)])
    dataList[0][0] = dataHist
    saveHistList(["data"], dataList, 'weights/pkl/data.pkl')

    histList = TList()
    normalizeMC(options.MC, typeList, histList)

    # make weights histogram

    MClist = pickle.load(file('weights/pkl/MC.pkl'))

    for i in range(len(typeList)):

        hist = MClist[i][0].Clone()
        makeWeight(options.outputFile, typeList[i], hist, dataHist)
        
    

    # for x in MClist:

    #     print(x[0])

    # summedMC = makeSummedHist(MClist[:-1])

    # weightHisto, _, _, _  = makeRatio(summedMC, dataHist, "Data/MC")

    # weightFile = TFile.Open(options.outputFile, "RECREATE")
    # weightFile.cd()
    
    # weightHisto.Write()
    
