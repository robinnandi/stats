# One bin; poisson likelihood; CLs, Profile Likelihood and Feldman Cousins.

import ROOT as r
from runInverter import RunInverter

def wimport(w, item) :
    r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.WARNING) #suppress info messages
    getattr(w, "import")(item)
    r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.DEBUG) #re-enable all messages

def setupLikelihood(w) :
    terms = []
    obs = []
    nuis = []

    wimport(w, r.RooRealVar("b", "b", 3.0))
    wimport(w, r.RooRealVar("n", "n", 4))
    wimport(w, r.RooRealVar("s", "s", 1.0, 0.0, 30.0))
    wimport(w, r.RooAddition("exp", "exp", r.RooArgSet(w.var("b"), w.var("s"))))
    wimport(w, r.RooPoisson("Pois", "Pois", w.var("n"), w.function("exp")))

    terms.append("Pois")
    obs.append("n")
    w.factory("PROD::model(%s)"%",".join(terms))

    w.defineSet("poi", "s")
    w.defineSet("obs", ",".join(obs))
    w.defineSet("nuis", ",".join(nuis))

def dataset(obsSet) :
    out = r.RooDataSet("dataName","dataTitle", obsSet)
    out.add(obsSet)
    return out

def modelConfiguration(w) :
    modelConfig = r.RooStats.ModelConfig("modelConfig")
    modelConfig.SetWorkspace(w)
    modelConfig.SetPdf(w.pdf("model"))
    modelConfig.SetObservables(w.set("obs"))
    modelConfig.SetParameters(w.set("poi"))
    modelConfig.SetNuisanceParameters(w.set("nuis"))
    return modelConfig

def clsPoisson(n = None, b = None, s = None) :
    num = 0.0
    den = 0.0
    #print n
    for i in range(1+n) :
        num+=r.TMath.PoissonI(i, b+s)
        den+=r.TMath.PoissonI(i, b)
    return num/den

def oneGraph(n = None, b = None, npoints = None, poimin = None, poimax = None) :
    gr = r.TGraph()
    gr.SetMarkerStyle(26)
    gr.SetLineColor(r.kCyan)
    gr.SetLineWidth(2)
    gr.SetMarkerColor(r.kMagenta)
    for i in range(npoints) :
        s = poimin
        if i : s += i*(poimax-poimin)/(npoints-1)
        gr.SetPoint(i, s, clsPoisson(n, b, s))

    return gr

def plInterval(dataset, modelconfig, wspace, cl = 0.95, makePlots = True) :
    out = {}
    calc = r.RooStats.ProfileLikelihoodCalculator(dataset, modelconfig, 1.-cl)
    lInt = calc.GetInterval()
    out["upperLimit"] = lInt.UpperLimit(wspace.var("s"))
    out["lowerLimit"] = lInt.LowerLimit(wspace.var("s"))

    if makePlots :
        canvas = r.TCanvas()
        canvas.SetTickx()
        canvas.SetTicky()
        filename = "intervalPlot_%g"%(100*cl)
        plot = r.RooStats.LikelihoodIntervalPlot(lInt)
        plot.SetMaximum(3.)
        plot.Draw()
        canvas.SaveAs(filename+".eps")
        #canvas.SaveAs(filename+".png")

    return out

def fcExcl(dataset, modelconfig, wspace, cl = 0.95, makePlots = True) :

    nPoints = 200
    out = {}
    calc = r.RooStats.FeldmanCousins(dataset, modelconfig)
    calc.FluctuateNumDataEntries(False)
    calc.UseAdaptiveSampling(True)
    calc.SetNBins(nPoints)

    calc.SetConfidenceLevel(cl)
    lInt = calc.GetInterval()

    out["upperLimit"] = lInt.UpperLimit(wspace.var("s"))

    return out

def cls(dataset, modelconfig, wspace) :

    testStatType = 3

    npoints = 11
    poimin = 0.0
    poimax = 30.0

    n = int(wspace.var("n").getVal())
    b = wspace.var("b").getVal()

    desc = "n_%d_b_%g_TS%d"%(n, b, testStatType)
    
    wimport(wspace, dataset)
    wimport(wspace, modelconfig)
    result = RunInverter(w = wspace, modelSBName = "modelConfig", dataName = "dataName",
                         nworkers = 6, type = 0, testStatType = testStatType, ntoys = 2000,
                         npoints = npoints, poimin = poimin, poimax = poimax)

    print "upper limit = %g +- %g"%(result.UpperLimit(), result.UpperLimitEstimatedError())
    plot = r.RooStats.HypoTestInverterPlot("HTI_Result_Plot", "", result)
    plot.Draw("CLb 2CL")

    gr = oneGraph(n = n, b = b, npoints = 3*npoints, poimin = poimin, poimax = poimax)
    gr.Draw("lpsame")

    for s in [3.0, 30.0] :
        tsPlot = plot.MakeTestStatPlot(result.FindIndex(s))
        #tsPlot.SetLogYaxis(True)
        t = "tsPlot_s_%g_%s"%(s, desc)
        tsPlot.Draw()
        tsPlot.SetTitle(t)
        r.gPad.Print("%s.eps"%t)
    
    plot.SetTitle(desc)
    r.gPad.Print("simple_%s.eps"%desc)
    return result

class foo(object) :
    def __init__(self) :
        r.gROOT.SetBatch(True)
        r.RooRandom.randomGenerator().SetSeed(1)
        self.wspace = r.RooWorkspace("workspace")
        setupLikelihood(self.wspace)
        #self.data = self.wspace.pdf("model").generate(self.wspace.set("obs"), 10000)
        self.data = dataset(self.wspace.set("obs"))
        self.modelConfig = modelConfiguration(self.wspace)

    def interval(self, cl = 0.95, method = "profileLikelihood", makePlots = True) :
        if method=="profileLikelihood" :
            return plInterval(self.data, self.modelConfig, self.wspace, cl = cl, makePlots = makePlots)
        elif method=="feldmanCousins" :
            return fcExcl(self.data, self.modelConfig, self.wspace, cl = cl, makePlots = makePlots)

    def cls(self) :
        return cls(self.data, self.modelConfig, self.wspace)


f = foo()
#out = f.cls()
#out = f.interval()
out = f.interval(0.95, "feldmanCousins", True)
print out
