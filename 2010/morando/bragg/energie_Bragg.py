#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TTree, TH1D, TFile, TLegend, gStyle, TF1, TGraphErrors
import Bragg

gStyle.SetOptStat(0)
def get_mean(hist):
    mean = hist.GetMean()
    mean_err = hist.GetMeanError()
    return mean, mean_err

bragg = [Bragg.Bragg(p) for p in Bragg.pressures]
[b.draw_energy() for b in bragg]
[b.draw_bragg_max() for b in bragg]
bragg_means = [b.bragg_max_means() for b in bragg] 
energy_means = [b.mean_energies() for b in bragg]
#gaussian = [b.gaussian_fit() for b in bragg] 
#kolm_probabilities = [b.kolmogorov_matrix() for b in bragg]
#for matrix in kolm_probabilities:
#    for line in matrix:
#        print("%.3g %.3g %.3g" %tuple(line))
#    print()

print("massimi di Bragg:")
for line in bragg_means:
    for mean in line:
        print("%.2f \pm %.2f" %mean, end="    ")
    print()
print("\n")

#for line in gaussian:
#    for mean in line:
#        print("%.2f \pm %.2f" %mean, end="    ")
#    print()

input()
