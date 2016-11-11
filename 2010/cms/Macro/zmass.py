#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TTree, TH1F, TFile
from string import Template
import sys
import os

try:
    input_root_file = sys.argv[1]
except IndexError as e:
    print(e, "Usage: python {0} input.root".format(sys.argv[0]), sep="\n")
    raise SystemExit

if not os.path.exists(input_root_file):
    raise OSError, "File {0} not found!".format(input_root_file)

root_file = TFile(input_root_file)
tree_name = "Summary/tree"
tree = root_file.Get(tree_name)
if not tree:
    raise KeyError, "Tree {0} not found!".format(tree_name)

selection_template = Template("selectionWord.TestBitNumber($n)")
selection_list = range(1)
full_selection = [selection_template.substitute(n=i) for i in selection_list]
full_selection = " && ".join(full_selection)
print(full_selection)

tree.Draw("ZMassEG", full_selection)
raw_input()
