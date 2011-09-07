import ROOT as r
import copy

def expectedLimitPlots(quantiles = {}, hist = None, obsLimit = None, note = "") :
    filename = "limits_%s.eps"%note
    canvas = r.TCanvas("canvas")
    canvas.SetTickx()
    canvas.SetTicky()

    l = drawDecoratedHisto(quantiles, hist, obsLimit)

    canvas.Print(filename)

def drawDecoratedHisto(quantiles = {}, hist = None, obs = None) :
    hist.Draw()
    hist.SetStats(False)

    q = copy.deepcopy(quantiles)
    q["Observed"] = obs

    legend = r.TLegend(0.1, 0.7, 0.5, 0.9)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    
    line = r.TLine()
    line.SetLineWidth(2)
    for i,key in enumerate(sorted(q.keys())) :
        line.SetLineColor(2+i)
        line2 = line.DrawLine(q[key], hist.GetMinimum(), q[key], hist.GetMaximum())
        legend.AddEntry(line2, key, "l")
    legend.Draw()
    return legend
