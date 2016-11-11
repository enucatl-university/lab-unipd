#!/usr/bin/env python
#coding=utf-8

from array import array
from ROOT import TH1I
import sys

step = array('i')
data = array('i')
file = open(sys.argv[1])
for line in file:
    step.append(int(line.split()[0]))
    data.append(int(line.split()[1]))
file.close()

histogram = TH1I("fondo","fondo",15,115,130)
fondo = TH1I("fondo_scan","scan",4600,-2300,2300)

for s, i in zip(step, data):
    fondo.Fill(s, i)
    histogram.Fill(i)

histogram.Draw()
fondo.Draw()
raw_input('Press ENTER to continue...')


