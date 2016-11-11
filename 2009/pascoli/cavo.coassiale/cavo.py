#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import math
     
def osc_error_t(measure, division):
    err = 100*measure/1e6+0.6e-9+division/250
    return err

l = (49.95, 0.02)
v0 = 608
vr = 536
alpha = 1 / (2 * l[0]) * math.log(v0 / vr)
alpha_err = alpha * l[1] / l[0]
print(alpha, alpha_err)

Z0 = (50, 0.25)
t = (504e-9, osc_error_t(504e-9, 100e-9))
v = (2*l[0]/t[0], 2*l[0]/t[0] * (l[1] / l[0] + t[1] / t[0]))
Rtot = (3.0, 3.0*0.5/100)
R = (Rtot[0]/l[0], Rtot[0] / l[0] * (Rtot[1] / Rtot[0] + l[1] / l[0]))
print("velocità = %.4g pm %.4g" %v)
print(l[1]/l[0], t[1]/t[0])
G = (R[0] / Z0[0]**2, R[0] / Z0[0]**2 * (2*Z0[1]/Z0[0] + R[1]/R[0]))
L = (Z0[0] / v[0], Z0[0] / v[0] * (Z0[1] / Z0[0] + v[1] / v[0]))
C = (1 / (Z0[0]*v[0]), 1/(Z0[0]*v[0]) * (Z0[1] / Z0[0] + v[1] / v[0]))
print(G, L, C)
print("resistenza per metro = %.4g pm %.4g" %R)
