#!/usr/bin/env python
#coding=utf-8

from array import array
import sys
from malus import Malus
from residuals import ResHist
from ROOT import TCanvas, TGraphErrors, TF1
from math import pi
from err import error

mu0 = 4*pi*1e-7
ls = 0.18
lv = 0.11
N = 3660

files = sys.argv[1:]
phi, phi_err = array('d'), array('d')
sine_curves = TCanvas('malus', "Malus' Law", 1200, 800)
sine_curves.Divide(2, 2)

malus = [Malus(file) for file in files]

for i, m in enumerate(malus):
    sine_curves.cd(i + 1)
    #m.get_phi(1, 50)
    #m.get_phi(1, 100)
#    m.get_phi(175, 225)
    #m.get_phi(180, 260)
    m.get_phi(130, 260)
    m.draw_hist()
    sine_curves.Update()
    phi.extend(m.phi)
    phi_err.extend(m.phi_err)

res = [ResHist(m.histogram, m.cos2) for m in malus]

residuals = TCanvas('malus_res', "Residuals", 1200, 800)
residuals.Divide(2, 2)
for i, r in enumerate(res):
    residuals.cd(i + 1)
    r.res_graph.Draw('AEP')
    r.res_graph.SetMarkerStyle(6)
    residuals.Update()

n = 1
current = [0]*n+[1]*n+[2]*n+[3]*n
current = array('d', current)
for tuple in zip(current, phi, phi_err):
    print "%i %.1f \pm %.1f" %tuple

zeros = array('d', [0]*n*4)
graph = TGraphErrors(n*4, current, phi, zeros, phi_err)
canv = TCanvas('shift', 'shift')
graph.SetMarkerStyle(8)
func = TF1('pol1', 'pol1', 0, 4)
graph.Fit('pol1', 'V')
graph.Draw('AEP')

slope = func.GetParameter(1)
slope_err = func.GetParError(1)
verdet = -(slope*ls) / (mu0*N*lv)
verdet_err = error(verdet, (slope, slope_err))
print 'Verdet = ', verdet, verdet_err
print 'Chi2 / NDF = ', func.GetChisquare(), func.GetNDF()
raw_input()
