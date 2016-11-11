#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from HistogramHandler import *
from ROOT import TCanvas, TLegend
import Selections

#DATA comparison
full_names = [
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_0.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_1.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_2.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_3.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_4.root",
"/afs/cern.ch/user/a/abis/scratch0/ntuple/data_myskim/PFAnalysis_NEW_MYSKIM_Data_5.root",
#"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_0.root",
#"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_1.root",
#"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_2.root",
#"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_3.root",
#"/afs/cern.ch/user/a/abis/scratch0/ntuple/fullsim_background/PFAnalysis_NEW_QCDEM3080_4.root",
        ]

fast_names = [
"/afs/cern.ch/user/a/abis/scratch0/ntuple/fastsim_background/PFAnalysis_NEW_QCDEM3080_0.root",
        ]

selections = {
        "empty_selection": Selections.empty_selection,
        "pt15ele1": Selections.pt15ele1,
        "id_oppcharge_selection": Selections.id_oppcharge_selection,
        #"only_isolation": Selections.only_isolation,
        "full_selection": Selections.full_selection,
        }

variables = ["ZMass", "ele1NormalizedChi2", "ele1Pt", "ele1Eta", "ele1Phi", "ele1FbremMode", "ele1Calo", "ele1ID", "ele1IsoRel", "ele1ID"]

for sel_name, selection in selections.iteritems():
    for variable in variables:
        full_handles = [HistogramHandler(name, variable, "_", selection) for name in full_names]
        fast_handles = [HistogramHandler(name, variable, "_", selection) for name in fast_names]

        full_handle = reduce(operator.add,
                full_handles)
        fast_handle = reduce(operator.add,
                fast_handles)

        full_scale = full_handle.mass_hist.Integral()
        fast_scale = fast_handle.mass_hist.Integral()
        if not (full_scale and fast_scale): continue
        full_handle.mass_hist.Scale(fast_scale/ full_scale)
        #fast_handle.mass_hist.Scale(full_scale / fast_scale)

        full_handle.mass_hist.SetFillColor(0)
        fast_handle.mass_hist.SetMarkerStyle(21)
        fast_handle.mass_hist.SetMarkerColor(2)
        full_handle.mass_hist.SetFillColor(0)
        fast_handle.mass_hist.SetFillColor(0)
        full_handle.mass_hist.SetLineColor(1)
        fast_handle.mass_hist.SetLineColor(2)
        full_handle.mass_hist.Sumw2()
        fast_handle.mass_hist.Sumw2()

        comparison_canvas = TCanvas("comp_canvas", "comp_canvas", 1024, 768)
        max1 = full_handle.mass_hist.GetMaximum()
        max2 = fast_handle.mass_hist.GetMaximum()
        maximum = max(max1, max2)
        full_handle.mass_hist.SetMaximum(1.2*maximum)
        full_handle.mass_hist.SetMinimum(0)
        full_handle.draw("hist")
        fast_handle.draw("esame")
        legend = TLegend(0.7331269, 0.6926573, 0.9622291, 0.9671329)
        legend.AddEntry(full_handle.mass_hist, "Data #int L dt = 166#[]{nb^{-1}}", "F")
        legend.AddEntry(fast_handle.mass_hist, "FastSim", "F")
        legend.SetFillColor(0)
        legend.Draw()
        comparison_canvas.SaveAs("plots_fast_vs_data/{0}_QCD3080_full_vs_fast_{1}.eps".format(variable, sel_name))
