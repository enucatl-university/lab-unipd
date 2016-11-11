#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from DebyeTemperature import DebyeTemperature
import os

img_folder = "../relazione/img"
file_name = "../dati/debye"
temperature = ["_low", "_med", "_high"]
td = [315, 340, 360]

for temp_name, theta in zip(temperature, td):
    d = DebyeTemperature(file_name + temp_name)
    d.calculate_chi_square_graph(theta - 15, theta + 15, 100,
            "chi2_{0}.out".format(temp_name))
    d.draw()
    d.fit(theta - 5, theta + 5)
    print(file_name + temp_name)
#    print("temperatura di debye = {0:.2f} \pm {1:.2f} K".format(
    print("temperatura di debye = {0:.1f} & {1:.1f} K".format(
        d.debye_temperature,
        d.debye_temperature_error))
    d.draw_error_lines()
    d.save_as(os.path.join(img_folder,
        "chi2_{0}.eps".format(temp_name)))
