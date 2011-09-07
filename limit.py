import ROOT as r
import array
import plotting as plotting
from runInverter import RunInverter
from inputData import inputData

def wimport(w, item) :
    r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.WARNING) #suppress info messages
    getattr(w, "import")(item)
    r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.DEBUG) #re-enable all messages

def setupLikelihood(w, inputData, smOnly) :
    terms = []
    obs = []
    nuis = []
    poi = []
    wimport(w, r.RooRealVar("f", "f", 0.1, 0.0, 1.0))
    wimport(w, r.RooRealVar("xsec", "xsec", inputData.CrossSection + 0.1*inputData.CrossSectionError, inputData.CrossSection - 3*inputData.CrossSectionError, inputData.CrossSection + 3*inputData.CrossSectionError))
    wimport(w, r.RooRealVar("xsec_mu", "xsec_mu", inputData.CrossSection))
    wimport(w, r.RooRealVar("xsec_sig", "xsec_sig", inputData.CrossSectionError))
    wimport(w, r.RooGaussian("gaus_xsec", "gaus_xsec", w.function("xsec"), w.var("xsec_mu"), w.var("xsec_sig")))
    wimport(w, r.RooRealVar("lumi", "lumi", inputData.Lumi + 0.1*inputData.LumiError, inputData.Lumi - 3*inputData.LumiError, inputData.Lumi + 3*inputData.LumiError))
    wimport(w, r.RooRealVar("lumi_mu", "lumi_mu", inputData.Lumi))
    wimport(w, r.RooRealVar("lumi_sig", "lumi_sig", inputData.LumiError))
    wimport(w, r.RooGaussian("gaus_lumi", "gaus_lumi", w.function("lumi"), w.var("lumi_mu"), w.var("lumi_sig")))
    for i in range(inputData.nBins) :
        wimport(w, r.RooRealVar("n_%d"%i, "n_%d"%i, inputData.Observation[i]))
        wimport(w, r.RooRealVar("b_%d"%i, "b_%d"%i, inputData.Background[i] + 0.1*inputData.BackgroundError[i], inputData.Background[i] - 3*inputData.BackgroundError[i], inputData.Background[i] + 3*inputData.BackgroundError[i]))
        wimport(w, r.RooRealVar("b_mu_%d"%i, "b_mu_%d"%i, inputData.Background[i]))
        wimport(w, r.RooRealVar("b_sig_%d"%i, "b_sig_%d"%i, inputData.BackgroundError[i]))
        wimport(w, r.RooGaussian("gaus_b_%d"%i, "gaus_b_%d"%i, w.function("b_%d"%i), w.var("b_mu_%d"%i), w.var("b_sig_%d"%i)))
        wimport(w, r.RooRealVar("eff_%d"%i, "eff_%d"%i, inputData.SignalEfficiency[i]))
        wimport(w, r.RooProduct("s_%d"%i, "s_%d"%i, r.RooArgSet(w.var("eff_%d"%i), w.var("lumi"), w.var("xsec"), w.var("f"))))
        if smOnly :
            wimport(w, r.RooPoisson("pois_%d"%i, "pois_%d"%i, w.var("n_%d"%i), w.var("b_%d"%i)))
        else :
            wimport(w, r.RooAddition("exp_%d"%i, "exp_%d"%i, r.RooArgSet(w.function("b_%d"%i), w.function("s_%d"%i))))
            wimport(w, r.RooPoisson("pois_%d"%i, "pois_%d"%i, w.var("n_%d"%i), w.function("exp_%d"%i)))

        terms.append("pois_%d"%i)
        terms.append("gaus_b_%d"%i)
        obs.append("n_%d"%i)
        nuis.append("b_%d"%i)
    terms.append("gaus_xsec")
    terms.append("gaus_lumi")
    nuis.append("xsec")
    nuis.append("lumi")

    poi.append("f")

    w.factory("PROD::model(%s)"%",".join(terms))

    w.defineSet("poi", ",".join(poi))
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
    out["upperLimit"] = lInt.UpperLimit(wspace.var("f"))
    out["lowerLimit"] = lInt.LowerLimit(wspace.var("f"))

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

    out["upperLimit"] = lInt.UpperLimit(wspace.var("f"))

    return out

