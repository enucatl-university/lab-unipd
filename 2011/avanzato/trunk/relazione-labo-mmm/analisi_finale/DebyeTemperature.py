#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from BlochGruneisen import BlochGruneisen
from LettoreFileDebye import LettoreFileDebye
from ROOT import TCanvas, TGraph, TF1, TLine
from style import style
from numpy import linspace
from math import sqrt

class DebyeTemperature(object):

    def __init__(self, file_name):
        super(DebyeTemperature, self).__init__()
        self.reader = LettoreFileDebye(file_name)
        self.bloch_gruneisen = BlochGruneisen(self.reader.T_i,
                self.reader.R_i,
                self.reader.sigma_i)
        
    def calculate_chi_square_graph(self, theta_min, theta_max,
            n_samples, output_file):
        self.graph_file = output_file
        with open(output_file, "w") as out_file:
            for theta in linspace(theta_min, theta_max, n_samples):
                chi_2 = self.bloch_gruneisen.chi_square(theta)
                out_line = [theta, chi_2, "\n"]
                out_line = [str(x) for x in out_line]
                out_line = " ".join(out_line)
                out_file.write(out_line)

    def ndf(self):
        return len(self.reader.T_i) - 1

    def draw(self):
        style.cd()
        canvas_name = self.graph_file + "_can"
        self.canvas = TCanvas(canvas_name, canvas_name)
        self.graph = TGraph(self.graph_file)
        self.graph.SetTitle("#chi^{2};#theta_{D}#[]{K};#chi^{2}")
        self.graph.Draw("ap")

    def save_as(self, name):
        self.canvas.SaveAs(name)

    def fit(self, range_min, range_max):
        self.function = TF1("fit_function", "pol2")
        self.fit_result = self.graph.Fit("fit_function", "qsr", "", range_min, range_max)

    @property
    def debye_temperature(self):
        a = self.fit_result.Parameter(2)
        b = self.fit_result.Parameter(1)
        theta_d = - b / (2 * a)
        return theta_d

    @property
    def debye_temperature_error(self):
        x_0 = self.debye_temperature
        y_min = self.function.Eval(x_0)
        y_tget = y_min + sqrt(2 * self.ndf())
        a = self.fit_result.Parameter(2)
        b = self.fit_result.Parameter(1)
        c = self.fit_result.Parameter(0) - y_tget
        x_tget = (-b + sqrt(b**2 - 4 * a * c)) / (2 * a)
        delta_x = x_tget - x_0
        return delta_x

    def draw_error_lines(self):
        delta_x = self.debye_temperature_error
        x_0 = self.debye_temperature
        y_min = self.function.Eval(x_0)
        y_tget = y_min + sqrt(2 * self.ndf())
        x_min = x_0 - 1.5 * delta_x
        x_max = x_0 + 1.5 * delta_x
        self.l1 = TLine(x_min, y_min, x_max, y_min)
        self.l2 = TLine(x_min, y_tget, x_max, y_tget)
        self.l1.SetLineWidth(1)
        self.l2.SetLineWidth(1)
        self.l1.SetLineStyle(7)
        self.l2.SetLineStyle(7)
        self.l2.Draw("same")
        self.l1.Draw("same")

if __name__ == "__main__":
    file_name = "../dati/debye"
    d = DebyeTemperature(file_name)
    d.calculate_chi_square_graph(300, 400, 100, "chi2.out")
    d.draw()
    d.save_as("../relazione/img/chi2.eps")
    input()
