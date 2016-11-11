#!/usr/bin/env python
#coding=utf-8
from __future__ import division
import math


print """1. Misura della resistenza interna del generatore di funzioni.
R = R_1*V_out/(V_in-V_out)"""

#tutte le quantità sono riportate come (valore, errore)
r_1 = (56.0, 0.7) #resistenza di carico misurato con T110B, FS 200 ohm
v_in = (1.48, 0.01) #tensione ai capi del generatore, con circuito aperto
v_out = (0.792, 0.01) #tensione ai capi del generatore, con la R1 collegata

res = r_1[0]*(v_in[0]-v_out[0])/v_out[0]
err_res = res*0.005
                    
                    

r = (res, err_res)

print "resistenza interna = %.2f \pm %.2f \ohm" %r
