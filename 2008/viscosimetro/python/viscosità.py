#!/usr/bin/env python
#coding=utf-8

from __future__ import division
import math
from ROOT import TGraph, TF1

input_file = 'pallina1.dat'
output_file = 'pallina1.out'

def av(iterable):
    n = len(iterable)
    sum = 0
    for elem in iterable:
        sum += elem
    return sum/n

with open(output_file, 'w') as out:
    with open(input_file) as file:
        for line in file:
            numbers = [float(x) for x in line.split()]
            media = av(numbers[1:])
            spazio = numbers[0]
            stringa = ' '.join([str(media), str(spazio)]) + '\n'
            out.write(stringa)

graph = TGraph(output_file)
func = TF1('retta', '[0]+[1]*x', 0, 100)
func.SetParameters(0, 4)
graph.SetMarkerStyle(8)
graph.Fit('retta','QW')
graph.Draw('AEP')
speed = func.GetParameter(1)
speed_error = func.GetParError(1)
print 'velocità = %.6f \pm %.6f' %(speed, speed_error)
raw_input()
