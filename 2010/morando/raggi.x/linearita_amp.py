#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TH1I, TF1, TGraphErrors
from read_hist import load_hist_from_file

in_file = "spettro.amp.dat"
out_file = "amp.grafici.out"
with open(out_file, "w") as output:
    with open(in_file) as file:
        for line in file:
            pot, tens, media = [float(x) for x in line.split()]
            err_media = 0.5
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
print(f_pot.GetChisquare(), "/", f_pot.GetNDF())

can_tens = TCanvas(out_file + "2", out_file)
gr_tens = TGraphErrors(out_file, "%*lg %lg %lg %*lg %g %lg")
gr_tens.SetMarkerStyle(8)
gr_tens.Draw("ap")
f_tens = TF1("retta", "pol1")
gr_tens.Fit("retta")
print(f_tens.GetChisquare(), "/", f_tens.GetNDF())
input()
