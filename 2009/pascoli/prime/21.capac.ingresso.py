#!/usr/bin/env python
#coding=utf-8

from __future__ import division
import math
import sys
from array import array
from ROOT import TGraphErrors, TF1

#CONSTANTS
name='capac.ingresso.dat'
output='capac.ingresso.out'
TIME_DIV = 4 #division on time axis
POT_DIV = 0.1 #division on voltage axis
INTERNAL_RES = 1 #internal oscilloscope resistance is 1MOhm
#UNITS:
#voltage: V
#capacity: nF
#resisance: MOhm
#time: ms

def osc_error_v(measure, division):
    err = 3*measure/100
    #err /= math.sqrt(3) #statistical error?
    return err

def osc_error_t(measure, division):
    err = 100*measure/1e6+0.6e-9+division/250
    #err /= math.sqrt(3) #statistical error?
    return err

class TimeConstant(object):
    def __init__(self, file_name):
        file = open(file_name)
        out = open(output, 'w')
        for line in file:
            #calculate errors and dump the content to output file
            #skip comment lines
            if '#' in line:
                continue
            t, v = [float(x) for x in line.split()]
            te = osc_error_t(t, TIME_DIV)
            ve = osc_error_v(v, POT_DIV)
            new_line = [t, v, te, ve]
            new_line = ' '.join([str(x) for x in new_line]) + '\n'
            out.write(new_line)
        file.close()
        out.close()
        #create Graph. ROOT automatically reads columns
        self.graph = TGraphErrors(output)
        self.graph.SetMarkerStyle(7)
        self.func = TF1("exp_decay", "[0]*exp(-x/[1])")
        self.func.SetParameters(2,20)

    def fit_graph(self):
        self.graph.Fit("exp_decay", "Q")
        self.v0 = self.func.GetParameter(0), self.func.GetParError(0)
        self.tau = self.func.GetParameter(1), self.func.GetParError(1)
#        print "%.3f \pm %.3f" %self.v0
#        print "%.3f \pm %.3f" %self.tau

    def get_capacity(self):
        c = (self.tau[0]/INTERNAL_RES, self.tau[1]/INTERNAL_RES)
        return c
        
a = TimeConstant(name)
a.graph.Draw('AEP')
a.fit_graph()
cap = a.get_capacity()
print "oscilloscope capacity is: %.3g \pm %.3g nF" %cap
raw_input('Press ENTER to continue...')
