#creates useful histograms for the analysis of electron tracks

from ROOT import TFile, TTree, TH1D, TCanvas, TLegend, TProfile
from histogram_parameters import *
import os
from time import gmtime, strftime

class ElectronDataset(object):
    def __init__(self, root_file_name):
        self.name = root_file_name
        self.root_file = TFile(root_file_name)
        tree = self.root_file.Get(tree_name)
        self.histograms = []
        for key, value in d.iteritems():
            if value[0] is "TH1D":
                self.histograms.append(TH1D(*value[1]))
            elif value[0] is "TProfile":
                self.histograms.append(TProfile(*value[1]))
        [tree.Project(key, formula[key], cuts[key]) for key in d.iterkeys()]
#just for debugging purposes:
        #for i, histogram in enumerate(self.histograms):
            #canvas = TCanvas("%i" %i, "%i" %i) 
            #histogram.Draw()
            #raw_input()

class DatasetComparison(object):
    def __init__(self, *root_files):
        self.datasets = [ElectronDataset(root_file_name)
                for root_file_name in root_files]
        self.normalize_histograms()
        self.set_histogram_style()

    def normalize_histograms(self):
        #normalize by integral. calculate coefficients:
        normalization = [[h.Integral() for h in dataset.histograms]
                for dataset in self.datasets]
        normalization = zip(*normalization)
        normalization = [[n[0] / elem for elem in n] for n in normalization]
        normalization = zip(*normalization)
#normalize
        [[h.Scale(factor)
            for h, factor in zip(dataset.histograms, norm)]
                for dataset, norm in zip(self.datasets, normalization)]

    def set_histogram_style(self):
        for colour, dataset in zip(colours, self.datasets):
            for h in dataset.histograms:
                h.SetLineColor(colour)

        for dataset in self.datasets:
            for h, key in zip(dataset.histograms, d.iterkeys()):
                h.GetXaxis().SetTitle(other_hist_pars[key]["xtitle"])
                h.GetYaxis().SetTitle(other_hist_pars[key]["ytitle"])

    def draw(self):
        folder = strftime("%Y_%m_%d_%H%M%S", gmtime())
        os.mkdir(folder)
        for i, key in enumerate(d.iterkeys()):
            canvas = TCanvas(key, key)
            legend = TLegend(0.8, 0.8, 1, 1)
            if other_hist_pars[key]["logy"]:
                canvas.SetLogy()
            for j, dataset in enumerate(self.datasets):
                if not j: dataset.histograms[i].Draw("e1")
                else: dataset.histograms[i].Draw("same")
                legend.AddEntry(dataset.histograms[i], dataset.name)
            legend.Draw()
            canvas.SaveAs(folder + "/" + key + ".eps")
            #raw_input()
