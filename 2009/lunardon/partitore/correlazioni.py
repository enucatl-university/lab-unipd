#!/usr/bin/env python
#coding=utf-8

import math
from ds import *

s_kv = 7e-3/math.sqrt(3)
s_ki = 7.5e-3/math.sqrt(3)

def sdiff(misure, scala, digit):
	dm = abs(misure[0]-misure[1])
	d2 = 2*digit**2 + (dm*scala)**2
	return math.sqrt(d2/3)

s100 = sdiff((5.027, 5.018), 7e-3, 2e-3)

def sigmaRG(RG, dv, sdv, i, si):
	return RG*math.sqrt((sdv/dv)**2+(si/i)**2)

def norm(misura, *args):
	quadrato = 0.
	for arg in args:
		quadrato += (arg[1]/arg[0])**2
	return misura*math.sqrt(quadrato)

def ddp():
	v51 = (r5[0]*v0[0]/r56[0], norm(r5[0]*v0[0]/r56[0], r56, r5, v0))
	v61 = (r6[0]*v0[0]/r56[0], norm(r6[0]*v0[0]/r56[0], r56, r6, v0))
	v11 = (r1[0]*v0[0]/r1234[0], norm(r1[0]*v0[0]/r1234[0], r1234, r1, v0))
	v21 = (r2[0]*v0[0]/r1234[0], norm(r2[0]*v0[0]/r1234[0], r1234, r2, v0))
	v31 = (r3[0]*v0[0]/r1234[0], norm(r3[0]*v0[0]/r1234[0], r1234, r3, v0))
	v41 = (r4[0]*v0[0]/r1234[0], norm(r4[0]*v0[0]/r1234[0], r1234, r4, v0))
	print v11, v21, v31, v41, v51, v61

#def acquisizionedati():
r1 = (99.7,0.5)
r2 = r1
r4 = r1
r3 = (99.5,0.5)
r5 =  (556.2,2.9)
r6 =  (555.0,2.9)
v1 = (1.258,0.005)
v2 = v1
v4 = (1.257, 0.005)
v3 = (1.254,0.005)
v5 = (2.516,.01)
v6 = (2.509,.01)
r56 = (r5[0]+r6[0],norm(r5[0]+r6[0],r5,r6))
r1234f = r1[0]+r2[0]+r3[0]+r4[0]
r1234 = (r1234f,norm(r1234f,r1,r2,r3,r4))
v0 = (5.025, 0.020)
req = (293.2, 1.5)

scrivivalori(((10.38,10.5), (0.08, 0.1)), 'RA.dat')
RA = DatiSperimentali('RA.dat', 0, 1)
print RA.calcmediap(),  RA.calcerrmediap()
ra = (RA.calcmediap(), RA.calcerrmediap())
i1 = (v0[0]/(req[0]+ra[0]), 0)
i2 = (v0[0]/(r56[0]+ra[0]), 0)
i3 = (v0[0]/(r1234[0]+ra[0]), 0)
print i2, i3,  i1, i2[0]+i3[0]

print 'NUOVI DATI'
i2 = (4.47e-3*(1+ra[0]/r56[0]), 0)
i3 = (12.31e-3*(1+ra[0]/r1234[0]), 0)
i1 = (16.58e-3*(1+ra[0]/req[0]), 0)
print i2, i3,  i1, i2[0]+i3[0]
print 'DDP'
ddp()


p = 2e-3**2/3/5.025**2 + 7e-3**2/3+27e-6

print i1[0]*math.sqrt(p + (2e-3)**2/(3*req[0]**2))
print i2[0]*math.sqrt(p + (2e-3)**2/(3*r56[0]**2))
print i3[0]*math.sqrt(p + (2e-3)**2/(3*r1234[0]**2))

