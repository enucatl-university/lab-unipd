#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1I, TCanvas

bins = 7926
def leggi_hist(file_name):
    hist = TH1I(file_name, file_name, bins, 0, bins)
    with open(file_name) as file:
        for i, line in enumerate(file):
            line = float(line)
            hist.SetBinContent(i + 1, line)
    return hist

file_incognito = "incognito-t100k-m20.csv"
file_fondo = "fondo.csv"

incognito = leggi_hist(file_incognito)
fondo = leggi_hist(file_fondo)

incognito.Add(fondo, -1)
fitincognito.Fit("gaus", "WS+", "", 1520, 1555)
incognito.Fit("gaus", "WS+", "", 1610, 1645)
incognito.Draw()

input()
