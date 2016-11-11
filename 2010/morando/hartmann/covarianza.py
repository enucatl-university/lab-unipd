#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TF1, TGraphErrors, TCanvas, TH1I
from scipy import mat, linalg
from math import sqrt, fabs

bins = 7926
def leggi_hist(file_name):
    hist = TH1I(file_name, file_name, bins, 0, bins)
    with open(file_name) as file:
        for i, line in enumerate(file):
            line = float(line)
            hist.SetBinContent(i + 1, line)
    return hist

def lam(x, x0, c, l0):
	return l0 + c / (x - x0)

def fit(hist, min, max):
    hist.GetXaxis().SetRange(min, max)
    mean = hist.GetMean()
    mean_err = hist.GetMeanError()
    hist.GetXaxis().SetRange()
    return mean, mean_err

def lambda_var(x, xe):
    f1 = 1
    f2 = 1 / (x - x0)
    f3 = c / (x - x0)**2
    f = [f1, f2, f3]
    f = [str(_) for _ in f]
    f = "[" + "; ".join(f) + "]"
    f = mat(f)
    return f.transpose() * covariance_matrix * f

hartmann_graph = TGraphErrors("xl.out");
hartmann_fun = TF1("hartmann", "[0] + [1] / (x - [2])");
#hartmann_fun.SetParameters(2702.8, -14935288.5, 11494.13);
hartmann_fun.SetParameters(2.70244e3, -1.49207e7, 1.14865e4);
hartmann_graph.SetMarkerStyle(8);
hartmann_graph.Fit("hartmann", "V");
l0 = hartmann_fun.GetParameter(0)
c = hartmann_fun.GetParameter(1)
x0 = hartmann_fun.GetParameter(2)

covariance_matrix = mat("[2.720e-2 3.995e2 -9.053e-2;\
        3.955e2 5.826e6 -1.348e3;\
        -9.053e-2 -1.348e3 3.152e-1]")

la, v = linalg.eig(covariance_matrix)
print(la)

file_incognito = "incognito-t100k-m20.csv"
file_fondo = "fondo.csv"
incognito = leggi_hist(file_incognito)
fondo = leggi_hist(file_fondo)

incognito.Add(fondo, -1)
list = []
list.append(fit(incognito, 1520, 1555))
list.append(fit(incognito, 1610, 1645))

unknown_x = [xi for xi, e in list]
unknown_x_err = [e for xi, e in list]
unknown_lambda = [lam(x, x0, c, l0) for x in unknown_x]
unknown_lambda_err = [fabs(-c / (x - x0)**2) * x_err
        for x, x_err in zip(unknown_x, unknown_x_err)]
unknown_lambda_err2 = [(lambda_var(x, x_err))
        for x, x_err in zip(unknown_x, unknown_x_err)]

print(unknown_lambda_err, unknown_lambda_err2)
