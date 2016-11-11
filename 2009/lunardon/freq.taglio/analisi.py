#!/usr/bin/env python
#coding=utf-8

from ds import *


#frequenza di taglio misurata
ft = 262.7

def datioriginali(nome='tutti'):
	global f, vin, vout, dt, a, phi
	f = DatiSperimentali(nome, 0, 0)
	vin = DatiSperimentali(nome, 1, 1)
	vout = DatiSperimentali(nome, 2, 2)
	dt = DatiSperimentali(nome, 3, 3)
	dt.converti(1e-6)
	a = vout/vin
	vin = DatiSperimentali(nome, 1, 1)
	vout = DatiSperimentali(nome, 2, 2)
	phi = dt*f
	f = DatiSperimentali(nome, 0, 0)
	phi.converti(2*math.pi)

def graficoresidui():
	a = DatiSperimentali('41.residui', 0, 0)
	b = DatiSperimentali('41.residui', 1, 1)
	a.grafico(b, 'n',  ('"%.0s"', '"%.2f"'), 'pstricks', (r'$f^2 (\\unit{kHz^2})$', r'$A^{-2}$'), 'f2.ameno2.res', 'yerr')
	a = DatiSperimentali('42.residui', 0, 0)
	b = DatiSperimentali('42.residui', 1, 1)
	a.grafico(b, 'n',  ('"%.0s"', '"%.2f"'), 'pstricks', (r'$f (\\unit{kHz})$', r'$\\tan(\\phi)$'), 'f.tanphi.res', 'yerr')
	a = DatiSperimentali('5.residui', 0, 0)
	b = DatiSperimentali('5.residui', 1, 1)
	a.grafico(b, 'n',  ('"%.1f"', '"%.0s"'), 'pstricks', (r'$\\log(f)$', r'$\\log(A)\\cdot 10^{-3}$'), 'lf.la.res', 'yerr')


datioriginali()
#tan(phi) = f/ft quindi moltiplico f per 1/ft
#parte 3
tanphi = phi.applica(math.tan)
datioriginali()
scrivivalori((f.valori, a.valori, phi.valori), '3')
f.grafico(a, 'n', ('"%.0s"', '"%.1f"'), 'pstricks', (r'$f (\\unit{kHz})$', r'$A$'), 'f.a')
f.grafico(phi, 'n', ('"%.0s"', '"%.1f"'), 'pstricks', (r'$f (\\unit{kHz})$', r'$\\phi$'), 'f.phi')

#parte 4
datioriginali('frequenze')
f2 = f.applica(math.pow, 2)
ameno2 = a.applica(math.pow, -2)
datioriginali('frequenze')
tanphi = phi.applica(math.tan)
datioriginali('frequenze')
scrivivalori((f.valori, f2.valori, ameno2.valori, tanphi.valori), '4')
f2.grafico(ameno2, 's', ('"%.0s"', '"%.1s"'), 'pstricks', (r'$f^2 (\\unit{kHz^2})$', r'$A^{-2}$'), 'f2.ameno2')
l1 = [0.]*len(f2.valori)
for i in range(len(l1)):
	l1[i]= f2.errpost(ameno2)

scrivivalori((f2.valori, f2.residui(ameno2), l1), 'f2.ameno2.res')
print 'interpolazione A-2 = mf2 + c'
f2.bli(ameno2)
i1 = f2.interpolazionelineare(ameno2)
ftamp = i1[2]**(-.5)
sftamp = .5*i1[2]**(-1.5)*i1[3]
percftamp = sftamp/ftamp*100
print 'ftamp = ', ftamp, '±', sftamp, '(',percftamp, '%)'
print 'interpolazione tanphi = mf + c'
f.grafico(tanphi, 's', ('"%.0s"', '"%.1f"'), 'pstricks', (r'$f (\\unit{kHz})$', r'$\\tan(\\phi)$'), 'f.tanphi')
l2 = [0.]*len(f2.valori)
for i in range(len(l2)):
	l2[i]= f.errpost(tanphi)
scrivivalori((f.valori, f.residui(tanphi), l2), 'f.tanphi.res')
f.bli(tanphi)
i2 = f.interpolazionelineare(tanphi)
ftsf = i2[2]**(-1)
sftsf = i2[2]**(-2)*i2[3]
percftsf = sftsf/ftsf*100
print 'ftsfas = ', ftsf, '±', sftsf, '(',percftsf, '%)'
#parte 5, grafico di Bode
datioriginali('bode')
la = a.applica(math.log)
lf = f.applica(math.log)
datioriginali('bode')
scrivivalori((f.valori, lf.valori, la.valori), '5')
print 'interpolazione log A = -log f + c'
lf.bli(la)
lf.grafico(la, 's', ('"%.1f"', '"%.1f"'), 'pstricks', (r'$\\log(f)$', r'$\\log(A)$'), 'lf.la')
l3 = [0.]*len(f2.valori)
for i in range(len(l3)):
	l3[i]= lf.errpost(la)
scrivivalori((lf.valori, lf.residui(la), l3), 'lf.la.res')
i3 = lf.interpolazionelineare(la)
ftbode = math.exp(i3[0])
sftbode = math.exp(i3[0])*i3[1]
percftbode = sftbode/ftbode*100
print 'ftbode = ', ftbode, '±', sftbode, '(',percftbode, '%)'
print 'compatibilità: ',  compatib(ftamp, sftamp, ftbode, sftbode)
scrivivalori(((ftamp, ftbode), (sftamp, sftbode)), 'freq.taglio')
freq = DatiSperimentali('freq.taglio', 0, 1)
print freq.calcmediap()
print freq.calcerrmediap()
tau=1/(2*math.pi*freq.calcmediap())
stau= freq.calcerrmediap()/(2*math.pi*freq.calcmediap()**2)
R = 55600
print 'tau = ',  tau, stau, stau/tau*100
print 'C = ', tau/R, stau/R
graficoresidui()
