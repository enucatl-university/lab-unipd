#coding=utf-8
from __future__ import division
from ROOT import TH1F, TStyle, TSpectrum, TCanvas

style = TStyle("style", "style")
style.SetCanvasColor(0)
style.SetMarkerStyle(5)
style.SetTitleFillColor(0)
style.cd()


class TrovaPicchi:
    def __init__(self, nomefile, sigma):
        n, nstep, step = [int(i) for i in nomefile.split(".")[0].split("_")]
        self.nfenditure = n
        self.canvas = TCanvas("canvas{0}".format(n), "canvas {0} fenditure".format(n))
        self.isto = TH1F("isto{0}".format(n),
                "{0} fenditure;bin ;-log(intensity)".format(n),
                nstep, -nstep/2*step/100, (nstep/2+1)*step/100)
        self.isto.SetStats(0)
        self.file2isto(nomefile)
        self.spectrum = TSpectrum()
        self.spectrum.Search(self.isto, sigma, "nobackground", 0.01)
        self.peaks = [self.spectrum.GetPositionX()[i] for i in range(self.spectrum.GetNPeaks())]

    def file2isto(self, nomefile):
        file = open(nomefile)
        for line in file:
            bin, content = [float(i) for i in line.split()]
            self.isto.Fill(bin/100, -content+500)
        file.close()

t1 = TrovaPicchi("1_400_20.dat", 2)
t2 = TrovaPicchi("2_800_10.dat", 0.01)


#files = ["1_400_20.dat", "2_800_10.dat", "3_1600_5.dat", "4_1600_5.dat"]
#for file in files:
#    t = TrovaPicchi(file)
#    t.isto.Draw()
input()

