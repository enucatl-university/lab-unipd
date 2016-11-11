#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from global_tools import *
from math import *

"""Crea gli istogrammi che descrivono l'associazione delle particelle
ricostruite e quelle generate"""

from ROOT import TFile, TTree, TH1D, TCanvas, gStyle, TH2D
import os
import sys

try:
    root_file_name = sys.argv[1]
except IndexError:
    root_file_name = "muon_reco25.1.root"

set_gstyle(gStyle)
root_file = TFile(root_file_name)
dir_name = "PatAnalyzerSkeleton"

"""open tree"""
tree = "ass_muons"
tree = os.path.join(dir_name, tree)
tree = root_file.Get(tree)

#tracks: lin - circ
#######################
hist_stats = 200, -1e-8, 1e-8
in_lin_circ_hist = TH1D("in_lin_circ",
"inner track",
*hist_stats)
tree.Project("in_lin_circ", "d_lin_inner - d_circ_inner")

glob_lin_circ_hist = TH1D("glob_lin_circ",
"global track",
*hist_stats)
tree.Project("glob_lin_circ", "d_lin_global - d_circ_global")
print(glob_lin_circ_hist.GetBinContent(0))
print(glob_lin_circ_hist.GetBinContent(glob_lin_circ_hist.GetNbinsX()+1))

title = "distribution of d_{lin} - d_{circ}"
lin_circ_can = TCanvas("lin_circ_can", title)
lin_circ_can.cd()
set_canvas(lin_circ_can)
lin_circ_can.SetLogy()
set_histogram(in_lin_circ_hist,
"""d_{lin} - d_{circ} #[]{cm}""",
"""entries / 1e-10 #[]{cm}""")
set_histogram(glob_lin_circ_hist, "", "")
in_lin_circ_hist.Draw()
in_lin_circ_hist.SetStats(0)
glob_lin_circ_hist.SetLineColor(2)
glob_lin_circ_hist.Draw("SAME")
legend = lin_circ_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
in_lin_circ_hist.SetTitle(title)
in_mean = in_lin_circ_hist.GetMean()
glob_mean = glob_lin_circ_hist.GetMean()
glob_RMS = glob_lin_circ_hist.GetRMS()
in_RMS = in_lin_circ_hist.GetRMS()
print("global mean, RMS", glob_mean, glob_RMS)
print("inner mean, RMS", in_mean, in_RMS)
#lin_circ_can.SaveAs("lin_circ2.eps")


#global_diff_can = TCanvas("glob_diff_can", "glob_diff_can")
#x_axis = "fabs(d_lin_global - d_circ_global)"
#y_axis = "sqrt(ref_x_global*ref_x_global + ref_y_global*ref_y_global)"
#global_diff_hist = TH2D("glob_diff", "glob_diff", 2000, 0, 1e-4, 1000, 0,
#        500)
#global_diff_hist.SetMarkerStyle(6)
#tree.Project("glob_diff", y_axis + ":" + x_axis)
#global_diff_hist.Draw()

#angle0_can = TCanvas("angle0_can", "angle0_can")
#anglePV_can = TCanvas("anglePV_can", "anglePV_can")
##angle = "atan2(ref_y_global - 0.00013, ref_x_global - 0.03203)"
##angle = "atan2(ref_y_global, ref_x_global) * 180 / %s" %str(pi)
##angle = "atan2(ref_y_global - 0.00013, ref_x_global - 0.03203) * 180 / %s" %str(pi)
#angle0 = "atan2(ref_y_inner, ref_x_inner) * 180 / %s" %str(pi)
#anglePV = "atan2(ref_y_inner - 0.00013, ref_x_inner - 0.03203) * 180 / %s" %str(pi)
##angle = "atan2(ref_y_inner - 0.3, ref_x_inner - 0.04203) * 180 / %s" %str(pi)
##angle_hist = TH1D("angle", "angle", 800, -4, 4)
#angle0_hist = TH1D("angle0", "angle0", 360, -180, 180)
#tree.Project("angle0", angle0)
#anglePV_hist = TH1D("anglePV", "anglePV", 360, -180, 180)
#tree.Project("anglePV", anglePV)
#angle0_can.cd()
#angle0_hist.Draw()
#anglePV_can.cd()
#anglePV_hist.Draw()
#######################
raw_input()
