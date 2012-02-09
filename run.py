import sys

#mSquark = int(sys.argv[1])
#mGluino = int(sys.argv[2])
#print "mSquark = "+str(mSquark)+"; mGluino = "+str(mGluino)

from limit import *
from inputData_150 import *

def get_file_number(mSquark, mGluino):
    return 21*( int((mSquark - 400)/80) ) + int((mGluino - 400)/80)

hist_obs = r.TH2F("exclusion", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
hist_exp = r.TH2F("exclusion", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
hist_upper = r.TH2F("exclusion", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
hist_lower = r.TH2F("exclusion", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
#for mSquark in [400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
for mSquark in [960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
    for mGluino in [400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
        n = get_file_number(mSquark, mGluino)
        f = foo(inputData[n])
        obs = f.observedLimit(0.95, "profileLikelihood", True, str(mSquark)+"_"+str(mGluino))
        limit_obs = obs["upperLimit"]
        exp = f.expectedLimit(0.95, "profileLikelihood", True, str(mSquark)+"_"+str(mGluino))
        print obs
        print exp
        limit_exp = exp[0]["Median"]
        limit_upper = exp[0]["MedianPlusOneSigma"]
        limit_lower = exp[0]["MedianMinusOneSigma"]
        hist_obs.SetBinContent(hist_obs.GetBin(mSquark, mGluino), limit_obs)
        hist_exp.SetBinContent(hist_exp.GetBin(mSquark, mGluino), limit_exp)
        hist_upper.SetBinContent(hist_upper.GetBin(mSquark, mGluino), limit_upper)
        hist_lower.SetBinContent(hist_lower.GetBin(mSquark, mGluino), limit_lower)

#f = r.TFile.Open("plots/Exclusion_Plot_"+str(mSquark)+"_"+str(mGluino)+".root", "recreate")
#hist.Write()
c = r.TCanvas("c", "c", 1000, 1000)
hist_obs.Draw("TEXT")
#c.SaveAs("Exclusion_Plot_obs.png")
c.SaveAs("Exclusion_Plot_obs.eps")
c.SaveAs("Exclusion_Plot_obs.pdf")
hist_exp.Draw("TEXT")
#c.SaveAs("Exclusion_Plot_exp.png")
c.SaveAs("Exclusion_Plot_exp.eps")
c.SaveAs("Exclusion_Plot_exp.pdf")
hist_upper.Draw("TEXT")
#c.SaveAs("Exclusion_Plot_upper.png")
c.SaveAs("Exclusion_Plot_upper.eps")
c.SaveAs("Exclusion_Plot_upper.pdf")
hist_lower.Draw("TEXT")
#c.SaveAs("Exclusion_Plot_lower.png")
c.SaveAs("Exclusion_Plot_lower.eps")
c.SaveAs("Exclusion_Plot_lower.pdf")
