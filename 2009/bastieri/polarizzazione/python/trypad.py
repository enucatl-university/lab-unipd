#!/usr/bin/env python
#coding=utf-8

from ROOT import TH1D, TCanvas
import sys

file_names = sys.argv[1:]
histograms = []

for file_name in file_names:
    try:
        file = open(file_name)
    except IOError:
        print "file %s not found!" %file_name
        sys.exit(2)
    histogram = TH1D(file_name, file_name, 720, 0, 360)
    for line in file:
        dd, ii = line.split()
        dd, ii = float(dd), float(ii)
        histogram.Fill(dd, ii)
    file.close()
    histograms.append(histogram)

canvas = TCanvas('malus', 'Malus Title', 1200, 800)
canvas.Divide(2, 1)
for i, hist in enumerate(histograms):
    canvas.cd(i+1)
    hist.Draw()
raw_input()
