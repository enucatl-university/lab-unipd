#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import sys
from math import sqrt

class PotenziometroResistenza:
    def __init__(self, fit_file, p):
        """
        fit_file: file con calibrazione del potenziometro
        P:  valore letto sul potenziometro"""
        a, sigma_a, b, sigma_b = [float(x) for x in open(fit_file).read().split()]
        sigma_p = 0.01
        self.R = a * p + b
        self.sigma_R = sqrt(
               p**2 * sigma_a**2 + 
               a**2 * sigma_p**2 +
               sigma_b**2)

    def __str__(self):
        return "{0:.2f} \pm {1:.2f}".format(self.R, self.sigma_R)

        


#uso: python ....py file_fit 5.54

if __name__ == "__main__":
    fit_file = sys.argv[1]
    p = sys.argv[2]
    c = PotenziometroResistenza(fit_file, p)
    print(c)
