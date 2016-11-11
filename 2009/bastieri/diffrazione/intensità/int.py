#!/usr/bin/python
#coding=utf-8

import sys
import time
from array import array
from ROOT import gROOT
from ROOT import TGraph, TCanvas, TF1, TAttMarker

def mi( fileName ):
	f = open( fileName )
	maxIntensity = 0
	for line in f:
		readIntensity = float( line.split()[1] )
		if  readIntensity > maxIntensity:
			maxIntensity = readIntensity
	f.close()
#	maxIntensity
	return maxIntensity

gROOT.Reset()

nFiles = len(sys.argv) - 1

n2 = array( 'd' )
intensity = array( 'd' )

for i in range(nFiles):
	n2.append( ( i+2 )**2 )
	intensity.append( mi(sys.argv[i+1]) )
	print n2[i], intensity[i]

c1 = TCanvas( 'c1', 'A Simple Graph Example' )
gr = TGraph( nFiles, n2, intensity )
line = TF1( 'line',  'pol1',  0, 20 )
gr.SetMarkerStyle( 8 )
gr.Fit( 'line', 'VR' )
gr.Draw( 'AP' )
time.sleep(100)
