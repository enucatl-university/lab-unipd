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


base_name = "spettro"
extension = ".root"
tree_name = "pjmca"
branch_name = Template("ch$ch")

intervals = {
        1: ((100, 130), (600, 750), (1500, 1700)),
        2: ((120, 150), (720, 870), (1650, 1850)),
        3: ((100, 140), (620, 770), (1500, 1750)),
        4: ((0, 0), (700, 850), (1650, 1900))
        }

energies = array("d", (88, 511, 1274.5)) #keV
energy_error = array("d", (0, 0, 0))

for i in range(1, 5):
    hist_name = base_name + str(i)
    file_name = base_name + str(i) + extension
    root_file = TFile(file_name)
    tree = root_file.Get("pjmca")
    hist = TH1D(hist_name, hist_name, 2000, 0, 2000)
    branch = branch_name.substitute(ch=(i-1))
    tree.Project(hist_name, branch, "{0} > 2".format(branch))
    canvas = TCanvas(hist_name + "canvas", hist_name)

    means = array("d")
    errors = array("d")
    for interval in intervals[i]: 
        if (interval[1] - interval[0]):
            result = hist.Fit("gaus", "QSR+", "", *interval)
            mean = result.Parameter(1)
            error = result.ParError(1)
            sigma = result.Parameter(2)
            means.append(mean)
            errors.append(error)
            print("gaussian mean = ", mean, "\pm", error)
            print("gaussian sigma = ", sigma)

    if (i == 4):
        energies = array("d", (511, 1274.5)) #keV
        energy_error = array("d", (0, 0))
    calibration_graph = TGraphErrors(len(means), energies, means, energy_error, errors)
    calibration = calibration_graph.Fit("pol1", "QS")
    intercept = calibration.Parameter(0), calibration.ParError(0)
    angular_coefficient = calibration.Parameter(1), calibration.ParError(1)
    print("intercept = {0[0]} \pm {0[1]} [ch]".format(intercept))
    print("angular_coefficient = {0[0]} \pm {0[1]} [ch/keV]".format(angular_coefficient))
    hist.Draw()
    canvas.SaveAs(base_name + str(i) + ".eps")
