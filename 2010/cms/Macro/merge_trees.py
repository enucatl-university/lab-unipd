#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TList, TTree, TFile
import sys
import os

home = os.environ["HOME"]
file_list = [
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_0.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_1.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_10.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_11.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_12.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_13.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_14.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_15.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_16.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_17.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_18.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_19.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_2.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_20.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_21.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_22.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_23.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_24.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_25.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_3.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_4.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_5.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_6.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_7.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_8.root".format(home),
"{0}/scratch0/ntuple/background_analysis/PFAnalysis_QCDEM3080_9.root".format(home),
        ]

tree_list = TList()
tree_name = "Summary/tree"
output_file_name = "~/scratch0/PFAnalysis_QCDEM3080_0.root"

files = [TFile(file_name) for file_name in file_list if os.path.exists(file_name)]
print("{0} files found.".format(len(files)))
trees = [file.Get(tree_name) for file in files]
for tree in trees:
    if tree:
        tree_list.Add(tree)

merged_tree = TTree.MergeTrees(tree_list)
output_file = TFile(output_file_name, "recreate")
merged_tree.Write()
output_file.Close()

