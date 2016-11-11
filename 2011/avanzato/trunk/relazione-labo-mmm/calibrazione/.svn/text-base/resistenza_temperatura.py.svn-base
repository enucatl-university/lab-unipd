#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

import sys

class ResistenzaTemperatura:

    def __init__(self, R, sigma_R, file_tabella):
        R0 = 100
        with open(file_tabella) as tabella:
            for line in tabella:
                if "//" in line:
                    continue
                else:
                    line = [float(x) for x in line.split()]
                    if line[1]*R0 > R:
                        self.T = line[0]
                        self.sigma_T = sigma_R / (R0 * line[2])
                        break

    def __str__(self):
        return "{0:.2f} \pm {1:.2f}".format(self.T, self.sigma_T)


if __name__ == "__main__":
    R = float(sys.argv[1])
    sigma_R = float(sys.argv[2])
    try:
        file_tabella = sys.argv[3]
    except IndexError:
        file_tabella = "tabellaPT"
    RT = ResistenzaTemperatura(R, sigma_R, file_tabella)
    print(RT)
