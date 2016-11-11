#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

with open('diodo.out') as file:
    for line in file:
        line = line.split()
        line[1], line[2] = line[2], line[1]
        line = map(float, line)
        print ("%.2f %.2f %.2f %.2f" %tuple(line))
