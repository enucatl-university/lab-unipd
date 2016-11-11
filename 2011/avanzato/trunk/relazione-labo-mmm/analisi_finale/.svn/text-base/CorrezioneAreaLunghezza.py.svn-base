#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
import os
from calibrazione.potenziometro_temperatura import PotenziometroTemperatura
from calibrazione.potenziometro_resistenza import PotenziometroResistenza
from LettoreFileDebye import LettoreFileDebye
from DebyeTemperature import DebyeTemperature
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

def coefficiente_correttivo(T):
    return alpha * (T - T0)

class CorrezioneAreaLunghezza(LettoreFileDebye):
    """Legge il file con Volt, corrente, Rt, Rd e restituisce temperature,
    resistenze ed errori per l'analisi della temperatura di Debye.
    Inserita correzione al primo ordine per la dipendenza della sezione e
    lunghezza del filo dalla temperatura"""

    def __init__(self, *args, **kwargs):
        super(CorrezioneAreaLunghezza, self).__init__(*args, **kwargs)

    def draw(self, output_file):
        self.output_filename = output_file
        with open(output_file, "w") as out_file:
            for T, sigma_T, R, sigma_R in zip(
                    self.T_i,
                    self.sigma_Ti,
                    self.R_i,
                    self.sigma_i):
                out_line = [T, R * (1 + coefficiente_correttivo(T)), sigma_T, sigma_R, "\n"]
                out_line = [str(x) for x in out_line]
                out_line = " ".join(out_line)
                out_file.write(out_line)
        style.cd()
        self.canvas = TCanvas("temperatura_resistenza_can",
                "temperatura_resistenza_can")
        self.graph = TGraphErrors(output_file)
        self.graph.SetTitle("Resistenza del campione;T#[]{K};R#[]{#Omega}")
        self.graph.Draw("ap")

class CorrezioneTemperaturaDebye(DebyeTemperature):

    def __init__(self, file_name):
        super(CorrezioneTemperaturaDebye, self).__init__(file_name)
        self.reader = CorrezioneAreaLunghezza(file_name)

if __name__ == "__main__":
    img_folder = "../relazione/img"
    file_name = "../dati/debye"

    d = CorrezioneTemperaturaDebye(file_name)
    d.calculate_chi_square_graph(300, 400, 100, "chi2_corretto.out")
    d.draw()
    d.save_as(os.path.join(img_folder, "chi2_corretto.eps"))

    d_det = DebyeTemperature(file_name)
    d_det.calculate_chi_square_graph(335, 350, 100,
            "chi2_dettagliato_corretto.out")
    d_det.draw()
    d_det.fit(338, 348)
    print("temperatura di debye = {0:.2f} \pm {1:.2f} K".format(
        d_det.debye_temperature,
        d_det.debye_temperature_error))
    d_det.draw_error_lines()
    d_det.save_as(os.path.join(img_folder, "chi2_dettagliato_corretto.eps"))
    #l = CorrezioneAreaLunghezza("../dati/debye")
    #l.draw("temperatura_resistenza_correzione.out")
    #l.save_as("../relazione/img/temperatura_resistenza_correzione_debye.eps")
    #l.tabella_latex("../relazione/tab/temperatura_resistenza_correzione_debye.tex")
    input()
