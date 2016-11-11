#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from global_tools import *

"""Crea gli istogrammi 
con le distribuzioni di parametro d'impatto dei B e D"""

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

"""inner lin"""
hist_stats = 80, 0, 0.4
B_d_lin_inner_hist = TH1D("B_d_lin_inner", "B", *hist_stats)
D_d_lin_inner_hist = TH1D("D_d_lin_inner", "D", *hist_stats)
B_d_lin_inner_hist.SetStats(0)
D_d_lin_inner_hist.SetLineColor(2)

tree.Project("B_d_lin_inner", "d_lin_inner", "abs(mother_pdgid) == 521")
tree.Project("D_d_lin_inner", "d_lin_inner", "abs(mother_pdgid) == 411")

[set_histogram(x,
    """d_{lin} #[]{cm}""",
    """entries / 0.005 #[]{cm}""") for x in [B_d_lin_inner_hist, D_d_lin_inner_hist]]

title = "d_{lin} distribution, inner track"
d_lin_inner_can = TCanvas("distribution", title)
d_lin_inner_can.cd()
d_lin_inner_can.SetLogy()
set_canvas(d_lin_inner_can)
B_d_lin_inner_hist.Draw()
D_d_lin_inner_hist.Draw("SAME")
legend = d_lin_inner_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
B_d_lin_inner_hist.SetTitle(title)
d_lin_inner_can.SaveAs("d_lin_inner.eps")

"""inner circ"""
B_d_circ_inner_hist = TH1D("B_d_circ_inner", "B", *hist_stats)
D_d_circ_inner_hist = TH1D("D_d_circ_inner", "D", *hist_stats)
B_d_circ_inner_hist.SetStats(0)
D_d_circ_inner_hist.SetLineColor(2)

tree.Project("B_d_circ_inner", "d_circ_inner", "abs(mother_pdgid) == 521")
tree.Project("D_d_circ_inner", "d_circ_inner", "abs(mother_pdgid) == 411")

[set_histogram(x,
    """d_{circ} #[]{cm}""",
    """entries / 0.005 #[]{cm}""") for x in [B_d_circ_inner_hist, D_d_circ_inner_hist]]

title = "d_{circ} distribution, inner track"
d_circ_inner_can = TCanvas("distribution", title)
d_circ_inner_can.cd()
d_circ_inner_can.SetLogy()
set_canvas(d_circ_inner_can)
B_d_circ_inner_hist.Draw()
D_d_circ_inner_hist.Draw("SAME")
legend = d_circ_inner_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
B_d_circ_inner_hist.SetTitle(title)
d_circ_inner_can.SaveAs("d_circ_inner.eps")

"""global lin"""
B_d_lin_global_hist = TH1D("B_d_lin_global", "B", *hist_stats)
D_d_lin_global_hist = TH1D("D_d_lin_global", "D", *hist_stats)
B_d_lin_global_hist.SetStats(0)
D_d_lin_global_hist.SetLineColor(2)

tree.Project("B_d_lin_global", "d_lin_global", "abs(mother_pdgid) == 521")
tree.Project("D_d_lin_global", "d_lin_global", "abs(mother_pdgid) == 411")

[set_histogram(x,
    """d_{lin} #[]{cm}""",
    """entries / 0.005 #[]{cm}""") for x in [B_d_lin_global_hist, D_d_lin_global_hist]]

title = "d_{lin} distribution, global track"
d_lin_global_can = TCanvas("distribution", title)
d_lin_global_can.cd()
d_lin_global_can.SetLogy()
set_canvas(d_lin_global_can)
B_d_lin_global_hist.Draw()
D_d_lin_global_hist.Draw("SAME")
legend = d_lin_global_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
B_d_lin_global_hist.SetTitle(title)
d_lin_global_can.SaveAs("d_lin_global.eps")

"""global circ"""
B_d_circ_global_hist = TH1D("B_d_circ_global", "B", *hist_stats)
D_d_circ_global_hist = TH1D("D_d_circ_global", "D", *hist_stats)
B_d_circ_global_hist.SetStats(0)
D_d_circ_global_hist.SetLineColor(2)

tree.Project("B_d_circ_global", "d_circ_global", "abs(mother_pdgid) == 521")
tree.Project("D_d_circ_global", "d_circ_global", "abs(mother_pdgid) == 411")

[set_histogram(x,
    """d_{circ} #[]{cm}""",
    """entries / 0.005 #[]{cm}""") for x in [B_d_circ_global_hist, D_d_circ_global_hist]]

title = "d_{circ} distribution, global track"
d_circ_global_can = TCanvas("distribution", title)
d_circ_global_can.cd()
d_circ_global_can.SetLogy()
set_canvas(d_circ_global_can)
B_d_circ_global_hist.Draw()
D_d_circ_global_hist.Draw("SAME")
legend = d_circ_global_can.BuildLegend(0.7, 0.8, 0.9, 0.9)
legend.SetFillColor(10)
B_d_circ_global_hist.SetTitle(title)
d_circ_global_can.SaveAs("d_circ_global.eps")
#raw_input()
