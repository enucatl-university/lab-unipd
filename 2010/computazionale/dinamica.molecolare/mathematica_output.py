#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function

with open("molecular.out") as in_file:
    print("{", end="")
    string = [line.split()[1] for line in in_file]
    print(",".join(string), end="")
    print("}")
