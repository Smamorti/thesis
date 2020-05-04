from ROOT import TCanvas, TFile

f = TFile.Open("../weights/bTagEff_looseLeptonCleaned_2018.root")
hist = f.Get("bTagEff_loose_beauty")
c = TCanvas("c2e","c2e",600,400)
hist.Draw("E")

c.SaveAs("test2D.pdf")
