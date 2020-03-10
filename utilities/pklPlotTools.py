from ROOT import TCanvas, TLegend, THStack

def makeLegend(typeList, histList, texDict, position = (0.8, 0.7, 0.9, 0.9)):

    leg = TLegend(position[0], position[1], position[2], position[3])

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

    # hardcoded for now                                                                                                                                                                                     
    elif xlabel == "leptonMVA l1" or xlabel == "leptonMVA l2" or xlabel == "leptonMVA":

        leg2.Draw()

    else:

        leg.Draw()

    subCanvas.Update()

def differentOrder(histList, i, hist, order = [2, 0, 1]):

    for j in order:

        hist.Add(histList[j][i])
    

def plot(plotList, histList, xLabelList, yLabelList, leg, leg2, title =  "", logscale = 1, year = "2018"):

    for i in range(len(plotList)):
        
        if logscale:
            scale = "log"
        else:
            scale = "linear"

        c = makeCanvas(1, 1)
        filename = "plots/Hist_{}_{}_{}".format(year, plotList[i], scale)
        fillSubCanvas(c, histList[-1][i], xLabelList[i], yLabelList[i], leg, leg2, title, logscale)
        c.SaveAs(filename + ".pdf")
        c.SaveAs(filename + ".png")
        c.Close()

        # hardcoded (for now?)

        if xLabelList[i] == "m(ll) (GeV)":

            hist = THStack(xLabelList[i]," ")
            differentOrder(histList, i, hist, order = [2, 0, 1])

            c = makeCanvas(1, 1)
            filename = "plots/Hist_{}_{}_{}_{}".format(year, plotList[i], scale, "ttunder")
            fillSubCanvas(c, hist, xLabelList[i], yLabelList[i], leg, leg2, title, logscale)
            c.SaveAs(filename + ".pdf")
            c.SaveAs(filename + ".png")
            c.Close()
