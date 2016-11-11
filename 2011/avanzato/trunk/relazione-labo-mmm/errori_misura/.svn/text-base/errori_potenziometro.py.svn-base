#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from math import sqrt
import sys

nome_file = sys.argv[1]
with open(nome_file) as file:
    for line in file:
        if "//" in line:
            output_line = line
        else:
            line = [float(x) for x in line.split()]
            err_scala = line[1]*0.002
            err_digit = 0.2
            err = sqrt((err_digit**2 + err_scala**2)/3)
            output_line = [line[0], line[1], 0.01, err]
            output_line = [str(x) for x in output_line]
            output_line = " ".join(output_line)
        print(output_line)
