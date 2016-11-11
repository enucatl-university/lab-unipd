#!/usr/bin/python
#coding=utf-8

import sys
from waveLength import *

nFiles = len(sys.argv)

print waveLength.__doc__

for i in range(1, nFiles):
	wl = waveLength( sys.argv[i] )
	wl.fitGraph()
	wl.getWaveLen()
#	wl.saveToEps()
#	wl.showGraph()
