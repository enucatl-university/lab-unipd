#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TMath, TH1D, TRandom3

h1 = TH1D("gaus", "gaus", 200, -10, 10)
h2 = TH1D("uniform", "uniform", 200, -10, 10)

rand = TRandom3()
for i in xrange(3500):
    a = rand.Gaus()
    b = rand.Uniform(-1, 1)
    h1.Fill(a)
    h2.Fill(b)

h1.Draw()
h2.Draw("SAME")
kolm_prob = h1.KolmogorovTest(h2, "D")
print("kolmogorov probability that the distribution are the same is",
        kolm_prob)
raw_input()
