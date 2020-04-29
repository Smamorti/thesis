from ROOT import TFile, TH1F

hist = TH1F("pileup", " ", 100, 0, 100)

for bin in range(hist.GetNbinsX() + 2):

    hist.SetBinContent(bin, 1)

for bin in range(hist.GetNbinsX() + 2):

    print(hist.GetBinContent(bin))

f = TFile.Open('noPileup.root', 'RECREATE')

f.cd()
hist.Write()
