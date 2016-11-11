#!/usr/bin/python
#coding=utf-8

from __future__ import division, print_function
from DebyeFunction import *
from A import A

class BlochGruneisen(object):
    """calcola la resistenza con l'approssimazione di Bloch-Gruneisen e il
    chi quadro per una data temperatura di Debye"""
    def __init__(self, T_i, R_i, sigma_i):
        self.A = A(T_i, R_i, sigma_i)
        self.T_i = T_i
        self.R_i = R_i
        self.sigma_i = sigma_i

    def chi_square(self, theta):
        A_min = self.A.A_min(theta)
        rho_ci_tilda = self.A.rho_ci_tilda
        chi_2 = sum([(A_min * rho_tilda - R)**2 / sigma**2
            for rho_tilda, R, sigma
            in zip(rho_ci_tilda, self.R_i, self.sigma_i)])
        return chi_2
