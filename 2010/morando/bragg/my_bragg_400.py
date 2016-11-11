#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1D, TCanvas, TH1S, TMath
import Bragg
import subprocess
import sys

p = 400
n = 1500
b = 80

bragg = Bragg.Bragg(p)
events_inside_hist = TH1D("inside", "inside", 60, 140, 180)
bragg.ntuple.Draw("maxC>>inside",
"maxC < 180 && maxC > 149 && integr > 5400",
"goff")

bragg_max = events_inside_hist.GetMean()

try:
    args = (p, n, b, bragg_max)
    retcode = subprocess.call("my_bragg_400 dati/%i_ %i %i %f" %args, shell=True)
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=sys.stderr)
    else:
        print("Child returned", retcode, file=sys.stderr)
except OSError, e:
    print("Execution failed:", retcode, file=sys.stderr)

bragg_new = Bragg.Bragg(p)
events_escaped_can = TCanvas("escaped_can", "escaped_can")
events_escaped_hist = TH1S("escaped", "escaped", 30, 30, 60)
bragg.ntuple.Draw("deltaT>>escaped",
"maxC < 149 && integr > 5000"
)

distance = 11e-2
escape_time = events_escaped_hist.GetMean() * 1e-7

b_600 = Bragg.Bragg(600)
b_600.ntuple.Draw("energy_fraction", b_600.spectral_lines[0])
print(escape_time)


electron_beta = distance / escape_time / TMath.C()
print(electron_beta)
raw_input()
