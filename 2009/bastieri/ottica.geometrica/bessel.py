#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("/home/matteo/bin/elaborazione.dati/")
from ds import *

print '----------------------'
print 'BESSEL '
print '----------------------'

P1 = DatiSperimentali('bessel', 0, 0) #prima posizione a fuoco
P2 = DatiSperimentali('bessel', 1, 1) #seconda posizione a fuoco
S = DatiSperimentali('bessel', 1, 1) #saranno le differenze

f = DatiSperimentali('distanze.focali', 0, 1) #distanze focali

fPC = float(open('fpc').read()) #lunghezza focale trovata col metodo dei punti coniugati
fAC = float(open('fac').read()) #lunghezza focale trovata col metodo dell'autocollimazione
Ps = 420. #posizione dello schermo (mm) [è inutile]
L = 220. #L? (mm)
p1p2 = 3.64517 #distanza tra i piani della lente

def ellemezzi():
	R = 5
	l2 = 1.62*R**2/(2*fPC)
#	print 'l/2 = ',  l2
	return l2

def errori_BS():
	global S, L1
	return math.sqrt((0.5**2+0.5**2)*((L1**2 + s**2)/(4*L1**2))**2+(S.calcerrmedia()*S.calcmedia()/2/L1)**2)

n = len(P1.valori)

#for i in range(n):
#	P1.valori[i]-=10.29
#	P2.valori[i]+=10.29
#print "mu_L* atteso: ",  Pl - P0 - fPC + mu0 + dr/2.-p1p2/2.
for i in range(n):
	S.valori[i] = P2.valori[i]-P1.valori[i]
	print '%02.i %05.2f %05.2f %05.2f' %(i,  P1.valori[i], P2.valori[i], S.valori[i])

S = S.converti(10)
L1 = L - p1p2
s = S.calcmedia()
fBS = ((L1**2 - s**2)/(4*L1), errori_BS())

print 'distanza focale stimata con Bessel: %.2f \pm %.2f' %fBS
