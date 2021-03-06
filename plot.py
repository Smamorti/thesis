from ROOT import TCanvas
import os

def makeCanvas(horizontal, vertical):
    
    c = TCanvas("c", "c", 550 * horizontal, 400 * vertical)
    c.Divide(horizontal, vertical)

    return c

def fillSubCanvas(subCanvas, hist, xlabel, ylabel, leg, leg2, title = None, logscale = 1):

    subCanvas.SetLogy(logscale)

    if title:

        subCanvas.SetTitle(title)

    hist.Draw("HIST")


    # # set the minimum of the y axis, hardcoded for now

    # if logscale:

    #     if xlabel == "m(top1) (GeV)" or xlabel == "m(W2) (GeV)":

    #         #hist.GetYaxis().SetRangeUser(1, 1.2 * hist.GetMaximum())
    #         #hist.GetYaxis().SetRangeUser(0.001, 1.2 * hist.GetMaximum())
    #         hist.SetMinimum(1)


    #     elif xlabel == "|#eta|(l_{1})" or xlabel == "|#eta|(l_{2})" or xlabel == "m(ll) (GeV)":
            
    #         #hist.GetYaxis().SetRangeUser(20, 1.2 * hist.GetMaximum())
    #         #hist.GetYaxis().SetRangeUser(20, 1.2 * hist.GetMaximum())
    #         hist.SetMinimum(20)


    hist.GetXaxis().SetTitle(xlabel)
    hist.GetYaxis().SetTitle(ylabel)

    # hardcoded for now
    if xlabel == "flavComp":

        hist.GetXaxis().SetBinLabel(1, "ee")
        hist.GetXaxis().SetBinLabel(2, "#mu#mu")
        leg2.Draw()

    elif xlabel == "SR":

        hist.GetXaxis().SetBinLabel(1, "=5 jets,=1 bjets")
        hist.GetXaxis().SetBinLabel(2, "=5 jets,>=2 bjets")
        hist.GetXaxis().SetBinLabel(3, ">=6 jets,=1 bjets")
        hist.GetXaxis().SetBinLabel(4, ">=6 jets,>=2 bjets")
        leg.Draw()
    # hardcoded for now
    
    elif xlabel == "leptonMVA l1" or xlabel == "leptonMVA l2" or xlabel == "leptonMVA":

        leg2.Draw()

    else:

        leg.Draw()

    subCanvas.Update()
    

def plot(plotList, histList, dataList, xLabelList, yLabelList, leg, leg2, title =  "", logscale = 1, histList_nonZ = None, titleNotZ = None, logNotZ = 1, year = "2018", MLalgo = "no", workingPoint = "0.5"):

    if MLalgo != "no":

        model = "{}_wp={}".format(MLalgo.replace(".h5", "").replace(".bin","").replace("machineLearning/models/", ""), workingPoint)

    else:

        model = ""

    if not os.path.exists("plots/{}".format(model)):
        os.makedirs("plots/{}".format(model))


    for i in range(len(plotList)):
        
        if titleNotZ:

            c = makeCanvas(2, 1)
            filename = "plots/{}/Hist_comp_{}_{}".format(model, year, plotList[i])
            p1 = c.cd(1)
            fillSubCanvas(p1, histList[-1][i], xLabelList[i], yLabelList[i], leg, leg2, title, logscale)
            p2 = c.cd(2)
            fillSubCanvas(p2, histList_nonZ[-1][i], xLabelList[i], yLabelList[i], leg, leg2, titleNotZ, logNotZ)
            c.SaveAs(filename + ".pdf")
            c.SaveAs(filename + ".png")

        else: 
            
            if logscale:
                scale = "log"
            else:
                scale = "linear"
            c = makeCanvas(1, 1)
            filename = "plots/{}/Hist_{}_{}_{}".format(model, year, plotList[i], scale)
            fillSubCanvas(c, histList[-1][i], xLabelList[i], yLabelList[i], leg, leg2, title, logscale)
            dataList[0][i].Draw("SAME P0 E1 X0 PLC")
            
            c.Update()
            c.SaveAs(filename + ".pdf")
            c.SaveAs(filename + ".png")


            
        c.Close()
