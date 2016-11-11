#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1I

N_BINS = 1024
def load_hist_from_file(file_name):
    histogram = TH1I(file_name, file_name, N_BINS, 0, N_BINS)
    with open(file_name) as file:
        for i, line in enumerate(file):
            line = line.split()[0]
            line = float(line)
            histogram.SetBinContent(i + 1, line)
    return histogram

if __name__ == "__main__":
    nome = "00mm.dat"
    h1 = load_hist_from_file(nome)
    h1.Draw()
    input()
