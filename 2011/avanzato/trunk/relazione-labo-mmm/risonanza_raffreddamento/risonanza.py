#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

from ROOT import TGraph, TGraphErrors, TCanvas, TF1
import style
import sys
style.style.cd()

name_in = sys.argv[1]

can = TCanvas("can", "can")
gr = TGraphErrors(name_in)
gr.SetTitle("curva di risonanza;#nu [Hz];A [V]")
gr.Draw("AP")
fu = TF1("fu_ris", "[0]/sqrt(1+[1]*(x^2-[2]^2)^2)", 300, 700)
fu.SetParameters(1.41,0.00000001,563.7)
fu.SetNpx(100000)
gr.Fit("fu_ris", "W")
can.SaveAs("relazione/img/" + name_in + ".eps") 

print("\\begin{tabular}{r@{ $\\pm$ }lr@{ $\\pm$ }l}")
print("\\multicolumn{2}{c}{$\\nu$ [Hz]} &\\multicolumn{2}{c}{$A$ [V]} \\\\ ")
print("\\hline")
with open(name_in) as file:
    for line in file:
        if "//" in line:
            continue
        line = [float(x) for x in line.split()]
        print("{0[0]:.0f} & {0[2]:.0f} & {0[1]:.3f} & {0[3]:.3f} \\\\ ".format(line))
print("\\end{tabular}")

input()
