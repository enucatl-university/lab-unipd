#!/usr/bin/python
#coding=utf-8

import math
from array import array
from residuals import ResGraph
from ROOT import TGraph, TGraphErrors, TF1,  TCanvas


#ALPHA = input('angolo al vertice del prisma (gradi.primi): ')

def set_graph_style(g):
    g.SetMarkerStyle(8)
    g.GetXaxis().SetTitle("lambda (nm)")
    g.GetYaxis().SetTitle("refraction index")
    g.GetYaxis().SetTitleOffset(1.2)
    g.GetXaxis().SetTitleSize(0.03)
    g.GetYaxis().SetTitleSize(0.03)
    g.GetXaxis().SetLabelSize(0.03)
    g.GetYaxis().SetLabelSize(0.03)
    g.GetXaxis().SetDecimals()
    g.GetYaxis().SetDecimals()

def save_to_eps(g, name):
    c = TCanvas(name, name)
    g.Draw('AEP')
    c.SaveAs(name + '.eps')

def show_graph(g, name):
    c = TCanvas(name, name)
    g.Draw('AEP')
    raw_input('Press ENTER to continue...')

def mean_angle(n1, n2):
    n1 = float(n1)
    n2 = float(n2)
    int1 = math.floor(n1)
    int2 = math.floor(n2)
    rem1 = 5.*(n1 - int1)/3
    rem2 = 5.*(n2 - int2)/3
    int1 += rem1
    int2 += rem2
    return (int1+int2)/2

try:
    data = open('alpha').read().split()
    ALPHA = mean_angle(data[0], data[1]) - mean_angle(data[2], data[3])
except IOError:
    print 'File %s not found!' %file
    ALPHA = 60.00*math.pi/180 #angolo al vertice del prisma
print 'Angolo al vertice: ', ALPHA
ALPHA *= math.pi/180 #in radianti

class RefractedCadmium(object):
    def __init__(self, file):
        """file contiene:
        misura dell'angolo sul nonio A es. 203.14
        misura dell'angolo sul nonio B es.  23.08
        misura dello zero sul nonio A es. 194.10
        misura dello zero sul nonio B es. 13.00
        """
        #calcola l'angolo di minima deflessione:
        try:
            data = open(file).read().split()
        except IOError:
            print 'File %s not found!' %file
            data = [0]*4
        self.delta = mean_angle(data[0], data[1]) - mean_angle(data[2], data[3])
        self.delta *= math.pi/180 #in radianti
        self.n = math.sin((ALPHA + self.delta) / 2) / math.sin(ALPHA / 2) #calcola indice di rifrazione
        err_delta = 2 #errore su delta, in primi
        err_delta *= 5*math.pi/180/300
        self.errn = 0.5 * err_delta * math.cos((ALPHA + self.delta) / 2) / math.sin(ALPHA / 2)

class CauchyRelation(object):
    def __init__(self, ref_indexes, err_ref_ind, wavelengths):
        self.name = 'Cauchy Relation'
        self.init_graph(ref_indexes, err_ref_ind, wavelengths)
        self.fit_graph()

    def init_graph(self, ref_indexes, err_ref_ind, wavelengths):
        n = array('d', ref_indexes)
        errn = array('d', err_ref_ind)
        wl = array('d', wavelengths)
        errwl = array('d', [0]*len(wavelengths))
        self.pars = array('d', [0]*3) #fit parameters
        self.parerrs = array('d', [0]*3) #fit parameter errors
        self.graph = TGraphErrors(len(wavelengths), wl, n, errwl, errn)
        set_graph_style(self.graph)
        self.graph.SetTitle(self.name)

    def fit_graph(self):
        self.func = TF1('cauchy', '[0] + [1]/x**2', 400, 700)
        self.func.SetParameters(10, 1e4)
        self.graph.Fit('cauchy',  'QR')
        self.func.GetParameters(self.pars)
        self.parerrs[0] = self.func.GetParError(0)
        self.parerrs[1] = self.func.GetParError(1)
        self.r = ResGraph(self.graph, self.func) #creates residual graph
        set_graph_style(self.r.graph)
        self.r.graph.SetTitle(self.r.name)
        return zip(self.pars, self.parerrs)

    def show_res_graph(self):
        show_graph(self.r.graph, self.r.name)

    def show_graph(self):
        show_graph(self.graph, self.name)


class LinearRelation(object):                                 
    def __init__(self, ref_indexes, err_ref_ind, wavelengths):
        self.name = 'Linear Relation'
        self.init_graph(ref_indexes, err_ref_ind, wavelengths)
        self.fit_graph()

    def init_graph(self, ref_indexes, err_ref_ind, wavelengths):
        n = array('d', ref_indexes)
        errn = array('d', err_ref_ind)
        wl = array('d', wavelengths)
        errwl = array('d', [0]*len(wavelengths))
        self.pars = array('d', [0]*3) #fit parameters
        self.parerrs = array('d', [0]*3) #fit parameter errors
        self.graph = TGraphErrors(len(wavelengths), wl, n, errwl, errn)
        set_graph_style(self.graph)
        self.graph.SetTitle(self.name)

    def fit_graph(self):
        self.func = TF1('line', '[0] + [1]*x ', 0.0, 1.)
        self.func.SetParameters(10, 10)
        self.graph.Fit('line',  'R')
        self.func.GetParameters(self.pars)
        self.parerrs[0] = self.func.GetParError(0)
        self.parerrs[1] = self.func.GetParError(1)
        self.r = ResGraph(self.graph, self.func) #creates residual graph
        set_graph_style(self.r.graph)
        self.r.graph.SetTitle(self.r.name)
        return zip(self.pars, self.parerrs)

    def show_res_graph(self):
        show_graph(self.r.graph, self.r.name)

    def show_graph(self):
        show_graph(self.graph, self.name)
