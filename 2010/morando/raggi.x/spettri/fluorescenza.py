#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TH1I
from read_hist import load_hist_from_file

def fit(hist, min, max):
    hist.GetXaxis().SetRange(min, max)
    mean = hist.GetMean()
    mean_err = hist.GetMeanError()
    hist.GetXaxis().SetRange()
    return mean, mean_err

dist = ["00", "25", "44", "68", "90"]
dist = ["Gd"+ _ + "mu.dat" for _ in dist]

histograms = [load_hist_from_file(file_name) for file_name in dist]
#histograms[3].Draw()
#sum = histograms[0]
#sum.Draw()
first = 4
for i in range(first, 5):
    histograms[first].Add(histograms[i])

sum = histograms[first]
sum.Draw()
media, errore = fit(sum, 230, 280)
print(media, errore)
input()
