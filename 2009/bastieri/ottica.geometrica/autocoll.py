#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("/home/matteo/bin/elaborazione.dati/")
from ds import *


mu = DatiSperimentali('autocoll', 0, 0) #lettura del micrometro
Dv = DatiSperimentali('autocoll', 1, 1) #diametro su schermo vicino
Dl = DatiSperimentali('autocoll', 2, 2) #diametro su schermo lontano

fPC = float(open('fpc').read()) #lunghezza focale trovata col metodo dei punti coniugati
Pl = 254. #posizione della lente (mm)
P0 = 200. #posizione della sorgente (mm)
dr = 2.70 #lunghezza dello spigolo orizzontale della lente
mu0 = 8.50 #azzeramento micrometro
p1p2 = 3.64517 #distanza tra i piani della lente

#funzione che calcola la distanza focale in mm con il metodo dell'autocollimazione:
def calc_fAC(m, Pl = 254., P0 = 200., dr = 2.70, mu0 = 8.50, p1p2 = 3.64517, pi ='no'):
	if pi=='no':
		return Pl - P0 - m[0] + mu0 + dr/2.
	else:
		return Pl - P0 - m[0] + mu0 + dr/2.-p1p2/2.

def calc_fAB(f_mis):
	return f_mis+ellemezzi()

def ellemezzi():
	R = 5
	l2 = 1.62*R**2/(2*fPC)
#	print 'l/2 = ',  l2
	return l2

def errori_AC():
	el = ellemezzi()
	return math.sqrt(0.5**2+0.5**2+0.1**2+el**2)

def calc_mu():
	global mu, Dv, Dl
	intV =mu.interpolazionelineare(Dv)
	intL =mu.interpolazionelineare(Dl)
	m_L = (intL[2], intL[3])
	c_L = (intL[0], intL[1])
	m_V = (intV[2], intV[3])
	c_V = (intV[0], intV[1])
	mu_valore = (c_L[0]-c_V[0])/(m_V[0]-m_L[0])
	mu_errore = (1/(intL[2]-intV[2]))*math.sqrt((intL[3]**2+intV[3]**2)*(mu.calcrms()**2 + (mu.calcmedia()-mu_valore)**2))
	mu = (mu_valore, mu_errore)
	return mu
print '----------------------'
print 'AUTOCOLLIMAZIONE '
print '----------------------'
#correzione dati per presunta lettura sbagliata sul micrometro:
Dl.valori[8]+=1
Dl.valori[12]+=1
Dl.valori[13]+=0.5
Dv.valori[5]-=0.5
for DS in (mu, Dv, Dl):
	DS.slice(2, 15)

n = len(mu.valori)
#print "mu_L* atteso: ",  Pl - P0 - fPC + mu0 + dr/2.-p1p2/2.
for i in range(n):
	print '%02.i %05.2f %05.2f %05.2f %-05.2f' %(i,  mu.valori[i], Dv.valori[i], Dl.valori[i],  Dv.valori[i]-Dl.valori[i])

#due rette y = m_V/L x + c_V/L da vicino e da lontano
mu = calc_mu()

print 'intersezione delle due rette mu* = %.2f \pm %.2f' %mu
print 'distanza focale stimata, autocollimazione: ', calc_fAC(mu)
print 'correzione per lenti spesse (p1p2): ', calc_fAC(mu, pi='si')
f_AB = (calc_fAB(calc_fAC(mu, pi='si')), errori_AC())
print 'correzione per aberrazione sferica: %.2f \pm %.2f' %f_AB


print '----------------------'
print 'PUNTI CONIUGATI'
print '----------------------'
ang = (-0.956037, 0.00509)
int = (0.189748, 0.0003456)

print 'retta interpolante y = mx+c:'
print 'm =  %.3f \pm %.3f' %ang
print 'c = %.4f \pm %.4f' %int

f1 = (1/int[0], int[1]/int[0]**2)
f2 = (-(int[0]/ang[0])**(-1), 0)

print f1, f2
f_PC = ((f1[0]+f2[0])/0.2, abs(f1[0]-f2[0])/0.2)

print 'distanza focale stimata, punti coniugati: %.2f \pm %.2f' %f_PC
f_PC2 = (calc_fAB(f_PC[0]), math.sqrt(f_PC[1]**2+(1.62*1.4**2/52.70)**2))
print 'correzione per aberrazione sferica: %.2f \pm %.2f' %f_PC2

open('fpc', 'w').write(str(f_PC2[0]))
open('fac', 'w').write(str(f_AB[0]))
