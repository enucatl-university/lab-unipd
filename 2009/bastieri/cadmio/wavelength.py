#!/usr/bin/python
#coding=utf-8

#from __future__ import division
import math
from residuals import ResGraph
from array import array
from ROOT import TGraph, TGraphErrors, TF1,  TCanvas

def set_graph_style(g):
    g.SetMarkerStyle(8)
    g.GetXaxis().SetTitle("order")
    g.GetYaxis().SetTitle("sine")
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

A = (12.65e-6, 0.05e-6) #passo del reticolo, con errore
MEASERR = 3 #errore (in primi) stimato a posteriori sulla misura col nonio
MEANERR = 5*MEASERR/math.sqrt(2)/300 #errore sulla media, in centesimi di grado
ARGERR = MEANERR*math.pi/180

class WaveLength(object):
    """			***classe WaveLength***

    legge un file formattato con tre colonne:

    ordine \t nonio A \t nonio B
    5 \t\t 213.54 \t 33.58
    4 \t\t 212.52 \t 32.48
    ... \t ... \t\t ...
    (significa 213°54', 33°58' per il massimo al quinto ordine etc.)

    opera automaticamente la conversione e la media,
    per poi disporre in grafico (self.graph).

    self.fit_graph() esegue l'interpolazione lineare
    self.show_fit_stats() stampa chi quadro / gradi di libertà
    con corrispondente probabilità del fit.

    self.show_graph() mostra il grafico
    self.save_to_eps() salva il grafico in formato .eps

    self.show_res_graph() mostra i residui
    self.save_res_to_eps() salva i residui

    la lunghezza d'onda con viene resituita da self.wavelen,
    che stampa su schermo e restituisce valore ed errore in una lista
    """

    def __init__(self, fileName):
        self.name = fileName
        self.nData = 0
        self.deg = array('d')
        self.degerr = array('d')
        self.ord = array('d')
        self.pars = array('d', [0, 0]) #fit parameters
        self.parerrs = array('d', [0, 0]) #fit parameter errors
        self.line = TF1('line',  'pol1',  -6, 6) #linear function to fit
        self.fill_data() #reads data from file
        self.convert_to_sine() #centers mean maximum, calculates sines
        self.init_graph() #initialize graph, set style

    def fill_data(self):
        file = open(self.name)
        for line in file:
            o = float(line.split()[0])
            n1 = float(line.split()[1]) - 180
            n2 = float(line.split()[2])
            self.ord.append(o)
            int1 = math.floor(n1)
            int2 = math.floor(n2)
            rem1 = 5.*(n1 - int1)/3
            rem2 = 5.*(n2 - int2)/3
            int1 += rem1
            int2 += rem2
            self.deg.append((int1+int2)/2)
            self.degerr.append(MEANERR*math.sqrt(2))
            self.nData += 1
        file.close()

    def convert_to_sine(self):
        j = self.ord.index(0) #finds central maximum
        center = self.deg[j]
        for i in xrange(self.nData):
            angle = self.deg[i]
            angle -= center #center mean maximum
            angle *= math.pi/180 #convert to radians
            self.deg[i] = angle
            self.deg[i] = math.sin(angle)
            self.degerr[i] = math.cos(angle)*ARGERR

    def init_graph(self):
        self.graph = TGraphErrors(self.nData, self.ord, self.deg, array('d', [0]*self.nData), self.degerr)
        set_graph_style(self.graph)
        self.graph.SetTitle(self.name)
        pass

    def fit_graph(self):
        self.graph.Fit('line',  'QR')
        self.line.GetParameters(self.pars)
        self.parerrs[0] = self.line.GetParError(0)
        self.parerrs[1] = self.line.GetParError(1)
        self.r = ResGraph(self.graph, self.line) #creates residual graph
        set_graph_style(self.r.graph)
        self.r.graph.SetTitle(self.r.name)
        return zip(self.pars, self.parerrs)

    def show_fit_stats(self):
        print 'chi square / NDF = ',  self.line.GetChisquare(), '/',  self.line.GetNDF()
        print 'fit probability = ', self.line.GetProb()

    @property
    def wavelen(self):
        wave = [0., 0.]
        wave[0] = math.fabs(self.pars[1]*A[0])*1e9
        wave[1] = wave[0]*math.sqrt((self.parerrs[1]/self.pars[1])**2 + (A[1]/A[0])**2)
#        print 'lambda %s = %.1f \pm %.1f nm' %(self.name, wave[0], wave[1])
        return wave

    @property
    def res_graph(self):
        return self.r.graph

    def show_res_graph(self):
        show_graph(self.r.graph, self.r.name)

    def show_graph(self):
        show_graph(self.graph, self.name)

    def save_to_eps(self):
        if self.pars[1]:
            save_to_eps(self.graph, self.name)
        else: pass

    def save_res_to_eps(self):
        if self.pars[1]:
            save_to_eps(self.r.graph, self.r.name)
        else: pass

    def printData(self):
        """test per verificare la corretta lettura dei dati"""
        for o, d, e in zip(self.ord, self.deg, self.degerr):
            print '%i \t %.3f \t %.3f' %(o, d, e)

    def set_graph_style(self):
        set_graph_style(self.graph)
