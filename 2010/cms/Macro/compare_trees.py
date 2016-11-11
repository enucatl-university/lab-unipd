#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TTree, TFile
import sys
import os
from string import Template

if len(sys.argv) < 3:
    raise IndexError, "Usage: python compare_trees.py file1.root file2.root"

file_names = sys.argv[1:]

if False in [os.path.exists(file_name) for file_name in file_names]:
    raise OSError, "File not found!"

tree_name = "ZeeAnalyzer/tree"
root_files = [TFile(file_name) for file_name in file_names]
trees = [file.Get(tree_name) for file in root_files] 

full_selection = "triggerMatched && isPtSelected && isEtaSelected && isIsolated && isIdentified && isOppositeCharge"
print(full_selection)

trees = [tree.CopyTree(full_selection) for tree in trees]
data = [set([(event.run, event.event, event.lumisection) for event in tree]) for tree in trees]

print(len(data[0]), len(data[1]))

intersection = data[0].intersection(*data[1:])
symmetric_difference = data[0].symmetric_difference(data[1])

print("intersection ({0} elements)".format(len(intersection)))
for element in sorted(intersection, cmp=lambda x,y: cmp(x[0], y[0])):
    print(element)

print()

print("symmetric_difference ({0} elements)".format(len(symmetric_difference)))
for element in sorted(symmetric_difference, cmp=lambda x,y: cmp(x[0], y[0])):
    print(element)

print()

just_in_first = data[0] - data[1]
just_in_second = data[1] - data[0]
print("just in first set ({0} elements)".format(len(just_in_first)))
for element in sorted(just_in_first, cmp=lambda x,y: cmp(x[0], y[0])):
    print(element)

print()

print("just in second set ({0} elements)".format(len(just_in_second)))
for element in sorted(just_in_second, cmp=lambda x,y: cmp(x[0], y[0])):
    print(element)

print()

