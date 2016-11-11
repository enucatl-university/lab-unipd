#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from global_tools import *

"""Crea gli istogrammi 
con le distribuzioni di parametro d'impatto e pt dei B e D"""

from ROOT import TFile, TTree, TH1D, TCanvas, gStyle, TLine
import os
import sys

try:
    root_file_name = sys.argv[1]
except IndexError:
    root_file_name = "muon_reco24.1.root"

set_gstyle(gStyle)
root_file = TFile(root_file_name)
dir_name = "PatAnalyzerSkeleton"

"""open tree"""
tree = "ass_muons"
tree = os.path.join(dir_name, tree)
tree = root_file.Get(tree)

"""Transverse momentum"""
hist_stats = 100, 0, 50
B_pt_hist = TH1D("B_pt", "B", *hist_stats)
D_pt_hist = TH1D("D_pt", "D", *hist_stats)
B_pt_hist.SetStats(0)
D_pt_hist.SetLineColor(2)

tree.Project("B_pt", "pt", "abs(mother_pdgid) == 521")
tree.Project("D_pt", "pt", "abs(mother_pdgid) == 411")

[set_histogram(x,
    """p_{t} #[]{GeV/c}""",
    """entries / 0.5 #[]{GeV/c}""") for x in [B_pt_hist, D_pt_hist]]

title = "p_{t} distribution"
pt_can = TCanvas("p_{t} distribution", title)
pt_can.cd()
pt_can.SetLogy()
B_pt_hist.Draw()
D_pt_hist.Draw("SAME")
legend = pt_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
B_pt_hist.SetTitle(title)
raw_input()
