#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1I, TCanvas, TGraph, TGraphErrors, TF1, TMath
from read_hist import load_hist_from_file
from math import *

class Thickness:

    def __init__(self, name):
        self.name = name
        self.canvas = TCanvas(name, name)
        self.canvas.SetFillColor(0)
        self.name_lin = name + "_lin"
        self.linearize()
        self.make_graph()

    def linearize(self):
        with open(self.name) as file:
            with open(self.name_lin, "w") as out_file:
                for line in file:
                    x, i = [float(_) for _ in line.split()]
                    i_err = 1 / sqrt(i)
                    i = log(i)
                    output_line = [x, i, 0, i_err]
                    output_line = " ".join([str(x) for x in output_line])
                    output_line += "\n"
                    out_file.write(output_line)

    def make_graph(self):
        self.graph = TGraphErrors(self.name_lin)
        self.graph.SetTitle(self.name)
        self.graph.GetYaxis().SetTitle("log(n_events)")
        self.graph.GetXaxis().SetTitle("thickness #[]{#mu m}")
        self.graph.SetMarkerStyle(8)
        self.graph.Fit("pol1")

    def draw(self):
        self.canvas.cd()
        self.graph.Draw("ap")

    def save(self):
        self.canvas.SaveAs(self.name + ".eps")

gd = "Gd"
cu = "Cu"

gd = Thickness(gd)
gd.draw()
gd.save()
cu = Thickness(cu)
cu.draw()
cu.save()
input()
