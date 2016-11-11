#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TGraphErrors

pressures = [600, 550, 500, 450]
pressures = [str(p) + "_calib.dat" for p in pressures]

cans = [TCanvas(p, p) for p in pressures]
graphs = [TGraphErrors(p) for p in pressures]

for c, g in zip(cans, graphs):
    c.cd()
    g.SetMarkerStyle(8)
    g.GetYaxis().SetRangeUser(5700, 6700)
    g.Fit("pol1", "")
    g.Draw("ap")
raw_input()
