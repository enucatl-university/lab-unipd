#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("/home/matteo/bin/elaborazione.dati/")
from ds import *

print '----------------------'
print 'ABERRAZIONE CROMATICA '
print '----------------------'


xblu = DatiSperimentali('cromatica', 0, 0) #blu a fuoco
xrosso = DatiSperimentali('cromatica', 1, 1) #rosso a fuoco
A = DatiSperimentali('cromatica', 1, 1) #saranno le differenze

fPC = float(open('fpc').read()) #lunghezza focale trovata col metodo dei punti coniugati
fAC = float(open('fac').read()) #lunghezza focale trovata col metodo dell'autocollimazione
Ps = 420. #posizione dello schermo (mm)
L = 220. #L? (mm)
p1p2 = 0.364517 #distanza tra i piani della lente

n = len(xblu.valori)
#print "mu_L* atteso: ",  Pl - P0 - fPC + mu0 + dr/2.-p1p2/2.
for i in range(n):
	A.valori[i] = xrosso.valori[i]-xblu.valori[i]
	print '%02.i %05.2f %05.2f %05.2f' %(i,  xblu.valori[i], xrosso.valori[i], A.valori[i])

abbe = 52.07/A.calcmedia()
abberr = abbe*math.sqrt(A.calcerrmedia()**2/A.calcmedia()**2 + 0.5**2/52.1**2)

print 'A media: ',  A.calcmedia(),  A.calcerrmedia()
print 'Numero di Abbe: ', abbe,  '\pm',  abberr


print '----------------------'
print 'ABERRAZIONE SFERICA '
print '----------------------'
xvic = DatiSperimentali('sferica', 3, 3) #posizione a fuoco prossimali
xlont = DatiSperimentali('sferica', 0, 0) #posizione a fuoco marginali
xs = DatiSperimentali('sferica', 4, 4) #posizione buco a sinistra
xd = DatiSperimentali('sferica', 5, 5) #posizione buco a destra
t = DatiSperimentali('sferica', 4, 4) #saranno le differenze
L = DatiSperimentali('sferica', 4, 4) #saranno le differenze

n = len(xs.valori)
#print "mu_L* atteso: ",  Pl - P0 - fPC + mu0 + dr/2.-p1p2/2.
for i in range(n):
	t.valori[i] = xs.valori[i]-xd.valori[i]
	L.valori[i] = xvic.valori[i]-xlont.valori[i]
	print '%02.i %05.2f %05.2f %05.2f %05.2f' %(i,  xs.valori[i], xd.valori[i], t.valori[i], L.valori[i])

R = 14.0 #distanza tra i due buchi sulla sorgente (mm)
cL = fPC*L.calcmedia()/R**2
cT = fPC**2*t.calcmedia()/(R**2*(2*R+t.calcmedia()))

print 'Coefficiente di aberrazione sferica longitudinale cL: ', cL
print 'Coefficiente di aberrazione sferica trasversale cT: ', cT
print 'media = %.3f \pm %.3f' %((cL+cT)/2., abs(cL-cT)/2.)
