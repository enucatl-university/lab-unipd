#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
import subprocess
import sys

pressures = [600, 550, 500, 450, 400]
backgrounds = [60, 70, 75, 75, 80]
n = 1500

for p, b in zip(pressures, backgrounds):
    try:
        args = (p, n, b)
        retcode = subprocess.call("my_bragg dati/%i_ %i %i" %args, shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError, e:
        print("Execution failed:", retcode, file=sys.stderr)
