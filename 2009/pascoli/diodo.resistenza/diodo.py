#!/usr/bin/env python
#coding=utf-8

"""3.diodo requires t, v_in, v_out in a three column, white space separated
file"""

from __future__ import division, print_function
import math
import sys
from array import array
from ROOT import TCanvas, TGraphErrors, TF1, TMath, TAxis

file_name = 'diodo2'
name = file_name + '.dat'
output = file_name + '.out'
TIME_DIV = 250 #division on time axis
POT_DIV = 1 #division on voltage axis
R = (1, 0.006)#resistance should be set so that current is 5mA
#UNITS:
#voltage: V
#resisance: kOhm
#time: ns

def osc_error_v(measure, division):
    if measure:
        err = 3*measure/100
    else:
        err = division/10
    return err

def osc_error_t(measure, division):
    err = 100*measure/1e6+0.6e-9+division/250
    return err
 
class DiodeCurrent(object): 
    def __init__(self, file_name):
        file = open(file_name)
        out = open(output, 'w')
        for line in file:
            #calculate errors and dump the content to output file
            if '#' in line:
                continue
            t, vin, vout = [float(x) for x in line.split()]
            te = osc_error_t(t, TIME_DIV)
            vd = vin - vout
            voute = osc_error_v(vout, POT_DIV)
            vde = osc_error_v(vd, POT_DIV)
            id = vout/R[0]
            if vout:
                ide = id*((voute/vout)+(R[1]/R[0]))
            else:
                ide = id*(R[1]/R[0])
            new_line = [vd, id, vde, ide]
            new_line = ' '.join([str(x) for x in new_line]) + '\n'
            out.write(new_line)
        file.close()
        out.close()
        #create Graph. ROOT automatically reads columns
        self.graph = TGraphErrors(output)
        self.graph.SetMarkerStyle(7)
        self.func = TF1("shockley", "[0]*(exp(x/[1])-1)", 0.1, 1)
        self.func.SetParameters(5, 0.026)

    def fit_graph(self):
        self.graph.Fit("shockley", "QRW")
        self.v0 = self.func.GetParameter(0), self.func.GetParError(0)
        self.tau = self.func.GetParameter(1), self.func.GetParError(1)
        print("Is = %.3g \pm %.3g" %self.v0)
        print("n*Vt = %.3f \pm %.3f" %self.tau)

a = DiodeCurrent(name)
canv = TCanvas('car','car')
canv.SetFillColor(10)
a.graph.SetTitle()
a.fit_graph()
a.graph.Draw('AEP')
a.graph.SetTitle()
#I0 = a.v0[0]
#const =a.tau[0]
#f2 = TF1('inverse','[0]*(TMath::Log(x/[1])+1)')
#f2.SetParameters(const, I0)
#print f2.Eval(0.5)
raw_input('Press ENTER to continue...')
