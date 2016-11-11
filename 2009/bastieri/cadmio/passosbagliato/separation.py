#!/usr/bin/env python
#coding=utf-8

from wavelength import WaveLength
from ROOT import TCanvas

cadmium_wl = [467.8, 480.0, 508.6, 643.8]
errori = [2.2/474.3, 1.9/489.6, 2.1/517.2, 2.7/656.7]
#files = ['blu.txt', 'azzurro2.txt', 'verde2.txt', 'rosso.txt']
files = ['1blu', '2blu', '3verde', '4rosso']
folder = 'miei'
files = [folder + '/' + file for file in files]
print files

for file, wave, errore in zip(files, cadmium_wl, errori):
    wl = WaveLength(file)
    wl.fit_graph()
    a = wl.get_separation(wave)
    c = TCanvas(file, file)
    wl.graph.Draw('AEP')
    raw_input()
    print file, 'slit separation = ', a, errore*a

