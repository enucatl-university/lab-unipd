#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1D, TGraphErrors, TCanvas, TFile
from string import Template
from style import *
from array import array

style.SetHistLineWidth(1)
style.SetOptStat(110011)
style.cd()


base_name = "calibrazione_tac"
extension = ".root"
tree_name = "pjmca"
branch = "ch3"
root_file_name = Template(base_name + "_${extratime}ns" + extension)

intervals = ((1100, 1190),
        (1180,1280))

extra_time = (0, 10) #ns

means = []
errors = []

for interval, t in zip(intervals, extra_time):

    hist_name = base_name + str(t)
    root_file = TFile(root_file_name.substitute(extratime=t))
    tree = root_file.Get("pjmca")
    hist = TH1D(hist_name, hist_name, 800, 800, 1600)
    tree.Project(hist_name, branch)
    canvas = TCanvas(hist_name + "canvas", hist_name)
    result = hist.Fit("gaus", "QSR+", "", *interval)
    mean = result.Parameter(1)
    error = result.ParError(1)
    print(mean, "\pm", error)
    means.append(mean)
    errors.append(error)
    hist.Draw()
    canvas.SaveAs(base_name + str(t) + ".eps")


angular_coefficient = (means[1] - means[0]) / 10
angular_coefficient_error = angular_coefficient * (
        errors[1] / means[1] +
        errors[0] / means[0]
        )


print("angular coefficient = {0} \pm {1} [ch/ns]".format(
    angular_coefficient,
    angular_coefficient_error)
    )

