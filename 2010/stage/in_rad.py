#!/usr/bin/python
#coding=utf-8

from ROOT import TFile, TTree, TH1D, TCanvas, TLegend, TPad, gStyle
from ROOT import TH2D
import os
import sys


try:
    root_file_name = sys.argv[1]
except IndexError:
    root_file_name = "muon_reco25.1.root"

gStyle.SetTitleFillColor(0)

root_file = TFile(root_file_name)
dir_name = "PatAnalyzerSkeleton"
size = 0.04

tree_name = "ass_muons"
tree_name = os.path.join(dir_name, tree_name)
tree = root_file.Get(tree_name)

hist = TH2D("in_rad", "innermost hit and impact parameter", 4000, 0, 1000,
        4000, 0, 1000)

can = TCanvas("hist", "hist")
tree.Project("in_rad", "in_rad:d_lin_global","eta < 0.8")
#can.SetLogy()
can.SetLogx()
hist.SetMarkerStyle(6)
hist.Draw()
#can.SaveAs("in_rad_bilog.root")
raw_input()
