#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1D, TCanvas, TFile, TH2D
import sys

from style import *

style.SetHistLineWidth(1)
style.SetOptStat(110011)
style.cd()


selections = {"2":
        [
            "1000 < ch3",
            "ch3 < 1300",
            "600 < ch0",
            "ch0 < 750",
            "700 < ch1",
            "ch1 < 850"
        ],
        "3":
        [
            "1000 < ch3",
            "ch3 < 1300",
            "ch0 < 600",
            "ch1 < 750",
            "ch2 < 600",
            "300 < ch0",
            "400 < ch1",
            "300 < ch2"
        ],
        }


#C = a + b E
#((a, sigma_a), (b, sigma_b)...
calibration = [
        ((37.2947460204, 0.0821031655421),
        (1.24197127531, 0.00013659538661)),
        ((128.613363685, 0.0853601013818),
        (1.2933026704, 0.000132253787011)),
        ((48.9236376144, 0.0912198919444),
        (1.24853478884, 0.000149853387339)),
        ]



selection = " && ".join(selections[sys.argv[1][0]])


root_file_name = sys.argv[1]
root_file = TFile(root_file_name)
tree = root_file.Get("pjmca")

#can2 = TCanvas("2dcan", "2dcan")
#twodim = TH2D("2d", "2d", 1950, 50, 2000, 1950, 50, 2000)
##tree.Project("2d", "ch0:ch1", "1000 < ch3 && ch3 < 1300")
#tree.Project("2d", "ch0:ch1")
#twodim.SetMarkerStyle(1)
#twodim.Draw()
#input()

canvas = TCanvas(root_file_name, root_file_name)
canvas.Divide(2, 2)
hists = [TH1D(root_file_name + str(i), root_file_name + str(i), 1950, 50,
    2000) for i in range(3)]
hists.append(
        TH1D(root_file_name + "3", root_file_name + "3", 800, 800,
    1600))

for i in range(4):
    canvas.cd(i + 1)
    tree.Project(root_file_name + str(i), "ch{0}".format(i), selection)
    hists[i].Draw()

canvas.SaveAs(root_file_name + ".eps")

centroids = [(h.GetMean(), h.GetMeanError()) for h in hists[:3]]

for cal, centroid in zip(calibration, centroids):
    energy = (centroid[0] - cal[0][0]) / cal[1][0]
    
    sigma_energy = energy * (
            cal[0][1] / cal[0][0] +
            cal[1][1] / cal[1][0] +
            centroid[1] / centroid[0]
    )

    print("Canale centroide = {0[0]:.1f} \pm {0[1]:.1f} ch".format(centroid))
    print("Energia centroide = {0:.1f} \pm {1:.1f} keV".format(energy, sigma_energy))


raw_input()
