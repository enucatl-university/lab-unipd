#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TH1I, TCanvas, TF1, TGraph, TAxis
from math import fabs

bins = 7926
def leggi_hist(file_name):
    hist = TH1I(file_name, file_name, bins, 0, bins)
    with open(file_name) as file:
        for i, line in enumerate(file):
            line = float(line)
            hist.SetBinContent(i + 1, line)
    return hist

def parametri(i,j,k):
	R = (l[i] - l[j]) * (x[j] - x[k]) / ((l[j] - l[k]) * (x[i] - x[j]))
	x0 = (R * x[i] - x[k]) / (R - 1)
	c = - (l[i] - l[j]) * ((x[i] - x0) * (x[j] - x0)) / (x[i] - x[j])
	l0 = l[i] + c / (x0 - x[i])
	return x0, c, l0

def lam(x, x0, c, l0):
	return l0 + c / (x - x0)

def fit(hist, min, max):
    hist.GetXaxis().SetRange(min, max)
    mean = hist.GetMean()
    mean_err = hist.GetMeanError()
    hist.GetXaxis().SetRange()
    return mean, mean_err


	
file_noto = "t12000-m10.csv"

noto = leggi_hist(file_noto)
l = [4046.5599999999999, 4358.3500000000004, 4678.1599999999999, 4799.3199999999997, 5085.8199999999997, 5460.7799999999997, 5769.5900000000001, 5790.6499999999996]

list = []
list.append(fit(noto, 360, 400))
list.append(fit(noto, 2465, 2495))
list.append(fit(noto, 3925, 3945))
list.append(fit(noto, 4360, 4380))
list.append(fit(noto, 5215, 5235))
list.append(fit(noto, 6070, 6085))
list.append(fit(noto, 6610, 6635))
list.append(fit(noto, 6645, 6670))

can1 = TCanvas("noto", "noto")
noto.Draw()

x = [xi for xi, e in list]
x_e = [e for xi, e in list]

with open("xl.out", "w") as file:
    for xi, li, xe in zip(x, l, x_e):
        line = [xi, li, xe, 0]
        line = [str(x) for x in line]
        line = " ".join(line)
        line += "\n"
        file.write(line)

x0, c, l0 = parametri(0, 3, 7)
delta_lambda = [l_i - lam(x_i, x0, c, l0) for l_i, x_i in zip(l, x)]

delta_lambda_file = "delta_lambda.out"
with open(delta_lambda_file, "w") as file:
    for l_i, delta_i in zip(l, delta_lambda):
        line = str(l_i) + " " + str(delta_i) + "\n"
        file.write(line)

can2 = TCanvas("res", "res")
res_graph = TGraph(delta_lambda_file)
res_graph.GetYaxis().SetTitle("#Delta #lambda #[]{#dot{A}}")
res_graph.GetYaxis().SetDecimals()
res_graph.GetXaxis().SetTitle("#lambda #[]{#dot{A}}")
res_graph.Draw("ALP")

#spettro incognito
file_incognito = "incognito-t100k-m20.csv"
file_fondo = "fondo.csv"
can3 = TCanvas("unk", "unk")

incognito = leggi_hist(file_incognito)
fondo = leggi_hist(file_fondo)

incognito.Add(fondo, -1)
list = []
list.append(fit(incognito, 1520, 1555))
list.append(fit(incognito, 1610, 1645))
incognito.Draw()

unknown_x = [xi for xi, e in list]
unknown_x_err = [e for xi, e in list]
unknown_lambda = [lam(x, x0, c, l0) for x in unknown_x]
unknown_lambda_err = [fabs(-c / (x - x0)**2) * x_err
        for x, x_err in zip(unknown_x, unknown_x_err)]

print(unknown_lambda)
print(unknown_lambda_err)
input()
