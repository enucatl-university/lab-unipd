#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("/home/matteo/bin/elaborazione.dati/")
from ds import *

f = DatiSperimentali('distanze.focali', 0, 1) #distanze focali

F = (f.calcmediap(), f.calcerrmediap())

print 'La distanza focale (media pesata) è: %.2f \pm %.2f' %F
