#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

import sys
from math import sqrt

R = sys.argv[1]
R=float(R)
err = R*0.02

print("{0:.2f} \pm {1:.2f}".format(R, err))



