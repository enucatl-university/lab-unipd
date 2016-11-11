#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
import os
from calibrazione.potenziometro_temperatura import PotenziometroTemperatura
from calibrazione.potenziometro_resistenza import PotenziometroResistenza
from ROOT import TCanvas, TGraphErrors
from style import style

cartella_calibrazione = "../calibrazione"
calibrazione_potenziometro_T = os.path.join(cartella_calibrazione,
"fit.calibrazione.potenziometro1.oscilloscopio")
calibrazione_potenziometro_D = os.path.join(cartella_calibrazione,
"fit.calibrazione.potenziometro2")
tabella_temperatura = os.path.join(cartella_calibrazione, "tabellaPT")

alpha = 17e-6
T0 = 293.15

class LettoreFileDebye(object):
    """Legge il file con Volt, corrente, Rt, Rd e restituisce temperature,
    resistenze ed errori per l'analisi della temperatura di Debye"""

    def __init__(self, file_name):
        super(LettoreFileDebye, self).__init__()
        self.T_i = []
        self.sigma_Ti = []
        self.R_i = []
        self.sigma_i = []
        with open(file_name) as input_file:
            for line in input_file:
                if "//" in line:
                    continue
                V, I, p_t, p_d = [float(x) for x in line.split()]
                PT = PotenziometroTemperatura(calibrazione_potenziometro_T,
                        tabella_temperatura, p_t)
                PD = PotenziometroResistenza(calibrazione_potenziometro_D, p_d)
                self.T_i.append(PT.T)
                self.sigma_Ti.append(PT.sigma_T)
                self.R_i.append(PD.R)
                self.sigma_i.append(PD.sigma_R)

    def draw(self, output_file):
        self.output_filename = output_file
        with open(output_file, "w") as out_file:
            for T, sigma_T, R, sigma_R in zip(
                    self.T_i,
                    self.sigma_Ti,
                    self.R_i,
                    self.sigma_i):
                out_line = [T, R, sigma_T, sigma_R, "\n"]
                out_line = [str(x) for x in out_line]
                out_line = " ".join(out_line)
                out_file.write(out_line)
        style.cd()
        self.canvas = TCanvas("temperatura_resistenza_can",
                "temperatura_resistenza_can")
        self.graph = TGraphErrors(output_file)
        self.graph.SetTitle("Resistenza del campione;T#[]{K};R#[]{#Omega}")
        self.graph.Draw("ap")

    def tabella_latex(self, output_file):
        with open(output_file, "w") as out_file:
            out_file.write("\\begin{tabular}{r@{ $\\pm$ }lr@{ $\\pm$ }l|cc}\n")
            out_file.write("\\multicolumn{2}{c}{$\\unit[T]{[K]}$} &\\multicolumn{2}{c}{$\\unit[R]{[\\ohm]}$} & $\\sigma_R/ R$ [\%] &  $\\Delta_D / D$ [\%] \\\\\n ")
            out_file.write("\\hline\n")
            for T, sigma_T, R, sigma_R in zip(
                    self.T_i,
                    self.sigma_Ti,
                    self.R_i,
                    self.sigma_i):
                line = [T, sigma_T, R, sigma_R, sigma_R/R*1e2, alpha*(T0-T)*1e2]
                out_file.write("{0[0]:.1f} & {0[1]:.1f} & {0[2]:.2f} & {0[3]:.2f} & {0[4]:.2f} & {0[5]:.2f} \\\\ \n ".format(line))
            out_file.write("\\end{tabular}")

    def save_as(self, name):
        self.canvas.SaveAs(name)

if __name__ == "__main__":
    l = LettoreFileDebye("../dati/debye")
    l.draw("temperatura_resistenza.out")
    l.save_as("../relazione/img/temperatura_resistenza_debye.eps")
    l.tabella_latex("../relazione/tab/temperatura_resistenza_debye.tex")
    input()