def cls(dataset = None, modelconfig = None, wspace = None, smOnly = None, cl = None, nToys = None, calculatorType = None, testStatType = None,
        plusMinus = {}, note = "", makePlots = None, nWorkers = None, nPoints = 1, poiMin = 1.0, poiMax = 1.0) :
    assert not smOnly

    wimport(wspace, dataset)
    wimport(wspace, modelconfig)
    wspace.Print()
    result = RunInverter(w = wspace, modelSBName = "modelConfig", dataName = "dataName",
                         nworkers = nWorkers, ntoys = nToys, type = calculatorType, testStatType = testStatType,
                         npoints = nPoints, poimin = poiMin, poimax = poiMax, debug = False)

    out = {}
    for iPoint in range(nPoints) :
        s = "" if not iPoint else "_%d"%iPoint
        out["CLb%s"     %s] = result.CLb(iPoint)
        out["CLs+b%s"   %s] = result.CLsplusb(iPoint)
        out["CLs%s"     %s] = result.CLs(iPoint)
        out["CLsError%s"%s] = result.CLsError(iPoint)
        out["PoiValue%s"%s] = result.GetXValue(iPoint)

    if nPoints==1 and poiMin==poiMax :
        args = {}
        for item in ["testStatType", "plusMinus", "note", "makePlots"] :
            args[item] = eval(item)
        args["result"] = result
        args["poiPoint"] = poiMin
        args["out"] = out
        clsOnePoint(args)
    else :
        out["UpperLimit"] = result.UpperLimit()
        out["UpperLimitError"] = result.UpperLimitEstimatedError()
        out["LowerLimit"] = result.LowerLimit()
        out["LowerLimitError"] = result.LowerLimitEstimatedError()
        
    return out

def pseudoData(wspace, nToys) :
    out = []
    #make pseudo experiments with current parameter values
    dataset = wspace.pdf("model").generate(wspace.set("obs"), nToys)
    for i in range(int(dataset.sumEntries())) :
        argSet = dataset.get(i)
        data = r.RooDataSet("pseudoData%d"%i, "title", argSet)
        data.add(argSet)
        out.append(data)
    return out

def limits(wspace, snapName, modelConfig, smOnly, cl, method, datasets, makePlots = False) :
    out = []
    for i,dataset in enumerate(datasets) :
        wspace.loadSnapshot(snapName)
        if method == "profileLikelihood" :
            interval = plInterval(dataset, modelConfig, wspace, cl = cl, makePlots = makePlots)
        elif method == "feldmanCousins" :
            interval = fcExcl(dataset, modelConfig, wspace, cl = cl, makePlots = makePlots)
        elif method == "cls" :
            interval = cls(dataset, modelConfig, wspace, smOnly = False, cl = 0.95, nToys = 1000, testStatType = 1, plusMinus = {}, makePlots = False, nWorkers = 1, nPoints = 31, poiMin = 0., poiMax = 30.)
        else :
            print "Method not recognised. Must be \"profileLikelihood\", \"feldmanCousins\" or \"cls\"."
        out.append(interval["upperLimit"])
    return sorted(out)

