#!/usr/bin/env python
#coding=utf-8

import math
from ds import *

def err():
	global e, r56, r1234, r16
	a= 1/r56[0]**2+2/r1234[0]**2+3/r16[0]**2
	return 1/(1/r1234[0]+1/r56[0])*math.sqrt(2*a*e**2)

e = 0.115470053838
sr = 3**(-.5)*9e-3
scala = 75e-4*3**(-.5)
digit = 0.01e-3*3**(-.5)
r1 = (99.7,e)
r2 = r1
r4 = r1
r3 = (99.5,e)
r5 =  (556.2,e)
r6 =  (555.0,e)
r56 = (r5[0]+r6[0],math.sqrt(2)*e)
r1234 = (r1[0]+r2[0]+r3[0]+r4[0],2*e)
r16 = (r56[0]+r1234[0], math.sqrt(6)*e)
R = (1/(1/r1234[0]+1/r56[0]), err())
ra = (10.5, 0.1)

print R

diff = 0.03e-3
c = diff/math.sqrt(2*digit**2+scala**2*diff**2)

print 'compatibilità: ',  c

def sigmai(i, n, req):
	q = scala**2+(digit/i)**2+(e/(ra[0]+req))**2+n*(ra[0]*e/(req*(req+ra[0])))**2
	return i*math.sqrt(q)

si = (sigmai(17.17e-3, 1, r16[0]), sigmai(4.27e-3, 2, r56[0]), sigmai(12.63e-3, 4, r1234[0]))
si23 = math.sqrt(2*digit**2+17.17e-3**2*scala**2)

print 'compatibilità correnti: ', 3e-5/math.sqrt(si[0]**2+si23**2)
print 'i1 ', sigmai(17.17e-3, 1, r16[0])
print 'i2 ', sigmai(4.27e-3, 2, r56[0])
print 'i3 ', sigmai(12.63e-3, 4, r1234[0])


d= 2e-2
print 1/math.sqrt(sr**2+e**2/d**2+R[1]**2/d**2)
