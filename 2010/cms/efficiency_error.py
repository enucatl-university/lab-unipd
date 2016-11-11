#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import Math

f = Math.fdistribution_quantile

a = 0.682689492137 #1 sigma

N = [13107 + 57670 + 232573, 59795 + 673518 + 3515450]
for n in N:
    eup = f(1 - a, 2, 2*n) / (n + f(1-a, 2, 2*n))
    print(eup)
    print(1425* eup)
    print()
