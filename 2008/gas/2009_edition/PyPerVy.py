#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import math
from ROOT import TCanvas, TH1F, TGraph, TF1, TGraphErrors, TMath
import time

expect_temps = ['T00', 'T15', 'T25', 'T35', 'T45', 'T55']
compexp = ['_esp', '_comp']

files = [x + y for x in expect_temps for y in compexp]
print(files)

absolute_zero_file = "absolute_zero.out"
out = open(absolute_zero_file, 'w')
for name in files:
    input_file = name + '.dat'
#linear fit gets v0 and nRT with errors 
    with open(input_file) as in_file:
        expected_temp = float(input_file[1:3])
        i = expected_temp // 30
        canv = TCanvas("perfect_gas", "perfect gas law")
        gr = TGraph(input_file)
        perfect_gas = TF1("perfect_gas", "pol1",
                0.34,
                0.86 - i*0.06)
        #shift limits towards high pressure region
#as temperature increases
        gr.SetMarkerStyle(8)
        gr.Draw('AP')
        gr.Fit("perfect_gas","QRW")
        v0 = (-perfect_gas.GetParameter(0),
                perfect_gas.GetParError(0))
        nRT = (perfect_gas.GetParameter(1),
                perfect_gas.GetParError(1))

        temp_hist = TH1F("temp_hist" + name,
                "Temperature Histogram",
                500,
                expected_temp -2,
                expected_temp +2)
        for line in in_file:
            t = float(line.split()[2])
            temp_hist.Fill(t)
        #get temperature distribution
        temp_mean = temp_hist.GetMean()
        temp_sigma = temp_hist.GetRMS()
        temp_canvas = TCanvas("temp_canvas","Temperature")
        temp_hist.Draw()
        #print(temp_mean, temp_sigma)
        print(temp_hist.GetMaximum(), temp_hist.GetMinimum())
        output_line = [nRT[0], temp_mean, nRT[1], temp_sigma, '\n']
        output_line = map(str, output_line)
        output_line = " ".join(output_line)
        out.write(output_line)
        raw_input()
out.close()

canv2 = TCanvas("abs_zero_canv", "Absolute Zero")
abs_zero_gr = TGraphErrors(absolute_zero_file)
abs_zero_func = TF1("abs_zero_func", "pol1", 0, 1)
abs_zero_gr.Fit("abs_zero_func","Q")
abs_zero_gr.Draw("AEP")
zero = (abs_zero_func.GetParameter(0), abs_zero_func.GetParError(0))
nR_inverse = (abs_zero_func.GetParameter(1), abs_zero_func.GetParError(1))
R = TMath.R() / 9.8e-2
num_mole = (1 / (nR_inverse[0] * R),
        1 / (nR_inverse[0] * R) * nR_inverse[1]/nR_inverse[0])
print("Numero di moli: %.4g pm %.4g" %num_mole)
print("zero assoluto = %.3f pm %.3f" %zero)
raw_input()
