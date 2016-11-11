#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TGraph, TCanvas, TAxis

def set_graph_style(graph):
                           
canvas = TCanvas("salita_discesa","salita_discesa")
canvas.Divide(2,1)
file_salita = "salita.dat"
file_discesa = "discesa.dat"
canvas.cd(1)
graph_salita = TGraph(file_salita)

