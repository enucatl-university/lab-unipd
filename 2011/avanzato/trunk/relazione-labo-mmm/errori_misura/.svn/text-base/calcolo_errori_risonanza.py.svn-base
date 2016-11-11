#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

from math import sqrt
import sys

nome_file = sys.argv[1]
with open(nome_file) as file:
    for line in file:
        if "//" in line:
            output_line = "//frequenza (Hz) ampiezza (V) err_frequenza (Hz) err_ampiezza (V)"
        else:
            line = [float(x) for x in line.split()]
            err_scala = line[1]*0.02
            output_line = [line[0], line[1], line[2], err_scala]
            output_line = [str(x) for x in output_line]
            output_line = " ".join(output_line)
        print(output_line)
