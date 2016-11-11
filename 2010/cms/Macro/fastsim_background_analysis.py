#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from HistogramHandler import BackgroundNoise, DataComparison
from HistogramParameters import lumi, variable_dictionary
import Selections

background_files = [
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_BCtoE2030_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_BCtoE3080_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_BCtoE80170_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_QCDEM2030_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_QCDEM3080_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_QCDEM80170_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/skimmed_Zee/PFAnalysis_NEW_Zee_0.root",
        ]

data_files = [
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_1.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_2.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_3.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_4.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_5.root",
        ]

selections = {
        #"empty_selection": Selections.empty_selection,
        #"pt_eta_selection": Selections.pt_eta_selection,
        #"id_oppcharge_selection": Selections.id_oppcharge_selection,
        #"only_isolation": Selections.only_isolation,
        #"full_selection": Selections.full_selection,
        #"full_selection_barrel_only": Selections.full_selection_barrel_only,
        "only_identification": Selections.only_identification,
        #"full_no_charge": Selections.full_no_charge,
        }

for variable in ["ZMass", "ele1NormalizedChi2", "ele1Pt", "ele1Eta", "ele1Phi", "ele1FbremMode", "ele1Calo", "ele1ID", "ele1IsoRel", "ele1ID"]:
#for variable in ["ZMass"]:
    for sel in selections:
        print(sel)
        c = DataComparison(background_files, data_files, variable, "_", selections[sel], lumi)
        c.draw()
        c.print_table()
        c.save("plots_my_skim/{0}_withdata_{1}.eps".format(variable, sel))
        #raw_input()
