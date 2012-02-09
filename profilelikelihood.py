import ROOT as r
from systematics import Systematics

def wimport(w, item) :
    r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.WARNING) #suppress info messages
    getattr(w, "import")(item)
    r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.DEBUG) #re-enable all messages

def setupLikelihood(w) :
    terms = []
    obs = []
    nuis = []

    wimport(w, r.RooRealVar("b", "b", 3.0))
    #wimport(w, r.RooGaussian("bkgd", "bkgd", 3.0))
    wimport(w, r.RooRealVar("n", "n", 4.0))
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


f = foo()
#out = f.interval()
out = f.interval(0.95, "feldmanCousins", True)
print out
