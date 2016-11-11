#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TTree, TFile, TH1D, THStack, TLegend, TCanvas
from HistogramParameters import *
import Selections
import operator
import subprocess
import os
import sys
import style

style.ele_style.cd()

class HistogramHandler(object):
    def __init__(self, root_file_name, variable, flavour_, selection, analyzed_events=0):
        self.variable = variable
        #print(root_file_name)
        self.root_file = TFile(root_file_name)
        self.tree = self.root_file.Get(tree_name)
        if not analyzed_events:
            self.analyzed_events = self.tree.GetEntriesFast()
        else:
            self.analyzed_events = analyzed_events
        self.name = root_file_name.split("_")[-2]
        first_bin = variable_dictionary[variable]["first_bin"]
        last_bin = variable_dictionary[variable]["last_bin"]
        bin_width = variable_dictionary[variable]["bin_width"]
        n_bins = int((last_bin - first_bin) // bin_width)
        self.mass_hist = TH1D(self.name, self.name, n_bins, first_bin, last_bin)
        self.tree.Project(self.name,
                variable_dictionary[variable]["formula"].substitute(flavour=flavour_),
                selection.substitute(flavour=flavour_))
        self.set_histogram_style()
        #self.print_integral()

    def set_histogram_style(self):
        self.mass_hist.SetXTitle(variable_dictionary[self.variable]["xtitle"])
        self.mass_hist.SetYTitle(variable_dictionary[self.variable]["ytitle"])
        self.mass_hist.SetTitle(title)
        self.mass_hist.SetStats(stats)
        if self.name not in "Data":
            self.mass_hist.SetLineColor(histogram_dictionary[self.name]["LineColor"])
            self.mass_hist.SetFillColor(histogram_dictionary[self.name]["FillColor"])
        else:
            self.mass_hist.SetMarkerStyle(histogram_dictionary["Data"]["MarkerStyle"])
            self.mass_hist.SetMarkerColor(histogram_dictionary["Data"]["MarkerColor"])

    def print_integral(self, from_energy=60, to_energy=120):
        """print number of events with invariant
        mass between from and to _energy (GeV)"""
        first_bin = variable_dictionary[self.variable]["first_bin"]
        last_bin = variable_dictionary[self.variable]["last_bin"]
        bin_width = variable_dictionary[self.variable]["bin_width"]
        bin1 = int((from_energy - first_bin) / bin_width)
        bin2 = int((to_energy - first_bin) / bin_width)
        print("events with {0} < Mee < {1} GeV = ".format(from_energy, to_energy),  
                self.mass_hist.Integral(bin1, bin2),
                "----------------------")

    def print_efficiency(self):
        """print efficiency statistics"""
        passed = self.mass_hist.Integral()
        total = self.analyzed_events
        efficiency = passed / total
        print("{0:<10} & {1:>10.1f} & {2:>10.1f} & {3:>10.2g} \\\\".format(self.name, passed, total, efficiency))

    def scale(self,
            luminosity=1,
            cross_section=0,
            filter_efficiency=0,
            reco_efficiency=0
            ):
        """Luminosity unit is pb^{-1}!"""
        if not cross_section:
            cross_section = histogram_dictionary[self.name]["cross_section"]
        if not filter_efficiency:
            filter_efficiency = histogram_dictionary[self.name]["filter_efficiency"]
        if not reco_efficiency:
            reco_efficiency = histogram_dictionary[self.name]["reco_efficiency"]
        #print("#analyzed events (total) = {0}".format(analyzed_events))
        scale = (luminosity * cross_section * filter_efficiency) / (reco_efficiency * self.analyzed_events)
        self.mass_hist.Scale(scale)
        self.analyzed_events *= scale
        return scale

    def draw(self, option=""):
        self.mass_hist.Draw(option)

    def __add__(self, other):
        self.mass_hist.Add(other.mass_hist)
        self.analyzed_events += other.analyzed_events
        return self

class BackgroundNoise(object):
    def __init__(self, files, variable, flavour="PF_SYM", selection=Selections.full_selection, luminosity=1):
        self.variable = variable
        """Luminosity unit is pb^{-1}!"""
        self.stack = THStack("stack", "")
        self.file_list = files
        self.histogram_handles = []
        for file_name in self.file_list:
            if isinstance(file_name, list):
                files = [TFile(f) for f in file_name]
                trees = [f.Get(tree_name) for f in files]
                total_events = sum([tree.GetEntriesFast() for tree in trees])
                self.histogram_handles.append(
                        reduce(
                            operator.add,
                    [HistogramHandler(f, variable, flavour, selection, total_events) for f in file_name]
                    ))
            else:
                self.histogram_handles.append(HistogramHandler(file_name, variable, flavour, selection))
        self.entries = sum(
                [h.mass_hist.Integral() for h in self.histogram_handles])
        for histo_handle in self.histogram_handles:
            histo_handle.scale(luminosity)
        self.histogram_handles = self.sum_with_same_name()
        self.build_legend()
        for histo_handle in self.histogram_handles:
            self.stack.Add(histo_handle.mass_hist)

    def print_integral(self, from_energy=60, to_energy=120):
        """print number of events with invariant
        mass between from and to _energy (GeV)"""
        first_bin = variable_dictionary[self.variable]["first_bin"]
        last_bin = variable_dictionary[self.variable]["last_bin"]
        bin_width = variable_dictionary[self.variable]["bin_width"]
        bin1 = int((from_energy - first_bin) / bin_width)
        bin2 = int((to_energy - first_bin) / bin_width)
        for h in self.histogram_handles:
            print("{0} events with {1} < Mee < {2} GeV = ".format(h.name, from_energy, to_energy),  
                    h.mass_hist.Integral(bin1, bin2),
                    "----------------------")

    def print_efficiency(self):
        for h in self.histogram_handles:
            h.print_efficiency()

    def build_legend(self):
        self.legend = TLegend(0.6331269, 0.6926573, 0.9622291, 0.9671329)
        for handle in self.histogram_handles:
            self.legend.AddEntry(handle.mass_hist,
                    histogram_dictionary[handle.name]["legend"],
                    "F")
        self.legend.SetFillColor(0)

    def sum_with_same_name(self):
        qcd = reduce(operator.add,
                [h for h in self.histogram_handles if "QCD" in h.name])
        #photon_jet = reduce(operator.add,
                #[h for h in self.histogram_handles if "PhotonJet" in h.name])
        bc_to_e = reduce(operator.add,
                [h for h in self.histogram_handles if "BCtoE" in h.name])
        self.histogram_handles = [h
                for h in self.histogram_handles
                if ("BCtoE" not in h.name and "PhotonJet" not in h.name and "QCD" not in h.name)]
        self.histogram_handles.append(qcd)
        #self.histogram_handles.append(photon_jet)
        self.histogram_handles.append(bc_to_e)
        self.sort_samples()
        return self.histogram_handles

    def sort_samples(self):
        self.histogram_handles.sort(
                cmp=lambda x,y: cmp(
                    histogram_dictionary[x.name]["stack_order"],
                    histogram_dictionary[y.name]["stack_order"]))

    def set_stack(self):
        self.stack.GetXaxis().SetTitle(variable_dictionary[self.variable]["xtitle"])
        self.stack.GetYaxis().SetTitle(variable_dictionary[self.variable]["ytitle"])

    def draw(self, option=""):
        self.canvas = TCanvas("canvas", "canvas", 1024, 768)
        self.stack.Draw(option)
        self.legend.Draw()
        self.canvas.SetLogy()
        self.set_stack()
        #print("Total events selected =", self.entries)

    def save(self, name):
        try:
            self.canvas.SaveAs(name)
        except AttributeError:
            self.draw()
            self.save()

class DataComparison(object):
    def __init__(self, background_files, data_files, variable, flavour, selection, luminosity):
        self.variable = variable
        self.background = BackgroundNoise(background_files, variable, flavour, selection, luminosity)
        self.data = [HistogramHandler(file, variable, flavour, selection) for file in data_files]
        self.data = self.sum_data_samples()
        self.lumi = luminosity

    def print_table(self):
        print("{0:<10} & {1:>10} & {2:>10} & {3:>10} \\\\".format("sample", "passed", "total", "efficiency"))
        self.background.print_efficiency()
        self.data.print_efficiency()
    def sum_data_samples(self):
        data = reduce(operator.add,
                self.data)
        return data

    def draw(self):
        self.canvas = TCanvas("comparison", "comparison", 1024, 768)
        if variable_dictionary[self.variable]["logy"]:
            self.canvas.SetLogy()
        bg_max = self.background.stack.GetMaximum()
        data_max = self.data.mass_hist.GetMaximum()
        maximum = max(bg_max, data_max)
        self.background.stack.SetMaximum(1.4*maximum)
        #self.background.stack.SetMinimum(10)
        self.background.stack.Draw()
        self.data.draw("esame")
        self.build_legend()
        self.legend.Draw()

    def save(self, name):
        try:
            self.canvas.SaveAs(name)
        except AttributeError:
            self.draw()
            self.save()

    def build_legend(self):
        self.legend = TLegend(0.5331269, 0.6926573, 0.9622291, 0.9671329)
        for handle in self.background.histogram_handles:
            self.legend.AddEntry(handle.mass_hist,
                    histogram_dictionary[handle.name]["legend"],
                    "F")
        self.legend.AddEntry(self.data.mass_hist,
                histogram_dictionary["Data"]["legend"])
        self.legend.SetFillColor(10)
