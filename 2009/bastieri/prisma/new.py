#!/usr/bin/python
#coding=utf-8

import sys
import math
from prism import RefractedCadmium, CauchyRelation, LinearRelation
from ROOT import TCanvas, TMath

correlation = 0.97667 #obtained from minuit fit.
#correlation = 0.97723 #MARCO
#couldn't find out how to pass the data from
#the program itself

files = sys.argv[1:]
n_files = len(files)

ref_index = []
err_ref_index = []
#wl = open('wavelengths').read().split()
#wl = [float(x) for x in wl]
#wl = [467.8, 480.0, 508.6, 643.8]
wl = [398.2, 467.8, 480.0, 508.6, 643.8]
#wl2 = [1/x**2 for x in wl]

#print wl2

draw_graph = True

for file in files:
    r = RefractedCadmium(file)
    n = r.n
    ref_index.append(n)
    err_ref_index.append(r.errn)
    print n, r.errn

cr = CauchyRelation(ref_index, err_ref_index, wl)

print'Fitted Cauchy parameters: '
A, B, C = zip(cr.pars, cr.parerrs)
print 'A = %.5f \pm %.5f' %A
print 'B = %.0f \pm %.0f' %B

#evaluate cauchy relation to find Abbe's number
cauchy = cr.func.Eval
nferro, nblu, nrosso = cauchy(587.6), cauchy(480.0), cauchy(643.8)
abbe = (nferro - 1)/(nblu - nrosso)

print'Abbe = %.2f' %abbe

npoints = 4
ndf = npoints-2
print 'correlation coefficient r = ', correlation
t = correlation*math.sqrt(ndf/(1-correlation**2))

print 'Student t = ', t
prob = TMath.StudentI(t, ndf)
print 'probability = ', (1-prob)*100, '%'

if draw_graph:
    c = TCanvas('Cauchy Relation', 'Cauchy Relation', 1200, 600)
    g = cr.graph
    res = cr.r.graph
    c.Divide(2, 1)
    c.cd(1)
    g.Draw('AEP')
    c.cd(2)
    res.Draw('AEP')
    c.SaveAs('cauchy.eps')
    raw_input('Press ENTER to continue...')
