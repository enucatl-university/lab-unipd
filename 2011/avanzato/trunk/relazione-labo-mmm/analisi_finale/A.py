#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from DebyeFunction import *

class A(object):

    def __init__(self, T_i, R_i, sigma_i):
        self.T_i = T_i
        self.R_i = R_i
        self.sigma_i = sigma_i

    def calc_rho_c(self, theta):
        self.rho_ci_tilda = [rho_c_rid(T, theta) for T in self.T_i]

    def A_min(self, theta):
        self.calc_rho_c(theta)
        s1 = sum([rho_c**2 / sigma**2
            for rho_c, sigma in zip(
                self.rho_ci_tilda,
                self.sigma_i)])
        s2 = sum([rho_c * rho / sigma**2
            for rho_c, rho, sigma in zip(
                self.rho_ci_tilda,
                self.R_i,
                self.sigma_i)])
        return s2 / s1
