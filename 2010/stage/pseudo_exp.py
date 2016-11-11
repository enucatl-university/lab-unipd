#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TTree, TH1D, TCut, TFile, TMath, TCanvas, TGraphErrors
from ROOT import gStyle
from itertools import izip
import random
import array
from norm_inv import kolm_to_sigma

def sum_cuts(cuts):
    try:
        try: cuts + ''
        except TypeError: pass
        else: raise TypeError
        total_cut = cuts[0]
        for cut in cuts:
            total_cut += (' && ' + cut)
    except TypeError:
        total_cut = cuts
    return total_cut

class PseudoExperiment(object):

    def __init__(self, tree, variable, cuts1, cuts2, n_getrand=10000, hist_stats=(400, 0, 2)):
        """projects tree variable on two histograms based on cut lists 1 and
        2. Then runs a pseudo experiment and a KolmogorovTest"""
        self.variable = variable
        self.n_getrand = n_getrand
        self.cuts = [sum_cuts(cut) for cut in cuts1, cuts2]
        self.hist_stats = hist_stats
        self.set_histograms()
        self.feed_children()
        self.kolm_sigma()

    def add_cut(self, cut):
        """adds string to both cuts, rebuild histograms"""
        self.cuts = [cut_already + " && " + cut
                for cut_already in self.cuts]
        self.set_histograms()

    def set_histograms(self):
        pnames = [str(random.randint(0, 1000000)) for _ in self.cuts]
        cnames = ['c' + name for name in pnames]
        self.parents = [TH1D(name, name, *self.hist_stats) for name in pnames]
        self.children = [TH1D(name, name, *self.hist_stats) for name in cnames]

        self.n_entries = [tree.Project(name, self.variable, cut)
                for name, cut in zip(pnames, self.cuts)]
        self.fractions = [num / sum(self.n_entries) for num in self.n_entries]
        self.pnames = pnames
        self.cnames = cnames

    def feed_children(self):
        for parent, child, fraction in zip(self.parents, self.children,
                self.fractions):
            #trying to speed up code:
            child_fill = child.Fill
            parent_get_random = parent.GetRandom
            for i in xrange(int(fraction * self.n_getrand)):
                child_fill(parent_get_random())
            del child_fill
            del parent_get_random

    def kolm_sigma(self):
        h1, h2 = self.children
        return kolm_to_sigma(h1.KolmogorovTest(h2))

    def next(self):
        [h.Reset() for h in self.children]
        self.feed_children()
        return self.kolm_sigma()

    def __iter__(self):
        return self

class PseudoScientist:
    """Repeats pseudo experiment, adding new cuts."""
    """next() returns a mean, rms/sqrt(n) tuple"""
    def __init__(self, pseudo_experiment, incremental_cut_on, start, end,
            step, experiments_per_step=10000):
        self.pseudo_experiment = pseudo_experiment
        self.incremental_cut_on = incremental_cut_on
        self.start = start
        self.current_cut = start
        self.end = end
        self.step = step
        self.experiments_per_step = experiments_per_step
        
    def next(self):
        if self.start <= self.end:
            self.current_cut += self.step
            cut = self.incremental_cut_on + " > " + str(self.current_cut)
            if self.current_cut > self.end:
                raise StopIteration
        if self.start > self.end:
            self.current_cut -= self.step
            cut = self.incremental_cut_on + " < " + str(self.current_cut)
            if self.current_cut < self.end:
                raise StopIteration
        exp = self.pseudo_experiment
        exp.add_cut(str(cut))
        mean_arr = array.array('d')
        for i, prob in izip(xrange(self.experiments_per_step), exp):
            mean_arr.append(prob)
        n = len(mean_arr)
        mean_prob = TMath.Mean(n, mean_arr)
        err_prob = TMath.RMS(n, mean_arr)
        #err_prob /= (n - 1)
        return self.current_cut, mean_prob, err_prob

    def __iter__(self):
        return self

class PainterScientist:

    def __init__(self, sci1, sci2, title, x_title, y_title):
        self.sci1, self.sci2 = sci1, sci2
        self.can = TCanvas("graph", "graph")
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.build_graphs()

    def build_graphs(self):
        scientists = [self.sci1, self.sci2]
        names = ['tmp_global', 'tmp_inner']
        for name, scientist in zip(names, scientists):
            with open(name, 'w') as file:
                for step, n_sigma, err in scientist:
                    list = [step, n_sigma, 0, err]
                    list = [str(x) for x in list]
                    output_line = '\t'.join(list)
                    output_line += '\n'
                    file.write(output_line)

        unique_name = "can" + str(random.randint(0, 1000))
        self.can = TCanvas(unique_name, "graph")
        self.gr_global = TGraphErrors(names[0])
        self.gr_inner = TGraphErrors(names[1])
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
        
if __name__ == '__main__':
    file = TFile("muon_reco25.1.root")
    tree = file.Get("PatAnalyzerSkeleton/ass_muons")
    variable_inner = "d_lin_inner"
    variable_global = "d_lin_global"
    cuts1 = "abs(mother_pdgid) == 411"
    cuts2 = "abs(mother_pdgid) == 521"

    cutting_on = "pt"
    start = 3
    end = 10
    step = 0.1
    n_getrand = 10000
    n_experiments = 100
    title = "results of KS test as a function of minimum pt"
    x_title = """pt #[]{GeV / c}"""
    y_title = """confidence level #[]{#sigma}"""
    save_file_name = "pseudo_pt_1.eps"

    #cutting_on = "lum"
    #start = 3e-2
    #end = 0
    #step = 5e-4
    #n_getrand = 10000
    #n_experiments = 100
    #title = "results of KS test as a function of luminosity"
    #x_title = """luminosity #[]{pb^{-1}}"""
    #y_title = """confidence level #[]{#sigma}"""
    #save_file_name = "pseudo_lum_1.eps"

    exp_global = PseudoExperiment(tree, variable_global, cuts1, cuts2, n_getrand)
    exp_inner = PseudoExperiment(tree, variable_inner, cuts1, cuts2, n_getrand)
    sci_global = PseudoScientist(exp_global, cutting_on, start, end, step,
            n_experiments)
    sci_inner = PseudoScientist(exp_inner, cutting_on, start, end, step,
            n_experiments)

    painter = PainterScientist(sci_global, sci_inner, title, x_title, y_title)
    painter.save_canvas(save_file_name)

    file.Close()
    raw_input()
