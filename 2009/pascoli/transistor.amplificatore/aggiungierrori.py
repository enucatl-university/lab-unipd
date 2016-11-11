#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

with open('tabella2') as file:
    for line in file:
         line = line.split("&")
         a = line[3].replace('\\','')
         a = float(a)
         err = 0.06*a
         line[3] = str(a)
         line.append("%.1f" %err)
         print(*line, sep = " & ", end= '\\\\\n')
