#!/usr/bin/env python
#coding=utf-8

"""
\t\tspectrum.py
run ./spectrum.py data_file1 data_file2 ...
default version only prints wavelength.
Uncomment lines in order to get
more info (graphs, fit stats, ...)
"""

import sys, getopt

#avoids ROOT catching command line arguments, must be done before import ROOT
files = sys.argv[1:]
sys.argv = []

from wavelength import WaveLength

try:
    opts, args = getopt.getopt(files, "h", ["help"])
except getopt.GetoptError:
    print __doc__
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print __doc__
        print WaveLength.__doc__
        sys.exit(2)

print 'run with -h or --help for help'

for file in files:
    try:
        wl = WaveLength(file)
    except IOError:
        print 'File \'%s\' not found!' %file
        sys.exit(2)
    wl.fit_graph()
#    wl.show_fit_stats()
    wave = wl.wavelen
    print 'lambda %s = %.1f \pm %.1f nm' %(wl.name, wave[0], wave[1])
#    wl.show_res_graph()
    wl.save_res_to_eps()
#    wl.show_graph()
    wl.save_to_eps()

