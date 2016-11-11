#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TFile, TTree, TH1D, TCanvas, TLegend, TPad, gStyle
import os
import sys


try:
    root_file_name = sys.argv[1]
except IndexError:
    root_file_name = "muon_reco24.1.root"

gStyle.SetTitleFillColor(0)

root_file = TFile(root_file_name)
dir_name = "PatAnalyzerSkeleton"
size = 0.04

def draw_branch(name, hist_stats, cut=""):
    h_D = TH1D("D" + name, "#mu from D", *hist_stats)
    h_B = TH1D("B" + name, "#mu from B", *hist_stats)
    h_D.SetLineColor(2)
    h_D.SetLineWidth(2)
    h_B.SetLineWidth(2)
    trees = {"B":"B_tree", "D":"D_tree"}
    for tree in trees:
        trees[tree] = os.path.join(dir_name, trees[tree])
        trees[tree] = root_file.Get(trees[tree])
        trees[tree].Project(tree + name, name, cut)

    can = TCanvas("can", "can")
    can.cd()
    h_D.Draw()
    h_B.Draw("SAME")
    can.SetFillColor(10)
    can.SetLogy()
    legend = can.BuildLegend(0.7, 0.8, 0.9, 0.9)
    legend.SetFillColor(10)
    h_D.GetXaxis().SetTitle(x_axis_title)
    h_D.GetYaxis().SetTitle(y_axis_title)
    h_D.GetXaxis().SetDecimals()
    h_D.GetYaxis().SetDecimals()
    h_D.GetXaxis().SetTitleSize(size)
    h_D.GetYaxis().SetTitleSize(size)
    h_D.GetYaxis().SetTitleOffset(1.2)
    h_D.GetXaxis().SetLabelSize(size)
    h_D.GetYaxis().SetLabelSize(size)
    h_D.SetTitle(name)
    h_D.SetStats(0)
    can.SaveAs("BD" + name + ".gif")

y_axis_title = "entries / 0.005 #[]{cm}"
x_axis_title = "impact parameter #[]{cm}"
lin_title =  "linear reconstruction"
circ_title = "circular reconstruction"
title =  "B and D, distribution of impact parameter d, "
titles = {"d_lin":title + lin_title, "d_circ": title + circ_title}
hist_stats = 200, 0, 1

for name in titles:
    draw_branch(name, hist_stats)

hist_stats = 100, 0, 50
y_axis_title = "entries / 0.5 #[]{GeV}"
x_axis_title = "pt #[]{GeV}"
lin_title =  "linear reconstruction"
circ_title = "circular reconstruction"
title =  "B and D, distribution of transverse momentum pt, "
titles = {"d_lin":title + lin_title, "d_circ": title + circ_title}
name = "pt"

draw_branch(name, hist_stats)
#raw_input()