def quantiles(values = [], plusMinus = {}, histoName = "", histoTitle = "", histoBins = [], cutZero = None) :
    def histoFromList(l, name, title, bins, cutZero = False) :
        h = r.TH1D(name, title, *bins)
        for item in l :
            if cutZero and (not item) : continue
            h.Fill(item)
        return h
    
    def probList(plusMinus) :
        def lo(nSigma) : return ( 1.0-r.TMath.Erf(nSigma/math.sqrt(2.0)) )/2.0
        def hi(nSigma) : return 1.0-lo(nSigma)
        out = []
        out.append( (0.5, "Median") )
        for key,n in plusMinus.iteritems() :
            out.append( (lo(n), "MedianMinus%s"%key) )
            out.append( (hi(n), "MedianPlus%s"%key)  )
        return sorted(out)

    def oneElement(i, l) :
        return map(lambda x:x[i], l)
    
    pl = probList(plusMinus)
    probs = oneElement(0, pl)
    names = oneElement(1, pl)
    
    probSum = array.array('d', probs)
    q = array.array('d', [0.0]*len(probSum))

    h = histoFromList(values, name = histoName, title = histoTitle, bins = histoBins, cutZero = cutZero)
    h.GetQuantiles(len(probSum), q, probSum)
    return dict(zip(names, q)),h

def expectedLimit(dataset, modelConfig, wspace, smOnly, cl, method, nToys, plusMinus, note = "", makePlots = False) :
    assert not smOnly
    
    def rooFitResults(pdf, data, options = (r.RooFit.Verbose(False), r.RooFit.PrintLevel(-1), r.RooFit.Save(True))) :
        return pdf.fitTo(data, *options)

    #fit to SM-only
    wspace.var("f").setVal(0.0)
    wspace.var("f").setConstant(True)
    results = rooFitResults(wspace.pdf("model"), dataset)

    #generate toys
    toys = pseudoData(wspace, nToys)

    #restore signal model
    wspace.var("f").setVal(1.0)
    wspace.var("f").setConstant(False)

    #save snapshot
    snapName = "snap"
    wspace.saveSnapshot(snapName, wspace.allVars())

    #fit toys
    l = limits(wspace, snapName, modelConfig, smOnly, cl, method, toys)

    q,hist = quantiles(l, plusMinus, histoName = "upperLimit", histoTitle = ";Upper limit on f;toys / bin", histoBins = (50, 1, -1), cutZero = True)
    nSuccesses = hist.GetEntries()

    obsLimit = limits(wspace, snapName, modelConfig, smOnly, cl, method, [dataset])[0]

    if makePlots : plotting.expectedLimitPlots(quantiles = q, hist = hist, obsLimit = obsLimit, note = note)
    return q,nSuccesses

class foo(object) :
    def __init__(self) :
        r.gROOT.SetBatch(True)
        r.RooRandom.randomGenerator().SetSeed(1)
        self.wspace = r.RooWorkspace("workspace")
        setupLikelihood(self.wspace, inputData, smOnly = False)
        self.data = dataset(self.wspace.set("obs"))
        self.modelConfig = modelConfiguration(self.wspace)

    def observedLimit(self, cl = 0.95, method = "profileLikelihood", makePlots = True) :
        if method == "profileLikelihood" :
            return plInterval(self.data, self.modelConfig, self.wspace, cl = cl, makePlots = makePlots)
        elif method == "feldmanCousins" : 
            return fcExcl(self.data, self.modelConfig, self.wspace, cl = cl, makePlots = makePlots)
        elif method == "cls" :
            return cls(self.data, self.modelConfig, self.wspace, smOnly = False, cl = 0.95, nToys = 100, testStatType = 1, plusMinus = {}, makePlots = False, nWorkers = 1, nPoints = 31, poiMin = 0., poiMax = 30.)
        else :
            print "Method not recognised. Must be \"profileLikelihood\", \"feldmanCousins\" or \"cls\"."

    def expectedLimit(self, cl = 0.95, method = "profileLikelihood", makePlots = True) :
        return expectedLimit(self.data, self.modelConfig, self.wspace, smOnly = False, cl = cl, method = method, nToys = 1000, plusMinus = {}, makePlots = makePlots)


f = foo()
out = f.observedLimit(0.95, "profileLikelihood", True)
#out = f.observedLimit(0.95, "feldmanCousins", True)
#out = f.observedLimit(0.95, "cls", True)
#print "Upper Limit = "+str(out["UpperLimit"])
#print "Lower Limit = "+str(out["LowerLimit"])
#out = f.expectedLimit(0.95, "profileLikelihood", True)
print out
