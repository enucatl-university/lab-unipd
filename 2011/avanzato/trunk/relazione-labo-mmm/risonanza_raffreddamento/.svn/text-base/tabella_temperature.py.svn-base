#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
import sys
from calibrazione.potenziometro_temperatura import PotenziometroTemperatura


V0 = 32
T0 = 220

calibrazione_pot = "../calibrazione/fit.calibrazione.potenziometro1.oscilloscopio"
calibrazione_temp = "../calibrazione/tabellaPT"

for pot in range(2, 80, 2):
    pot = pot / 10
    pt = PotenziometroTemperatura(calibrazione_pot, calibrazione_temp, pot)
    T = pt.T
    V = (T - 30) * V0 / T0
    print("{0:.0f} {1:.2f}".format(T, V))
