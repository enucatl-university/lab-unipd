#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from HistogramParameters import lumi
import math

lumi *= 1e3
eff = 0.41
n_zee = 48750
eff_err = math.sqrt(eff * (1 - eff) / n_zee)
sigma = 30 / lumi / (eff * n_zee / 1e5)
sigma_err = sigma * eff_err / eff
print("Z cross section = {0} \pm {1} (stat.)".format(sigma, sigma_err))
