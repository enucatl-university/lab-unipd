#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TCanvas, TTree, TH1D, TH1I, TFile, TLegend, gStyle, TF1, TGraphErrors

gStyle.SetOptStat(0)
def get_mean(hist):
    mean = hist.GetMean()
    mean_err = hist.GetMeanError()
    return mean, mean_err

bragg_mean_energies = [5.14837, 5.47831, 5.79504]
pressures = [600, 550, 500, 450]

class Bragg(object):
    """make hist of bragg maximum as a function of alpha particle energy.
    Integral limits to be found in file
    P_limits.dat,
    ntuple in
    P_.root"""

    def __init__(self, pressure):
        self.name = str(pressure)
        root_file_name = "dati/" + self.name + "_matteo.root"
        self.spectral_lines = self.read_energy_limits()
        self.root_file = TFile(root_file_name)
        self.ntuple = self.root_file.Get("ntuple")

    def read_energy_limits(self):
        #read file p_limits.dat to read integral limits on spectral lines
        limits_file_name = self.name + "_limits.dat"
        with open(limits_file_name) as file:
            #read limits from file
            spectral_lines = [[float(x) for x in line.split()]
                    for line in file
                    if '#' not in line]
            self.limits_tuple = [tuple(x) for x in spectral_lines]
            spectral_lines = ["integr>%i && integr<%i" %line
                    for line in self.limits_tuple]
            return spectral_lines

    def draw_energy(self):
        #draw histogram with integrals (energy)
        #integr_output = TFile(self.name + "_integr.root", "recreate")
        #integr_output.cd()
        self.integral_canvas = TCanvas("integral_canvas" + self.name,
                "integral")
        self.integral_hist = TH1I("integral_hist" + self.name,
                "Integral " + self.name,
                150, 5000, 7000) 
        self.ntuple.Draw("integr>>integral_hist" + self.name)
        #self.integral_hist.Write()
        self.integral_hist.SaveAs(self.name + "_integr.root")
        #integr_output.Close()

    def draw_range(self):
        #draw range(delta_t) histograms
        self.range_can = TCanvas("range_" + self.name,
                "range")
        self.integral_hist = TH1D("delta_t" + self.name, "#Delta T", 40, 10, 50) 
        self.ntuple.Draw("deltaT>>delta_t" + self.name)

    def draw_bragg_max(self):
        #three histograms for bragg maxima
        self.bragg_maxima_can = TCanvas("max_can_" + self.name, "Bragg maxima")
        self.bragg_histograms = [TH1D(self.name + "line%i" %i, "Bragg max", 100, 130, 230)
                for i in range(3)]

        for i, line in enumerate(self.spectral_lines):
            self.ntuple.Draw("maxC>>%sline%i" %(self.name, i), line, "goff")

        for i, hist in enumerate(self.bragg_histograms):
            hist.SetLineStyle(i + 1)
            if i: hist.Draw("same")
            else:
                hist.Draw()
                hist.GetYaxis().SetRangeUser(0,75)

        leg_hist = TLegend(0.75,0.75,0.98,0.98)
        leg_hist.SetHeader("Bragg maxima")
        [leg_hist.AddEntry(hist,"alpha energy %i" %(i+1),"l") for i, hist in
                enumerate(self.bragg_histograms)]
        leg_hist.Draw();

    def draw_mean_energies(self):
        #draw TGraphErrors with mean energies (integral) vs alpha energies (MeV)
        file_name = self.name + "_calib.dat"
        self.mean_en_can = TCanvas(file_name, file_name)
        self.mean_en_graph = TGraphErrors(file_name)
        self.mean_en_graph.GetYaxis().SetRangeUser(5700, 6700)
        self.mean_en_graph.SetMarkerStyle(8)
        self.mean_en_graph.Draw("AP")

    def bragg_max_means(self):
        #calculate means of bragg maximums
        return [get_mean(hist) for hist in self.bragg_histograms]

    def bragg_max_gaussian_fit(self):
        #make a gaussian fit instead of mean
        means = []
        for hist in self.bragg_histograms:
            f = TF1("gaussian", "gaus")
            fit = hist.Fit("gaussian", "S")
            mean, mean_err = f.GetParameter(1), f.GetParError(1)
            means.append((mean,mean_err))
        #fit_results = [hist.Fit("gaus", "SQ") for hist in self.bragg_histograms]
        #return [(fit.Value(2), fit.Error(2)) for fit in fit_results]
        return means

    def bragg_max_kolmogorov_matrix(self):
        return [[h1.KolmogorovTest(h2)
            for h1 in self.bragg_histograms]
            for h2 in self.bragg_histograms]

    def mean_energies(self):
        #mean integral of the three spectral lines 
        output_name = self.name + "_calib.dat"
        with open(output_name, "w") as file:
            hist = self.integral_hist
            means = []
            for en, tuple in zip(bragg_mean_energies, self.limits_tuple):
                min, max = [int(x) for x in tuple]
                hist.GetXaxis().SetRangeUser(min, max)
                mean = hist.GetMean()
                mean_err = hist.GetMeanError()
                output_line = "%f %f 0 %f \n" %(en, mean, mean_err)
                file.write(output_line)
                means.append((mean, mean_err))
            hist.GetXaxis().SetRange()
        return means

    def mean_range(self):
        range_hists = [TH1D(self.name + "range_line%i" %i, "Range", 60, 5.5,
            70.5)
                for i in range(3)]

        for i, line in enumerate(self.spectral_lines):
            self.ntuple.Draw("deltaT>>%srange_line%i" %(self.name, i), line, "goff")

        return [get_mean(hist) for hist in range_hists]

if __name__ == "__main__":
    bragg = [Bragg(p) for p in pressures]
    [b.draw_energy() for b in bragg]
    [b.draw_bragg_max() for b in bragg]
    bragg_means = [b.bragg_max_means() for b in bragg] 
    energy_means = [b.mean_energies() for b in bragg]
    range_means = [b.mean_range() for b in bragg]
    [b.draw_mean_energies() for b in bragg]
#gaussian = [b.gaussian_fit() for b in bragg] 
    #kolm_probabilities = [b.kolmogorov_matrix() for b in bragg]
#for matrix in kolm_probabilities:
#    for line in matrix:
#        print("%.3g %.3g %.3g" %tuple(line))
#    print()

    print("massimi di Bragg:")
    for line in bragg_means:
        for mean in line:
            print("%.2f \pm %.2f" %mean, end="    ")
        print()
    print("\n")

    print("range (tempo):")
    for line in range_means:
        for mean in line:
            print("%.3f \pm %.3f" %mean, end="    ")
        print()
    print("\n")

    print("Bragg-Kleman: R prop. 1/P")
    for line, p in zip(range_means, pressures):
        for mean in line:
            print("%f %f 0 %f" %(1/p, mean[0], mean[1]), end="    ")
        print()
    print("\n")


#print("media delle energie:")
#for b, line in zip(bragg, energy_means):
#    with open(b.name + "_calib.dat", "w") as file:
#        for energy, mean in zip(bragg_mean_energies, line):
#            print("%.3f \pm %.3f" %mean, end="    ")
#            output_line = "%f %f 0 %f \n" %(energy, mean[0], mean[1])
#            file.write(output_line)
#        print()
#print("\n")
        
#for line in gaussian:
#    for mean in line:
#        print("%.2f \pm %.2f" %mean, end="    ")
#    print()

    input()
