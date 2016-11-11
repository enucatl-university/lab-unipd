#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TMath, TH1D, TH2D, TTree, TCanvas, TFile, TGraph, gStyle
from ROOT import TLegend
import random
import norm_inv

def flatten(nested):
    try:
        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested



class KolmogorovDistribution:
    """class to analyze the B/D tree and return the Kolmogorov
    Probability distribution as a function of a cut in one of the tree
    branches"""

    def __init__(self, trees, analyzing_branch, cutting_on, start, end, step,
            hist_stats, other_cuts):
        """trees are the two TTrees with all data. It's going to be a
        dictionary.
        analyzing_branch = name of the branch we are going to compare
        (KTest)
        cutting_on, start, end, step = the cut we are going to study, e.g.
        the Kolmogorov distribution as a function of the cut on pt, with pt
        ranging from start to end in steps of length step
        hist_stats is the range of analyzing_branch we're going to use for
        comparison. (hist_bins, hist_start, hist_end) as a tuple, to be
        passed to the TH1D constructor."""
        self.trees = trees
        self.branch = analyzing_branch
        self.cutting_on = cutting_on
        self.start = start
        self.current_cut = start
        self.end = end
        self.step = step
        self.hist_stats = hist_stats
        try:
            other_cuts + ['is', 'list']
            self.other_cuts = ' && '.join(other_cuts)
        except TypeError:
            self.other_cuts = other_cuts
        self.particle_pdgid = {"B":" && abs(mother_pdgid) == 521",
                "D": " && abs(mother_pdgid) == 411"}

        """Now building histograms"""
        unique_name = str(random.randint(0, 1000))
        self.histograms = dict([(tree + unique_name, TH1D(tree + unique_name, tree, *hist_stats)) for tree in trees])

    def next(self):
        if self.start <= self.end:
            self.current_cut += self.step
            cut = self.cutting_on + " > " + str(self.current_cut)
            if self.current_cut > self.end:
                raise StopIteration
        if self.start > self.end:
            self.current_cut -= self.step
            cut = self.cutting_on + " < " + str(self.current_cut)
            if self.current_cut < self.end:
                raise StopIteration
        cut = cut + ' && ' + self.other_cuts
        for tree, hist_name in zip(self.trees, self.histograms):
            self.trees[tree].Project(hist_name, self.branch, cut +
                    self.particle_pdgid[tree])
        h1, h2 = [self.histograms[name] for name in self.histograms]
        kolm_prob = h1.KolmogorovTest(h2, "")
#convert to n of standard deviations with inverse error function
        kolm_prob = norm_inv.kolm_to_sigma(kolm_prob)
        return self.current_cut, kolm_prob

    def __iter__(self):
        return self

class KolmogorovResults:
    """compare d_global with d_inner"""
    def __init__(self, trees, cutting_on, start, end, step,
            hist_stats, other_cuts, title, x_title, y_title):
        self.kd_global = KolmogorovDistribution(trees, "d_lin_global", cutting_on, start, end, step,
                hist_stats, other_cuts)
        self.kd_inner = KolmogorovDistribution(trees, "d_lin_inner", cutting_on, start, end, step,
                hist_stats, other_cuts)
        self.can = TCanvas("graph", "graph")
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.build_graphs()

    def build_graphs(self):
        kds = [self.kd_global, self.kd_inner]
        names = ['tmp_global', 'tmp_inner']
        for name, kd in zip(names, kds):
            with open(name, 'w') as file:
                for step, n_sigma in kd:
                    output_line = '\t'.join([str(x) for x in [step, n_sigma]])
                    output_line += '\n'
                    file.write(output_line)

        unique_name = "can" + str(random.randint(0, 1000))
        self.can = TCanvas(unique_name, "graph")
        self.gr_global = TGraph(names[0])
        self.gr_inner = TGraph(names[1])
        titles = ("global track", "inner track")
        self.set_graph_title(*titles)
        self.set_graph_style()

    def SetLogy(self):
        self.can.SetLogy()

    def set_graph_style(self):
        self.can.SetFillColor(10)
        self.gr_global.Draw("AP")
        self.gr_inner.Draw("P")
        legend = self.can.BuildLegend(0.7, 0.8, 0.9, 0.9)
        legend.SetFillColor(10)
        legend.Paint()
        self.gr_global.SetMarkerStyle(20)
        self.gr_inner.SetMarkerStyle(22)
        self.gr_inner.SetMarkerColor(2)
        self.gr_global.SetMarkerColor(4)

        size = 0.04
        self.gr_global.SetTitle(self.title)
        gStyle.SetTitleFillColor(0)
        self.gr_global.GetXaxis().SetTitle(self.x_title)
        self.gr_global.GetYaxis().SetTitle(self.y_title)
        self.gr_global.GetXaxis().SetDecimals()
        self.gr_global.GetYaxis().SetDecimals()
        self.gr_global.GetXaxis().SetTitleSize(size)
        self.gr_global.GetYaxis().SetTitleSize(size)
        self.gr_global.GetYaxis().SetTitleOffset(1.2)
        self.gr_global.GetXaxis().SetLabelSize(size)
        self.gr_global.GetYaxis().SetLabelSize(size)

    def set_graph_title(self, title_global, title_inner):
        self.gr_global.SetTitle(title_global)
        self.gr_inner.SetTitle(title_inner)

    def save_canvas(self, file_name):
        self.can.SaveAs(file_name)

