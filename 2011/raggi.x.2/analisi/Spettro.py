#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1F, TCanvas, TF1, TGraph, TFile, TGraphErrors, TMath
from math import sqrt, log, pi, fabs


bins = 1024

class Spettro:
    def __init__(self, filename):
        self.filename = filename
        self.hist_filename = filename + ".dat"
        self.leggi_file()
        self.leggi_hist()

    def leggi_file(self):
        self.intervalli = []
        with  open(self.hist_filename, "w") as file_w:
            with open(self.filename) as file:
                flag = 0
                flag_roi = 0
                self.calib = 0
                self.ka, self.kb, self.la, self.lb = [-1 for _ in range(4)]
                i = 0
                for line in file:
                    if "<<END>>" in line:
                        break
                    if flag:
                        file_w.write(line)
                    if "REAL_TIME" in line:
                        self.time = float(line.split()[-1])
                    if "<<DATA>>" in line:
                        flag = 1
                        flag_roi = 0
                    if flag_roi:
                        inter = [int(x) for x in line.split()[0:2]]
                        self.intervalli.append(inter)
#                        print(inter)
                        if "ka" in line:
                            self.ka = i
                        if "kb" in line:
                            self.kb = i
                        if "la" in line:
                            self.la = i
                        if "lb" in line:
                            self.lb = i
                        i += 1
                    if "ROI" in line:
                        flag_roi = 1
                    if "200 13.95" in line:
                        self.calib = 1 #calibrazione giorno 1
                    elif "199.94 13.95" in line:
                        self.calib = 2 #calibrazione giorno 2
                        # se non trova nessuna di queste due righe è un file
                        # di calibrazione: resta calib = 0

    def leggi_hist(self):
        self.hist_name = self.filename.split(".")[0]
        self.hist = TH1F(self.hist_name, self.hist_name, bins, 0, bins)
        with open(self.hist_filename) as file:
            for i, line in enumerate(file):
                line = float(line)
                self.hist.SetBinContent(i + 1, line)

    def riscala_hist(self, time_scale):
        self.hist.Scale(time_scale / self.time)

    def riscala_hist_en(self, time_scale):
        self.hist_en.Scale(time_scale / self.time)

    def riscala_integrali(self, time_scale):
        self.integrali = [i * time_scale / self.time for i in self.integrali]
        self.integrali_err = [i * time_scale / self.time for i in self.integrali_err]

    def analisi_picchi(self):
        self.centroidi, self.sigma, self.integrali = [[] for _ in range(3)]
        gau = TF1("gau", "[0] * exp(-(x - [1])**2 / (2 *[2]**2))", 0, bins)
        for estremi in self.intervalli:
            m = estremi[0]
            M = estremi[1]
            gau.SetParameters(self.hist.GetBinContent(int((m+M)/2)), (m+M)/2, abs(M-m)/3)
            self.hist.GetYaxis().SetTitle("Numero fotoni")
            self.hist.GetXaxis().SetTitle("Canale")
            self.hist.Fit("gau", "WRQN+", "", m, M)
            self.integrali.append(gau.GetParameter(0) * sqrt(2 * pi) * gau.GetParameter(2))
            self.centroidi.append(gau.GetParameter(1))
            self.sigma.append(gau.GetParameter(2))
        self.risoluzioni = [2 * sqrt(2 * log(2)) * s / N * 100 for s,N in zip(self.sigma, self.integrali)]
        self.integrali_err = [sqrt(fabs(n)) for n in self.integrali]
        self.centroidi_err = [x/y for x,y in zip(self.sigma, self.integrali_err)]
        self.intensita_rel = [x / max(self.integrali) for x in self.integrali]

    def disegna_spettro(self):
		self.can = TCanvas(self.hist_name, self.hist_name)
		self.hist.Draw()
		#self.can.SaveAs(self.hist_name + ".eps")	

    def calibrazione(self):
        a = 0.0687553
        ea = 1.0116E-05
        b = 0.153694
        eb = 0.00539013
        ro = -0.8
        hist_en_name = self.hist_name + "_en"
        self.hist_en = TH1F(hist_en_name, hist_en_name, bins, b, a * bins + b) # istogramma in energia
        with open(self.hist_filename) as file:
            for i, line in enumerate(file):
                line = float(line)
                self.hist_en.SetBinContent(i + 1, line)
        canali = self.centroidi # temporaneo
        self.centroidi = [x * a + b for x in self.centroidi]
        self.centroidi_err = [sqrt(a**2 * ex**2 + x**2 * ea**2 + eb**2 + ro
            * x * ea * eb) for ex,x in
                zip(self.centroidi_err,canali)]
