#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from global_tools import *

"""Crea gli istogrammi che descrivono l'associazione delle particelle
ricostruite e quelle generate"""

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
tree = "r_pt_tree"
tree = os.path.join(dir_name, tree)
tree = root_file.Get(tree)

#draw delta r distribution
#######################
delta_r_hist = TH1D("delta_r",
"distribution of #Delta R of generated-reconstructed pair",
300, 0, 0.3)
tree.Project("delta_r", "r")

delta_r_can = TCanvas("delta_r_can",
"distribution of #Delta R of generated-reconstructed pairs")
delta_r_can.cd()
set_canvas(delta_r_can)
delta_r_can.SetLogy()
set_histogram(delta_r_hist, "#Delta R", "entries / 0.001")
line = TLine(0.1, 0, 0.1, delta_r_hist.GetMaximum())
set_line(line)
delta_r_hist.Draw()
line.Draw("SAME")
delta_r_can.SaveAs("delta_r.eps")
#######################

#draw delta pt distribution
#######################
delta_pt_hist = TH1D("delta_pt",
"distribution of #Delta p_{t} / p_{t} of generated-reconstructed pair",
200, -1, 1)
tree.Project("delta_pt", "rel_delta_pt")

delta_pt_can = TCanvas("delta_r_can",
"distribution of #Delta R of generated-reconstructed pairs")
delta_pt_can.cd()
set_canvas(delta_pt_can)
delta_pt_can.SetLogy()
set_histogram(delta_pt_hist, "#Delta p_{t} / p_{t}", "entries / 0.01")
line = TLine(0.1, 0, 0.1, delta_pt_hist.GetMaximum())
line2 = TLine(-0.1, 0, -0.1, delta_pt_hist.GetMaximum())
set_line(line)
set_line(line2)
delta_pt_hist.Draw()
line.Draw("SAME")
line2.Draw("SAME")
delta_pt_can.SaveAs("delta_pt.eps")
#######################
#raw_input()
