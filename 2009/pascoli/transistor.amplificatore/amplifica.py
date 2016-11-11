#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import math
from ROOT import TGraphErrors, TCanvas, TF1

file_dati = 'amplificazione.dat'
file_output = 'amplificazione.out'

def set_graph_style(graph):
    graph.SetMarkerStyle(7)
    graph.SetTitle()
    graph.SetFillColor(10)
    x_axis = graph.GetXaxis()
    y_axis = graph.GetYaxis()
    x_axis.SetTitle("frequenza (kHz)")
    y_axis.SetTitle("amplificazione")
    x_axis.SetLabelSize(0.03)
    y_axis.SetLabelSize(0.03)
    x_axis.SetTitleSize(0.03)
    y_axis.SetTitleSize(0.03)
    x_axis.SetTitleOffset(1.2)
    y_axis.SetTitleOffset(1.2)
    return graph

def freq_taglio(a, b, corr, at):
    freq = (at[0] - a[0])/b[0]
    freq_max = (1.06*at[0]-a[0])/b[0]
    err = freq_max - freq
    err = math.fabs(err)
    return (freq, err)

with open(file_output,'w') as file_out:
    with open(file_dati) as file:
        for line in file:
            if line[0] is '#': continue
            f, vin, vout = map(float, line.split())
            a = vout / vin
            output_line = " ".join(map(str, (f, a, 0, a*0.06))) + "\n"
            file_out.write(output_line)

canv = TCanvas('ampli','ampli')
gr = TGraphErrors(file_output)
#
#create functions
inf = TF1('inferiore','[0]+[1]*x',0,35)
sup = TF1('superiore','[0]+[1]*x',2e3,4e3)
amplifica = TF1('amplificazione', '[0]', 300, 650)
amplifica.SetParameter("0",22)
amplifica.SetLineStyle(7) #dashed
amplifica.SetLineWidth(1)
canv.SetLogx()
gr.Fit('inferiore', 'QR+')
gr.Fit('superiore', 'QR+')
gr.Fit('amplificazione', 'QR+')
amplificazione = amplifica.GetParameter(0)
ampl_taglio = amplificazione / math.sqrt(2)
taglio = TF1('ampiezzataglio', str(ampl_taglio),0,5e3)
gr = set_graph_style(gr)
taglio.SetLineStyle(7) #dashed
taglio.SetLineWidth(1)
canv.SetFillColor(10)
gr.Draw('AP')
taglio.Draw("LSAME")

a_inf = (inf.GetParameter(0), inf.GetParError(0))
b_inf = (inf.GetParameter(1), inf.GetParError(1))
a_sup = (sup.GetParameter(0), sup.GetParError(0))
b_sup = (sup.GetParameter(1), sup.GetParError(1))
ampl_taglio = (ampl_taglio, 0.6/math.sqrt(2))
freq_inf = freq_taglio(a_inf, b_inf, ampl_taglio)
freq_sup = freq_taglio(a_sup, b_sup, ampl_taglio)

print("freq taglio inferiore = %.1f pm %.1f" %freq_inf)
print("freq taglio superiore = %.1f pm %.1f" %freq_sup)
print("amplificazione media = ", amplificazione)
print("ampiezza di taglio = ", ampl_taglio)
canv.SaveAs('amplificazione.eps')
#raw_input()
