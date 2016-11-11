#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TMath, TH1D, TH2D, TTree, TCanvas, TFile, TGraph
from kolmogorov_distribution import KolmogorovResults, HowManyGraph
import sys
import os

graphix_ext = ".eps"

try:
    root_file_name = sys.argv[1]
except IndexError:
    root_file_name = "muon_reco25.1.root"

"""We are going to analyze events with two muons, whose mother is a B or D
meson. A Kolmogorov test between the 2D histograms with the distributions in
pt of the two muons should return a very small probability.

We are interested in finding out this probability as a function of the total
number of events and the cut in transverse momentum"""

root_file = TFile(root_file_name)
dir_name = "PatAnalyzerSkeleton"
trees = {"B":"ass_muons", "D":"ass_muons"}
for tree in trees:
    trees[tree] = os.path.join(dir_name, trees[tree])
    trees[tree] = root_file.Get(trees[tree])
    print(type(trees[tree]))

#n_event
cutting_on = "lum"
start = 3e-2
end = 0
step = 5e-4
hist_stats = 400, 0, 2
other_cuts = "n_muons >= 1"
y_title = """confidence level #[]{#sigma}"""
#other_cuts = "n_muons == 2"

k_lum_1 = KolmogorovResults(trees, cutting_on, start, end, step, hist_stats,
        other_cuts,
        "results of KS test as a function of luminosity",
        """luminosity #[]{pb^{-1}}""",
        y_title)
k_lum_1.save_canvas("lum_1" + graphix_ext)
other_cuts = "n_muons == 2"
k_lum_2 = KolmogorovResults(trees, cutting_on, start, end, step, hist_stats,
        other_cuts,
        """results of KS test as a function of luminosity, only events with two muons""",
        """luminosity #[]{pb^{-1}}""",
        y_title)
k_lum_2.save_canvas("lum_2" + graphix_ext)

#pt
cutting_on = "pt"
start = 3
end = 20
step = 0.2
other_cuts = "n_muons >= 1"
k_pt_1 = KolmogorovResults(trees, cutting_on, start, end, step, hist_stats,
        other_cuts,
        "results of KS test as a function of minimum pt",
        """pt #[]{GeV / c}""",
        y_title)
k_pt_1.save_canvas("pt_1" + graphix_ext)
other_cuts = "n_muons == 2"
k_pt_2 = KolmogorovResults(trees, cutting_on, start, end, step, hist_stats,
        other_cuts,
        """results of KS test as a function of minimum pt, only events with two muons""",
        """pt #[]{GeV / c}""",
        y_title)
k_pt_2.save_canvas("pt_2" + graphix_ext)

#y_title = """entries"""
#other_cuts = "n_muons == 2"
#n_pt_2 = HowManyGraph(trees, cutting_on, start, end, step, 
#        other_cuts,
#        """number of events in KS histograms as a function of minimum pt, only events with two muons""",
#        """pt #[]{GeV / c}""",
#        y_title) 
#n_pt_2.SetLogy()
#n_pt_2.save_canvas("n_pt_2" + graphix_ext)

#other_cuts = "n_muons >= 1"
#n_pt_1 = HowManyGraph(trees, cutting_on, start, end, step, 
#        other_cuts,
#        """number of events in KS histograms as a function of minimum pt""",
#        """pt #[]{GeV / c}""",
#        y_title) 
#n_pt_1.SetLogy()
#n_pt_1.save_canvas("n_pt_1" + graphix_ext)

##n_event
#cutting_on = "lum"
#start = 3e-2
#end = 0
#step = 5e-4
#other_cuts = "n_muons == 2"
#n_lum_2 = HowManyGraph(trees, cutting_on, start, end, step, 
#        other_cuts,
#        """number of events in KS histograms as a function of luminosity, only events with two muons""",
#        """luminosity #[]{pb^{-1}}""",
#        y_title) 
#n_lum_2.SetLogy()
#n_lum_2.save_canvas("n_lum_1" + graphix_ext)

#other_cuts = "n_muons >= 1"
#n_lum_1 = HowManyGraph(trees, cutting_on, start, end, step, 
#        other_cuts,
#        """number of events in KS histograms as a function of luminosity""",
#        """luminosity #[]{pb^{-1}}""",
#        y_title) 
#n_lum_1.SetLogy()
#n_lum_1.save_canvas("n_lum_2" + graphix_ext)
raw_input()
