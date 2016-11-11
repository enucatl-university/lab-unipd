#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1I, TCanvas, TGraph, TGraphErrors, TF1, TMath
from read_hist import load_hist_from_file
from math import *


#apre file e calcola integrali ed errori come poisson
prefissi = ['00', '04', '08', '12', '16', '20']
suffisso = "mm.dat"
nomi_file = [_ + suffisso for _ in prefissi]
histograms = [load_hist_from_file(file) for file in nomi_file]
intensity = [h.Integral(320, 380) for h in histograms]
intensity_error = [sqrt(n) for n in intensity]

#linearizzazione
intensity = [1 / x**0.5 for x in intensity]
intensity_error = [0.5 * i ** 3 * old_err
        for i, old_err in zip(intensity, intensity_error)]

out_intensity = "intensity.out"
with open(out_intensity, "w") as out_file:
    for dist, intens, int_err in zip(prefissi, intensity, intensity_error):
        line = dist + " " + str(intens) + " " + "0" + " " + str(int_err) + "\n"
        out_file.write(line)

can = TCanvas("dist", "dist")
can.SetFillColor(0)
intensity_graph = TGraphErrors(out_intensity)
intensity_graph.SetTitle()
line = TF1("line", "pol1")
intensity_graph.SetMarkerStyle(8)
intensity_graph.Fit("line")
intensity_graph.GetYaxis().SetDecimals()
intensity_graph.GetYaxis().SetTitle("I^{-1/2} #[]{n_events^{-1/2}}")
intensity_graph.GetYaxis().SetDecimals()
intensity_graph.GetXaxis().SetTitle("distance #[]{mm}")
intensity_graph.Draw("ap")
r = intensity_graph.GetCorrelationFactor() #correlation coefficient=?
print(r)
#r = 0.826 #correlation coefficient=?
npoints = 6
ndf = npoints-2
t = r * sqrt(ndf / (1 - r**2))
prob = TMath.StudentI(t, ndf)
print('probability = ', (prob)*100, '%')
can.SaveAs("distance.eps")
input()
