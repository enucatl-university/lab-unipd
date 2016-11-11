#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import sys
from math import sqrt

class ErroriResistenzeWavetek:
    def __init__(self, r):
        err_scala = r*0.01
        exp = len(str(r).split(".")[1])
        err_digit = 4*10**(-exp)
        self.err = sqrt((err_scala**2 + err_digit**2)/3)
        self.r = r

    def __str__(self):
        return "{0:.2f} \pm {1:.2f}".format(self.r, self.err)


if __name__ == "__main__":
    r = float(sys.argv[1])
    err = ErroriResistenzeWavetek(r)
    print(err)
