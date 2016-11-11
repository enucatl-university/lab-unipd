#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1D, TCanvas, TFile, TH2D
import sys

from style import *

style.SetHistLineWidth(1)
style.SetOptStat(110011)
style.cd()

tree_name = "pjmca"

background = sys.argv[2]
background_root_file = TFile(background)
background_tree = background_root_file.Get(tree_name)
background_hist = TH1D("background", "background", 2000, 0, 2000)
background_tree.Project("background", "ch3")

root_file_name = sys.argv[1]
root_file = TFile(root_file_name)
tree = root_file.Get(tree_name)


canvas = TCanvas(root_file_name, root_file_name)
canvas.Divide(2, 2)

intervals = [
        (480, 500),
        (600, 620),
        (700, 740),
        (840, 860),
        (920, 960),
        (1020, 1060),
        (1160, 1180)
        ]


hists = [TH1D(root_file_name + str(i),
    root_file_name + str(i),
    2000, 0, 2000)
    for i in range(4)]

for i in range(4):
    canvas.cd(i + 1)
    tree.Project(root_file_name + str(i), "ch{0}".format(i))
    hists[i].Draw()

revealed_photons = [hists[3].Integral(*interval) for interval in intervals]
background_photons = [background_hist.Integral(*interval) for interval in intervals]

att = [i/i_0 for i, i_0 in zip(revealed_photons, background_photons)]
print(revealed_photons)
print(background_photons)
print(att)
raw_input()
