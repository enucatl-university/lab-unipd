#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

from style import style
import sys
from ROOT import TGraphErrors, TCanvas
style.cd() 

class CalibrazionePotenziometro:

    def __init__(self, tabella):
        self.file_tabella = tabella
        self.gr = TGraphErrors(tabella)
        self.gr.SetTitle("calibrazione potenziometro;potenziometro;R [#Omega]")
        self.result = self.gr.Fit("pol1", "SQ")

    def disegna_grafico(self):
        self.can = TCanvas("can", "can")
        self.gr.Draw("AP")
        can.SaveAs("relazione/img/{0}.eps".format(self.file_tabella)) 

    def salva_calibrazione(self):
        with open("fit.{0}".format(self.file_tabella), "w") as out_file:
            a = self.result.Parameter(1)
            sigma_a = self.result.ParError(1)
            b = self.result.Parameter(0)
            sigma_b = self.result.ParError(1)
            line = [a, sigma_a, b, sigma_b]
            line = [str(x) for x in line]
            line = " ".join(line)
            out_file.write(line)

    def stampa_tabella(self):
        print("\\begin{tabular}{r@{ $\\pm$ }lr@{ $\\pm$ }l}")
        print("\\multicolumn{2}{c}{$R [\\unit[]{\\ohm}]$} &\\multicolumn{2}{c}{potenziometro} \\\\ ")
        print("\\hline")
        with open(name_in) as file:
            for line in file:
                if "//" in line:
                    continue
                line = [float(x) for x in line.split()]
                print("{0[1]:.2f} & {0[3]:.2f} & {0[0]:.2f} & {0[2]:.2f} \\\\ ".format(line))
        print("\\end{tabular}")
        
if __name__ == "__main__":
    tabella = sys.argv[1]
    c = CalibrazionePotenziometro(tabella)
    c.disegna_grafico()
    c.salva_calibrazione()
    c.stampa_tabella()

