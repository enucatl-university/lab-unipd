#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from FullHistogramHandler import BackgroundNoise, DataComparison
from FullHistogramParameters import lumi, variable_dictionary
import Selections

background_files = [
        "/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_BCtoE2030_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_BCtoE3080_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_BCtoE80170_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet015_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet120170_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet1520_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet170300_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet2030_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet300500_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet3050_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet5080_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_PhotonJet80120_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM2030_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_Zee_0.root",
[
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_1.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_2.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_3.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_4.root",
], 
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM80170_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_TTbar_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_Wenu_0.root",
]

data_files = [
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


selections = {
        "empty_selection": Selections.empty_selection,
        #"pt_eta_selection": Selections.pt_eta_selection,
        #"id_oppcharge_selection": Selections.id_oppcharge_selection,
        #"only_isolation": Selections.only_isolation,
        #"full_selection": Selections.full_selection,
        }

for variable in ["ZMass"]:
#for variable in ["ZMass", "ele1NormalizedChi2", "ele1Pt", "ele1Eta", "ele1Phi", "ele1FbremMode", "ele1Calo", "ele1ID", "ele1IsoRel", "ele1ID"]:
    for sel in selections:
        print(sel)
        c = DataComparison(background_files, data_files, variable, "_", selections[sel], lumi)
        c.draw()
        c.print_table()
        c.save("plots_fullsim/{0}_withdata_{1}.png".format(variable, sel))
