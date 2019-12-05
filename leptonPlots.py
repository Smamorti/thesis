from ROOT import TFile, TH1F, TCanvas, TList, TColor, TLegend, THStack
from ROOT import Math
import ROOT
import numpy as np

import makeHists, plot

# stack = "task1_2018.stack" 
# conf = "tuples_2018.conf"

# stack = "task1_2017.stack" 
# conf = "tuples_2017.conf"

stack = "samples/newSkim_2018.stack"
conf = "samples/tuples_2018_newSkim.conf"

year = stack.split("_")[1].rstrip(".stack")
print("Using files from " + year)


channels_stack, texList, _, colorList = np.loadtxt(stack, comments = "%", unpack = True, dtype = str)
channels_conf, files, xSecs = np.loadtxt(conf, comments = "%", unpack = True, dtype = str) #different channel list to enable different ordering of events in .stack and .conf files, one can later match the two together


colorList = colorList.astype(int)
xSecs = xSecs.astype(float)


plotList = ["leading_lPt", "subleading_lPt", "leading_lEta", "subleading_lEta","nJets", "m_ll", "flavComp", "nbJets", "MET", "leading_DeltaR", "leading_DeltaR_b", "subleading_DeltaR", "subleading_DeltaR_b", "leading_leptonMVA", "subleading_leptonMVA"]#, "lEta", "m_ll", "nJets", "flavComp"] #also: nbjets, pt_Z
binList = [(20, 0, 200), (20, 0, 200), (10, 0, 2.5), (10, 0, 2.5), (12, 0, 12), (10, 81, 101), (2, 0, 2), (5, 0, 5), (20, 0, 500), (20, 0, 5), (20, 0, 5), (20, 0, 5), (20, 0, 5), (20, -1, 1), (20, -1, 1)]#, (10, 0, 2.5), (20, 0, 500), (20, 0, 19), (3, 0, 2)] #also: nbjets, pt_Z

histList = makeHists.fillTList(channels_stack, plotList, binList)  

histZMassList = makeHists.fillTList(channels_stack, ["Z mass"], [(50, 0, 180)], extra = "ZMass")
#histList_Z = makeHists.fillTList(channels_stack, plotList, binList, "_Z")
#histList_notZ = makeHists.fillTList(channels_stack, plotList, binList, "_NotZ")


#
# Fill histograms
#

for i in range(len(files)):

    f = TFile.Open(files[i])
    print("Working on file number {}".format(i))
    print(files[i])
    print(channels_stack[i])
    makeHists.fillHist(f, xSecs[i], histList[i], plotList, histZMassList[i], year = year)
    
    f.Close()


makeHists.fillColor(histList, colorList)
makeHists.fillStacked(histList)

makeHists.fillColor(histZMassList, colorList)
makeHists.fillStacked(histZMassList)
#
#Plotting
#

ROOT.gROOT.SetBatch(True)

# Plot Z Mass

# c1 = TCanvas("c1", "Z Mass", 425, 425)
# c1.SetLogy()
# h_ZMass_Stacked = histZMassList[-1][0]

# h_ZMass_Stacked.Draw("HIST")
# h_ZMass_Stacked.GetXaxis().SetTitle("Z Mass (GeV)")
# h_ZMass_Stacked.GetYaxis().SetTitle("Events")

# leg2 = makeHists.makeLegend(channels_stack, histZMassList)

# leg2.Draw()
# c1.Update()

# c1.SaveAs("HistZMass_{}.pdf".format(year))


#leg = makeHists.makeLegend(channels_stack, histList)
leg = makeHists.makeLegend(texList, histList)

plot.plot(plotList, histList, leg, year = year)
plot.plot(plotList, histList, leg,title =  "No Logscale", logscale = 0, histList_nonZ = histList, titleNotZ = "Logscale", logNotZ = 1, year = year)
