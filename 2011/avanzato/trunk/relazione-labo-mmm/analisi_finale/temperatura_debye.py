#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from DebyeTemperature import DebyeTemperature
import os

img_folder = "../relazione/img"
file_name = "../dati/debye"

d = DebyeTemperature(file_name)
d.calculate_chi_square_graph(300, 400, 100, "chi2.out")
d.draw()
d.save_as(os.path.join(img_folder, "chi2.eps"))

d_det = DebyeTemperature(file_name)
d_det.calculate_chi_square_graph(335, 350, 100, "chi2_dettagliato.out")
d_det.draw()
d_det.fit(338, 348)
print("temperatura di debye = {0:.2f} \pm {1:.2f} K".format(
    d_det.debye_temperature,
    d_det.debye_temperature_error))
d_det.draw_error_lines()
d_det.save_as(os.path.join(img_folder, "chi2_dettagliato.eps"))

input()
