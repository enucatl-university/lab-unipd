#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from ROOT import TF1

fu_integral = TF1("fu_integral", "x^5 * exp(x) / (exp(x) -1)^2", 0 , 50)
def rho_c_rid(T, theta):
    return (T / theta)**5 * fu_integral.Integral(0, theta / T)
