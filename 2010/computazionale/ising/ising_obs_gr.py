#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TGraph

def format(i):
    list = ["%*lg" for _ in range(5)]
    list[0] = "%lg"
    list[i] = "%lg"
    return " ".join(list)

file_names = ["observed%i" %i for i in [30,50]]
y_titles = ["energy #[]{J}",
        "magnetization",
        "Cv",
        "#chi"]

for file_name in file_names:
    with open(file_name) as input:
        for i in range(1,5):
            can = TCanvas("can%i" %i, "ising")
            graph = TGraph(file_name, format(i))
            can.SetFillColor(0)
            graph.SetMarkerStyle(8)
            graph.GetXaxis().SetDecimals()
            graph.GetYaxis().SetDecimals()
            graph.GetXaxis().SetTitle("temperature #[]{K}")
            graph.GetYaxis().SetTitle(y_titles[i-1])
            graph.Draw("AP")
            can.SaveAs(file_name + "_%i.eps" %i)
