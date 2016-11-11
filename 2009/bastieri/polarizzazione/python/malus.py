#coding=utf-8

from array import array
from sys import exit
from ROOT import TH1D, TF1
from math import pi

class Malus(object):
    def __init__(self, file_name):
        try:
            file = open(file_name)
        except IOError:
            print "file %s not found!" %file_name
            exit(2)
        self.histogram = TH1D(file_name, file_name, 720, 0, 360)
        for line in file:
            dd, ii = line.split()
            dd, ii = float(dd), float(ii)
            self.histogram.Fill(dd, ii)
        file.close()
        self.phi = array('d')
        self.phi_err = array('d')
        self.set_style()

    def get_phi(self, begin, end):
        self.cos2 = TF1("cos2", "[0]*(cos([1] * (x-[2])))^2", begin, end)
        self.cos2.SetParameters(212, pi / 180, 25)
        self.histogram.Fit("cos2", "WQR+")
        phi = self.cos2.GetParameter(2)
        phi_err = self.cos2.GetParError(2)
        self.phi.append(phi)
        self.phi_err.append(phi_err/2.5)
        return phi, phi_err

    def set_style(self):
        self.histogram.GetXaxis().SetTitle("angle (deg)")
        self.histogram.GetYaxis().SetTitle("intensity")
        self.histogram.GetXaxis().SetTitleSize(0.03)
        self.histogram.GetYaxis().SetTitleSize(0.03)
        self.histogram.GetXaxis().SetLabelSize(0.03)
        self.histogram.GetYaxis().SetLabelSize(0.03)
        self.histogram.GetYaxis().SetTitleOffset(1.2)
        self.histogram.GetXaxis().SetDecimals()
        self.histogram.GetYaxis().SetDecimals()
        self.histogram.SetStats(False)
        self.histogram.SetTitle("")

    def draw_hist(self):
        self.histogram.Draw()
        pass
