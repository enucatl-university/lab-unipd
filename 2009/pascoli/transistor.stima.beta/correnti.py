#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

Rb = 149.3
Rc = 1.008
v0 = 15.03

with open('tabdafare') as file:
    for line in file:
        va, vb, vc = map(float, line.split())
        ib, ic = (va - vb) / Rb, (v0 - vc) / Rc
        print(va, vb, vc, "%.3f %.2f" %(ib, ic), "%i" %(ic/ib))