class HowManyEvents:

    def __init__(self, trees, cutting_on, start, end, step,
            other_cuts, title, x_title, y_title):
        self.trees = trees
        self.cutting_on = cutting_on
        self.start = start
        self.current_cut = start
        self.end = end
        self.step = step
        try:
            other_cuts + ['is', 'list']
            self.other_cuts = ' && '.join(other_cuts)
        except TypeError:
            self.other_cuts = other_cuts

    def next(self):
        if self.start <= self.end:
            self.current_cut += self.step
            cut = self.cutting_on + " > " + str(self.current_cut)
            if self.current_cut > self.end:
                raise StopIteration
        if self.start > self.end:
            self.current_cut -= self.step
            cut = self.cutting_on + " < " + str(self.current_cut)
            if self.current_cut < self.end:
                raise StopIteration
        cut = cut + ' && ' + self.other_cuts
        n_events = [self.trees[tree].GetEntries(cut) for tree in self.trees]
        return list(flatten((self.current_cut, n_events)))

    def __iter__(self):
        return self

class HowManyGraph:
    def __init__(self, trees, cutting_on, start, end, step,
            other_cuts, title, x_title, y_title):
        self.names = [name for name in trees]
        files = [open(name, 'w') for name in self.names]
        for cut, n1, n2 in HowManyEvents(trees, cutting_on, start, end, step,
                other_cuts, title, x_title, y_title):
            for n, file in zip((n1, n2), files):
                string = str(cut) + '\t\t' + str(n) + '\n'
                file.write(string)
        for file in files:
            file.close()
        self.can = TCanvas("graph", "graph")
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.gr_0 = TGraph(self.names[0])
        self.gr_1 = TGraph(self.names[1])
        self.set_graph_style()

    def set_graph_style(self):
        self.can.SetFillColor(10)
        self.gr_0.Draw("AP")
        self.gr_1.Draw("P")
        legend = self.can.BuildLegend(0.7, 0.8, 0.9, 0.9)
        legend.SetFillColor(10)
        legend.Paint()
        self.gr_0.SetMarkerStyle(21)
        self.gr_1.SetMarkerStyle(23)
        self.gr_1.SetMarkerColor(3)
        self.gr_0.SetMarkerColor(9)
        self.set_graph_title(*self.names)

        size = 0.04
        self.gr_0.SetTitle(self.title)
        gStyle.SetTitleFillColor(0)
        self.gr_0.GetXaxis().SetTitle(self.x_title)
        self.gr_0.GetYaxis().SetTitle(self.y_title)
        self.gr_0.GetXaxis().SetDecimals()
        self.gr_0.GetYaxis().SetDecimals()
        self.gr_0.GetXaxis().SetTitleSize(size)
        self.gr_0.GetYaxis().SetTitleSize(size)
        self.gr_0.GetYaxis().SetTitleOffset(1.2)
        self.gr_0.GetXaxis().SetLabelSize(size)
        self.gr_0.GetYaxis().SetLabelSize(size)

    def set_graph_title(self, title_0, title_1):
        self.gr_0.SetTitle(title_0)
        self.gr_1.SetTitle(title_1)

    def SetLogy(self):
        self.can.SetLogy()

    def save_canvas(self, file_name):
        self.can.SaveAs(file_name)
