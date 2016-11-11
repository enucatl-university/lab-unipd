#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TTree, TFile, TChain
import os
from string import Template

files_not_skimmed = [
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_1.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_2.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_3.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_4.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_5.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_6.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_7.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_8.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Data_9.root",
        ]

files_skimmed = [
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/skimmed_Zee/PFAnalysis_SKIMMED_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/skimmed_Zee/PFAnalysis_SKIMMED_1.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/skimmed_Zee/PFAnalysis_SKIMMED_2.root",
        ]

tree_name = "ZeeAnalyzer/tree"
chain_not_skimmed = TChain(tree_name)
chain_skimmed = TChain(tree_name)

[chain_not_skimmed.Add(file) for file in files_not_skimmed]
[chain_skimmed.Add(file) for file in files_skimmed]

full_selection = "triggerMatched && isPtSelected && isEtaSelected && isIsolated && isIdentified && isOppositeCharge"
print(full_selection)

trees = [tree.CopyTree(full_selection) for tree in (chain_not_skimmed, chain_skimmed)]
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

