from ROOT import TCanvas, TFile, TLegend, gROOT, TList
import ROOT.gStyle as gStyle
from inputParser import readStack
from pklPlotTools import makeLegend


typeList, sourceDict, texDict, colorDict = readStack("samples/2018_total.stack")
typeList.append("total")

gROOT.SetBatch(True)

leg = TLegend(0.8, 0.685, 0.89, 0.875, '', 'NBNDC')
leg.SetBorderSize(0)


histList = TList()

ttZ = TFile.Open('weights/pileup/pileup_up_{}.root'.format('ttZ'))
hist_ttZ = ttZ.Get("pileup").Clone('ttZ')
hist_ttZ.SetLineColor(colorDict['ttZ'])
histList.Add(hist_ttZ)
ttX = TFile.Open('weights/pileup/pileup_up_{}.root'.format('ttX'))
hist_ttX = ttX.Get("pileup").Clone('ttX')
hist_ttX.SetLineColor(colorDict['ttX'])
histList.Add(hist_ttX)
ttW = TFile.Open('weights/pileup/pileup_up_{}.root'.format('ttW'))
hist_ttW = ttW.Get("pileup").Clone('ttW')
hist_ttW.SetLineColor(colorDict['ttW'])
histList.Add(hist_ttW)
other = TFile.Open('weights/pileup/pileup_up_{}.root'.format('other'))
hist_other = other.Get("pileup").Clone('other')
hist_other.SetLineColor(colorDict['other'])
histList.Add(hist_other)
tt = TFile.Open('weights/pileup/pileup_up_{}.root'.format('tt'))
hist_tt = tt.Get("pileup").Clone('tt')
hist_tt.SetLineColor(colorDict['tt'])
histList.Add(hist_tt)
DY = TFile.Open('weights/pileup/pileup_up_{}.root'.format('DY'))
hist_DY = DY.Get("pileup").Clone('DY')
hist_DY.SetLineColor(colorDict['DY'])
histList.Add(hist_DY)
total = TFile.Open('weights/pileup/pileup_up_{}.root'.format('total'))
hist_total = total.Get("pileup").Clone('total')
hist_total.SetLineColor(1)
histList.Add(hist_total)



for h in histList:

    h.SetStats(0)

for h in histList:

    print(h)

for i in range(len(typeList[:-1])):

    leg.AddEntry(histList[i], typeList[i], "l")

leg.AddEntry(histList[-1], typeList[-1], "ep")

canvas = TCanvas("c", "c", 550, 500)


for h in histList[:-1]:

    print(h.GetBinContent(13))
    h.SetMinimum(0)
    h.Draw("HIST SAME")
    canvas.Update()

histList[-1].SetMinimum(0)
histList[-1].Draw("SAME P0 E1 X0")
canvas.Update()

leg.Draw()
canvas.Update()

canvas.SaveAs("test_up.pdf")
canvas.Close()
