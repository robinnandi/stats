import sys

#mSquark = int(sys.argv[1])
#mGluino = int(sys.argv[2])
#print "mSquark = "+str(mSquark)+"; mGluino = "+str(mGluino)

from limit import *
from inputData_150 import *

def get_file_number(mSquark, mGluino):
    return 21*( int((mSquark - 400)/80) ) + int((mGluino - 400)/80)

#hist_obs = r.TH2F("obs", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
#hist_exp = r.TH2F("exp", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
#hist_upper = r.TH2F("upper", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
#hist_lower = r.TH2F("lower", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
#outfile = open("results.txt", "w")
#outfile.write("mSquark, mGluino, obs, exp, upper, lower\n")
#outfile.close()
outfile = open("results.txt", "a")
#for mSquark in [400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
#for mSquark in [400, 480, 560, 640, 720, 800, 880]:
#for mSquark in [960, 1040, 1120, 1200]
#for mSquark in [1280, 1360, 1440, 1520]:
#for mSquark in [1600, 1680, 1760, 1840]:
for mSquark in [1920, 2000]:
#for mSquark in [400]:
    for mGluino in [400, 480, 560, 640, 720, 800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760, 1840, 1920, 2000]:
#    for mGluino in [400]:
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
        text = str(mSquark)+", "+str(mGluino)+", "+str(limit_obs)+", "+str(limit_exp)+", "+str(limit_upper)+", "+str(limit_lower)+"\n"
        outfile.write(text)
        #hist_obs.SetBinContent(hist_obs.FindBin(mSquark, mGluino), limit_obs)
        #hist_exp.SetBinContent(hist_exp.FindBin(mSquark, mGluino), limit_exp)
        #hist_upper.SetBinContent(hist_upper.FindBin(mSquark, mGluino), limit_upper)
        #hist_lower.SetBinContent(hist_lower.FindBin(mSquark, mGluino), limit_lower)
        # Draw Histograms
        #f = r.TFile.Open("plots/Exclusion_Plots_"+str(mSquark)+"_"+str(mGluino)+".root", "recreate")
        #hist_obs.Write()
        #hist_exp.Write()
        #hist_upper.Write()
        #hist_lower.Write()
        #f.Close()

