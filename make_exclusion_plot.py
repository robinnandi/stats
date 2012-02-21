import ROOT as r
import math
import array
from interpolate import interpolate_array

def Min(list):
    min_ele = 1e10
    min_ix = 0
    ix = 0
    for ele in list:
        if (ele < min_ele):
            min_ele = ele
            min_ix = ix
        ix = ix + 1
    return min_ix, min_ele

def GetBin(mSquark, mGluino):
    return int(23*((mGluino - 400)/80+1) + (mSquark - 400)/80+1)

def GetContour(a):
    min_ix = []
    min_ele_row = []
    min_ix_row = []
    i = 0
    for row in a:
        ix, ele = Min([math.fabs(x - 1) for x in row])
        min_ele_row.append(ele)
        min_ix_row.append((i, ix))
        if (i > 106 and i < 189 and ix < 58): # mSquark = 1200
            min_ix.append((i, ix))
        i = i + 1
    min_ix.reverse()
    min_ele_column = []
    min_ix_column = []
    for i in range(len(a[0])):
        column = [row[i] for row in a]
        ix, ele = Min([math.fabs(x - 1) for x in column])
        min_ele_column.append(ele)
        min_ix_column.append((i, ix))
        if (i > 51 and i < 189 and ix < 106): # mGluino = 800
            min_ix.append((ix, i))
    return min_ix

# Extract numbers from the file, make an array and plot histograms
f = open("results.txt", "r")
obs_array = [[0 for i in range(21)] for j in range(21)]
exp_array = [[0 for i in range(21)] for j in range(21)]
lower_array = [[0 for i in range(21)] for j in range(21)]
upper_array = [[0 for i in range(21)] for j in range(21)]
hist_obs = r.TH2F("obs", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
hist_exp = r.TH2F("exp", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
hist_upper = r.TH2F("upper", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
hist_lower = r.TH2F("lower", ";mSquark / GeV;mGluino / GeV", 21, 400., 2000., 21, 400., 2000.)
for line in f:
    mSquark, mGluino, obs, exp, upper, lower = [float(x) for x in line.split(", ")]
    i = int((mSquark - 400)/80)
    j = int((mGluino - 400)/80)
    obs_array[i][j] = obs
    exp_array[i][j] = exp
    upper_array[i][j] = upper
    lower_array[i][j] = lower
    bin = GetBin(mSquark, mGluino)
    hist_obs.SetBinContent(bin, obs)
    hist_exp.SetBinContent(bin, exp)
    hist_upper.SetBinContent(bin, upper)
    hist_lower.SetBinContent(bin, lower)

# Interpolate between elements in the array
a_obs = interpolate_array(obs_array, 9)
a_exp = interpolate_array(exp_array, 9)
a_upper = interpolate_array(upper_array, 9)
a_lower = interpolate_array(lower_array, 9)

# Make high resolution histogram
hist_obs_highres = r.TH2F("obs_highres", ";mSquark / GeV;mGluino / GeV", 201, 400., 2000., 201, 400., 2000.)
hist_exp_highres = r.TH2F("exp_highres", ";mSquark / GeV;mGluino / GeV", 201, 400., 2000., 201, 400., 2000.)
hist_upper_highres = r.TH2F("upper_highres", ";mSquark / GeV;mGluino / GeV", 201, 400., 2000., 201, 400., 2000.)
hist_lower_highres = r.TH2F("lower_highres", ";mSquark / GeV;mGluino / GeV", 201, 400., 2000., 201, 400., 2000.)
for i in range(201):
    for j in range(201):
        bin = int( 203*(i+1) + j+1 ) 
        hist_obs_highres.SetBinContent(bin, a_obs[j][i])
        hist_exp_highres.SetBinContent(bin, a_exp[j][i])
        hist_upper_highres.SetBinContent(bin, a_upper[j][i])
        hist_lower_highres.SetBinContent(bin, a_lower[j][i])

# Get contours and make graphs
cont_obs = GetContour(a_obs)
#cont_obs.sort()
x_obs = array.array("d", [])
y_obs = array.array("d", [])
for (p, q) in cont_obs:
    x_obs.append(400 + 8*p)
    y_obs.append(400 + 8*q)
graph_obs = r.TGraph(len(cont_obs), x_obs, y_obs)
graph_obs.SetLineWidth(3)
cont_exp = GetContour(a_exp)
#cont_exp.sort()
x_exp = array.array("d", [])
y_exp = array.array("d", [])
for (p, q) in cont_exp:
    x_exp.append(400 + 8*p)
    y_exp.append(400 + 8*q)
graph_exp = r.TGraph(len(cont_exp), x_exp, y_exp)
graph_exp.SetLineColor(3)
graph_exp.SetMarkerColor(3)
graph_exp.SetLineWidth(3)
cont_upper = GetContour(a_upper)
cont_upper.append((73, 188))
cont_upper.insert(0, (188, 34))
print cont_upper
#cont_upper.sort()
x_upper = array.array("d", [])
y_upper = array.array("d", [])
for (p, q) in cont_upper:
    x_upper.append(400 + 8*p)
    y_upper.append(400 + 8*q)
graph_upper = r.TGraph(len(cont_upper), x_upper, y_upper)
graph_upper.SetLineColor(4)
graph_upper.SetMarkerColor(4)
graph_upper.SetFillColor(0)
graph_upper.SetLineWidth(1002)
cont_lower = GetContour(a_lower)
#cont_lower.sort()
x_lower = array.array("d", [])
y_lower = array.array("d", [])
for (p, q) in cont_lower:
    x_lower.append(400 + 8*p)
    y_lower.append(400 + 8*q)
graph_lower = r.TGraph(len(cont_lower), x_lower, y_lower)
graph_lower.SetLineColor(4)
graph_lower.SetMarkerColor(4)
graph_lower.SetFillColor(4)
graph_lower.SetLineWidth(2002)

# Draw Graphs
c = r.TCanvas("c", "c", 1000, 1000)
multigraph = r.TMultiGraph("exclusion", ";mSquark / GeV;mGluino / GeV")
multigraph.Add(graph_lower)
multigraph.Add(graph_upper)
multigraph.Add(graph_exp)
multigraph.Add(graph_obs)
multigraph.Draw("apl")
multigraph.GetXaxis().SetLimits(600., 1900.)
multigraph.GetYaxis().SetRangeUser(600., 1900.)
c.SaveAs("graph.pdf")

# Draw histograms
hist_obs.Draw("COLZ")
c.SaveAs("ObservedLimit.pdf")
hist_exp.Draw("COLZ")
c.SaveAs("ExpectedLimit.pdf")
hist_upper.Draw("COLZ")
c.SaveAs("ExpectedLimitPlusOneSigma.pdf")
hist_lower.Draw("COLZ")
c.SaveAs("ExpectedLimitMinusOneSigma.pdf")
hist_obs_highres.Draw("COLZ")
c.SaveAs("ObservedLimit_HighRes.pdf")
hist_exp_highres.Draw("COLZ")
c.SaveAs("ExpectedLimit_HighRes.pdf")
hist_upper_highres.Draw("COLZ")
c.SaveAs("ExpectedLimitPlusOneSigma_HighRes.pdf")
hist_lower_highres.Draw("COLZ")
c.SaveAs("ExpectedLimitMinusOneSigma_HighRes.pdf")
