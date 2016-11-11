#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function

import sys
import subprocess
from ROOT import TCanvas, TGraphErrors
from style import style
from errori_misura.errori_resistenze_wavetek import ErroriResistenzeWavetek
from calibrazione.potenziometro_temperatura import PotenziometroTemperatura
from calibrazione.resistenza_temperatura import ResistenzaTemperatura

input_file = sys.argv[1]
output_file = "{0}.out".format(input_file)
calibrazione_pot = "../calibrazione/fit.calibrazione.potenziometro1.oscilloscopio"
calibrazione_temp = "../calibrazione/tabellaPT"
cartella_immagini = "relazione/img/"


print("\\begin{tabular}{c|cr@{ $\\pm$ }lr@{ $\\pm$ }l}")
print("$\\unit[t]{[min]}$ & $\\unit[P]{[10^{-6}bar]}$\\multicolumn{2}{c}{$\\unit[T]{[K]}$} & \\multicolumn{2}{c}{$\\unit[T_c]{[K]}$} \\\\ ")
print("\\hline")
with open(output_file, "w") as out:
    with open(input_file) as f:
        for line in f:
            if "//" in line:
                out.write(line)
            else:
                line = [float(x) for x in line.split()]
                t, P, pot, Rc = line
#calcola errore wavetek
                calc_err_wavetek = ErroriResistenzeWavetek(Rc)
                sigma_Rc = calc_err_wavetek.err
#calcola temperatura da resistenza potenziometro
                pt = PotenziometroTemperatura(calibrazione_pot,
                        calibrazione_temp, pot)
                sigma_T = pt.sigma_T
                T = pt.T
                #calcola temperatura da resistenza di controllo
                rt = ResistenzaTemperatura(Rc, sigma_Rc, calibrazione_temp)
                sigma_Tc = rt.sigma_T
                Tc = rt.T
                line0 = [t, P, T, Tc, 1, 0, sigma_T, sigma_Tc]
                line = [str(x) for x in line0]
                line = " ".join(line)
                line0[1] = line0[1]*1e6
                out.write(line + "\n")
                print("{0[0]:.0f} & {0[1]:.1f} & {0[2]:.1f} & {0[6]:.1f} & {0[3]:.1f} & {0[7]:.1f} \\\\".format(line0))
print("\\end{tabular}")

style.cd()
canvas_tempo_pressione = TCanvas("tempo_pressione", "tempo_pressione")
grafico_tempo_pressione = TGraphErrors(output_file, "%lg %lg %*lg %*lg %lg %lg")
grafico_tempo_pressione.SetTitle("pressione; tempo [min]; pressione [mbar]")
canvas_tempo_pressione.SetLogy()
grafico_tempo_pressione.Draw("ap")
canvas_tempo_pressione.SaveAs(cartella_immagini + "tempo_pressione.eps")

canvas_tempo_T = TCanvas("tempo_T", "tempo_T")
grafico_tempo_T = TGraphErrors(output_file, "%lg %*lg %lg %*lg %lg %*lg %lg")
grafico_tempo_T.SetTitle("Termometro R_{T}; tempo [min]; T [K]")
grafico_tempo_T.GetYaxis().SetRangeUser(20, 160)
grafico_tempo_T.Draw("ap")
canvas_tempo_T.SaveAs(cartella_immagini + "tempo_T.eps")

canvas_tempo_Tc = TCanvas("tempo_Tc", "tempo_Tc")
grafico_tempo_Tc = TGraphErrors(output_file, "%lg %*lg %*lg %lg %lg %*lg %*lg %lg")
grafico_tempo_Tc.SetTitle("Termometro di controllo R_{c}; tempo [min]; T [K]")
grafico_tempo_Tc.GetYaxis().SetRangeUser(20, 160)
grafico_tempo_Tc.Draw("ap")
canvas_tempo_Tc.SaveAs(cartella_immagini + "tempo_Tc.eps")
input()
