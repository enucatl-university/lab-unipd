#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TH1I, TF1, TGraphErrors
from read_hist import load_hist_from_file

def fit(hist, min, max):
    hist.GetXaxis().SetRange(min, max)
    mean = hist.GetMean()
    mean_err = hist.GetMeanError()
    hist.GetXaxis().SetRange()
    return mean, mean_err

nomi_file = ["preamp1.dat", "amp3.dat"]
h1 = load_hist_from_file(nomi_file[0])

limiti = [(130, 210),
        (290, 360),
        (460, 520),
        (560, 610),
        (631, 690),
        (730, 780),
        (800, 850),
        (870, 930),
        (950, 1020)]

means = [fit(h1, *tup) for tup in limiti]
for mean in means:
    print(mean)
#h1.Draw()

in_file = "spettro.preamp.dat"
out_file = "preamp.grafici.out"
with open(out_file, "w") as output:
    with open(in_file) as file:
        for line, tuple in zip(file, means):
            pot, tens, _ = [float(x) for x in line.split()]
            media, err_media = tuple
            new_line = [pot, tens, media, 0, 0.03*tens, err_media]
            new_line = [str(x) for x in new_line]
            new_line = " ".join(new_line) + "\n"
            output.write(new_line)

can_pot = TCanvas(out_file, out_file)
gr_pot = TGraphErrors(out_file, "%lg %*lg %lg %lg %*g %lg")
gr_pot.SetMarkerStyle(8)
gr_pot.Draw("ap")
f_pot = TF1("retta", "pol1")
gr_pot.Fit("retta")
print(gr_pot.GetCorrelationFactor())
print(f_pot.GetChisquare(), "/", f_pot.GetNDF())

can_tens = TCanvas(out_file + "2", out_file)
gr_tens = TGraphErrors(out_file, "%*lg %lg %lg %*lg %g %lg")
gr_tens.SetMarkerStyle(8)
gr_tens.Draw("ap")
f_tens = TF1("retta", "pol1")
gr_tens.Fit("retta")
print(f_tens.GetChisquare(), "/", f_tens.GetNDF())
input()
