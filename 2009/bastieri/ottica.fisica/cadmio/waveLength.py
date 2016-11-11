#!/usr/bin/python
#coding=utf-8

from math import *
from array import array
from ROOT import TGraph, TGraphErrors, TF1,  TCanvas

a = (12.65e-6, 0.05e-6) #passo del reticolo, con errore
measerr = 5.*2/300 #errore (in gradi) stimato sulla misura col nonio
meanerr = measerr/sqrt(2)
argerr = meanerr*pi/180

class waveLength :
	"""			***classe waveLength***

	legge un file formattato con tre colonne:

	ordine	nonio A	nonio B
	5	213.54	33.58
	4	212.52	32.48
	...	...	...
	(significa 213°54', 33°58' per il massimo al quinto ordine etc.)

	opera automaticamente la conversione e la media,
	per poi disporre in grafico (self.graph).

	self.fitGraph() esegue l'interpolazione lineare
	self.showGraph() mostra il grafico
	self.saveToEps() salve il grafico in formato .eps

	la lunghezza d'onda con si calcola con self.getWaveLen(),
	che restituisce una valore ed errore in una lista
	"""
#	a = (12.65e-6, 0.05e-6) #passo del reticolo, con errore
#	measerr = 5.*2/300 #errore (in gradi) stimato sulla misura col nonio

	def __init__( self, fileName ):
		self.wavelen = [0, 0]
		self.name = fileName
		self.nData = 0
		self.deg = array( 'd' )
		self.degerr = array( 'd' )
		self.ord = array( 'd' )
		self.pars = array( 'd', [0, 0] ) #fit parameters
		self.parerrs = array( 'd', [0, 0] ) #fit parameter errors
		self.fillDeg() #reads data from file
		self.convertToSine() #centers mean maximum, calculates sines
		self.initGraph() #initialize graph, set style

	def fillDeg( self ):
		file = open( self.name )
		for line in file:
			o = float( line.split()[0] )
			n1 = float( line.split()[1] ) - 180
			n2 = float( line.split()[2] )
			self.ord.append( o )
			int1 = floor( n1 )
			int2 = floor( n2 )
			rem1 = 5.*(n1 - int1)/3
			rem2 = 5.*(n2 - int2)/3
			int1 += rem1
			int2 += rem2
			self.deg.append( (int1+int2)/2 )
			self.degerr.append( measerr/sqrt(2) )
			self.nData += 1
		file.close()

	def convertToSine( self ):
		j = self.ord.index( 0 ) #finds central maximum
		center = self.deg[j]
		for i in xrange( self.nData ):
			angle = self.deg[i]
			angle -= center
			self.deg[i] = angle
			self.deg[i] = sin( pi*angle/180 )
			self.degerr[i] = cos( angle )*argerr

	def initGraph( self ):
		self.graph = TGraphErrors( self.nData, self.ord, self.deg, array('d', [0]*self.nData), self.degerr )
		self.setGraphStyle()
		pass

	def fitGraph( self ):
		line = TF1( 'line',  'pol1',  -5, 5 ) #funzione lineare per fit
		self.graph.Fit( 'line',  'QR' )
		line.GetParameters( self.pars )
		self.parerrs[0] = line.GetParError(0)
		self.parerrs[1] = line.GetParError(1)
		return zip( self.pars, self.parerrs )

	def getWaveLen( self ):
		self.wavelen[0] = fabs( self.pars[1]*a[0] )*1e9
		self.wavelen[1] = self.wavelen[0]*sqrt( (self.parerrs[1]/self.pars[1])**2 + (a[1]/a[0])**2 )
		print 'lambda %s = %.1f \pm %.1f nm' %(self.name, self.wavelen[0], self.wavelen[1])
		return self.wavelen

	def showGraph( self ):
		c = TCanvas( self.name, self.name )
		self.graph.Draw( 'AEP' )
		raw_input('Press ENTER to continue...')

	def saveToEps( self ):
		if self.pars[1]:
			c = TCanvas( self.name, self.name )
			self.graph.Draw( 'AEP' )
			c.SaveAs( self.name + '.fit.eps' )
		else: pass


	def printData( self ):
		"""test per verificare la corretta lettura dei dati"""
		for o, d, e in zip( self.ord, self.deg, self.degerr ):
			print '%i \t %.3f \t %.3f' %(o, d, e)

	def setGraphStyle( self ):
		self.graph.SetMarkerStyle( 8 )
		self.graph.GetXaxis().SetTitle( "order" );
		self.graph.GetYaxis().SetTitle( "sine" );
		self.graph.GetYaxis().SetTitleOffset( 1.2 );
		self.graph.GetXaxis().SetTitleSize( 0.03 );
		self.graph.GetYaxis().SetTitleSize( 0.03 );
		self.graph.GetXaxis().SetLabelSize( 0.03 );
		self.graph.GetYaxis().SetLabelSize( 0.03 );
		self.graph.GetXaxis().SetDecimals(  );
		self.graph.GetYaxis().SetDecimals(  );
#		self.graph.SetStats( kFALSE );
		self.graph.SetTitle( self.name );

