#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import sys
from math import sqrt
from potenziometro_resistenza import PotenziometroResistenza
from resistenza_temperatura import ResistenzaTemperatura

class PotenziometroTemperatura:

    def __init__(self, fit_file, tabella_pt, p):
        self.c = PotenziometroResistenza(fit_file, p)
        self.t = ResistenzaTemperatura(self.c.R, self.c.sigma_R, tabella_pt)
        self.T = self.t.T
        self.sigma_T = self.t.sigma_T
        
    def __str__(self):
        return "{0:.2f} \pm {1:.2f}".format(self.T, self.sigma_T)

if __name__ == "__main__":
    fit_file = sys.argv[1]
    p = float(sys.argv[2])
    try:
        file_tabella = sys.argv[3]
    except IndexError:
        file_tabella = "tabellaPT"
    PT = PotenziometroTemperatura(fit_file, file_tabella, p)
    print(PT)
