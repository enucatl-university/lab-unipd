#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from global_tools import *
from math import *
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


glob_inn_can = TCanvas("glob_inn_can", "glob_inn_can")
glob_hist = TH1D("glob", "global track", 1000, 0, 500)
inner_hist = TH1D("inner", "inner track", 1000, 0, 500)
tree.Project("glob", "d_lin_global")
tree.Project("inner", "d_lin_inner")
glob_hist.SetStats(0)
glob_hist.SetFillColor(0)
glob_hist.Draw()
inner_hist.Draw("SAME")
legend = glob_inn_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
glob_hist.SetTitle("d distribution")
glob_inn_can.SetLogx()
glob_inn_can.SetLogy()
set_canvas(glob_inn_can)
inner_hist.SetLineWidth(2)
inner_hist.SetLineColor(2)
set_histogram(glob_hist,
        """d #[]{cm}""",
        """entries / 0.5 #[]{cm}""")

glob_inn_can.SaveAs("glob_inn2.eps")
#######################
#raw_input()
