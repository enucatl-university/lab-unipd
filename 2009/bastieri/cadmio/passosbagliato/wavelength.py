from __future__ import division
import math
from ROOT import TGraph, TF1, TCanvas

def to_decimal(deg):
    int = math.floor(deg)
    rem = 5*(deg - int) / 3
    return int + rem

class WaveLength(object):
    def __init__(self, file_name):
        self.output_file = file_name + '.out'
        with open(file_name) as input_file:
            with open(self.output_file, 'w') as output:
                for line in input_file:
                    o, n1, n2 = [float(x) for x in line.split()]
                    n1, n2 = to_decimal(n1), to_decimal(n2)
                    angle = ((n1 - 180) + n2)*math.pi/360
                    sine = math.sin(angle)
                    out_string = str(o) + ' ' + str(sine) + '\n'
                    output.write(out_string)

    def fit_graph(self):
        self.graph = TGraph(self.output_file)
        self.func = TF1('line', 'pol1', -6, 6)
        self.graph.Fit('line', 'QW')
        self.slope = self.func.GetParameter(1)
        #canv = TCanvas('can', 'can')
        self.graph.SetMarkerStyle(8)
        #self.graph.Draw('AP')

    def get_separation(self, wavelen):
        self.separation = math.fabs(wavelen / self.slope)
        return self.separation
