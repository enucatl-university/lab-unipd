#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TF1, TCanvas, TH1D, TFile
from style import *

file_name = "ZMass_withdata_full_selection.root"
root_file = TFile(file_name)

canvas = root_file.Get("comparison")
histogram = canvas.GetPrimitive("Data")
legend = canvas.GetPrimitive("TPave")
stack = canvas.GetPrimitive("stack")
bw = TF1("bw", "[1] / ((x**2 - [0]**2)**2 +2.4952**2*[0]**2)", 40, 140)
bw.SetParameter(0, 90)
bw.SetParameter(1, 50)
bw.SetParLimits(0, 87, 93)
bw.SetNpx(100000)

histogram.Fit("bw","")

new_can = TCanvas("c", "c")
new_can.cd()
new_can.SetFillColor(0)
maximum = bw.GetMaximum()
stack.SetMaximum(maximum *1.1)
stack.Draw()
histogram.Draw("esame")
bw.Draw("same")
legend.Draw()
new_can.SaveAs("mass_fit.eps")
raw_input()
