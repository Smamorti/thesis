from ROOT import TCanvas

def makeCanvas(horizontal, vertical):
    
    c = TCanvas("c", "c", 500 * horizontal, 400 * vertical)
    c.Divide(horizontal, vertical)

    return c

def fillSubCanvas(subCanvas, hist, xlabel, leg, title = None, logscale = 1):

    subCanvas.SetLogy(logscale)
    if title:

        subCanvas.SetTitle(title)

    hist.Draw("HIST")
    hist.GetXaxis().SetTitle(xlabel)
    hist.GetYaxis().SetTitle("Events")
    leg.Draw()
    subCanvas.Update()
    

def plot(plotList, histList, leg,title =  "", logscale = 1, histList_nonZ = None, titleNotZ = None, logNotZ = 1, year = "2018"):

    for i in range(len(plotList)):
        
        if titleNotZ:

            c = makeCanvas(2, 1)
            filename = "plots/Hist_comp_{}_{}".format(year, plotList[i])
            p1 = c.cd(1)
            fillSubCanvas(p1, histList[-1][i], plotList[i], leg, title, logscale)
            p2 = c.cd(2)
            fillSubCanvas(p2, histList_nonZ[-1][i], plotList[i], leg, titleNotZ, logNotZ)
            c.SaveAs(filename + ".pdf")
            c.SaveAs(filename + ".png")

        else: 
            
            if logscale:
                scale = "log"
            else:
                scale = "linear"

            c = makeCanvas(1, 1)
            filename = "plots/Hist_{}_{}_{}".format(year, plotList[i], scale)
            fillSubCanvas(c, histList[-1][i], plotList[i], leg, title, logscale)
            c.SaveAs(filename + ".pdf")
            c.SaveAs(filename + ".png")


            
        c.Close()
