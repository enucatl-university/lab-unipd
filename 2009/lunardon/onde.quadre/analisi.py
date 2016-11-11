#!/usr/bin/env python
#coding=utf-8

from ds import *

#resistenza utilizzata
r = (55600., 170.571588099)

#1 Misura della resistenza interna dell'oscilloscopio
print '\n 1 Misura della resistenza interna dell\'oscilloscopio'
def sro():
	"""Calcola errore sulla resistenza dell'oscilloscopio"""
	e1 = vout[0]*R[1]/(vin[0]-vout[0])
	e2 = R[0]*vout[0]*vin[1]/(vin[0]-vout[0])**2
	e3 = R[0]*vin[0]*vout[1]/(vin[0]-vout[0])**2
	return math.sqrt(e1**2+e2**2+e3**2)

R = (0.999e6, 2941.08965068)
vout = (8.6, 0.5/math.sqrt(3))
vin = (16.8, 0.5/math.sqrt(3))
ro = ((R[0]*vout[0])/(vin[0]-vout[0]), sro())
print 'resistenza dell\'oscilloscopio %3.3g \pm %3.3g' %ro
print ro[1]/ro[0]*100,  '%'
print 'vin = ', vin
print 'vout = ', vout

#2: Misura della capacità parassita dei cavi.
print '\n 2: Misura della capacità parassita dei cavi.'
def diff(lista):
	for i in range(len(lista)):
		lista[i]-=8.5
		lista[i]*=-1

V = DatiSperimentali('cp', 0, 0)
t = DatiSperimentali('cp', 1, 1)
diff(V.valori)
log_V = V.applica(math.log)

t.bli(log_V)
t.grafico(log_V, 's', ('"%.0s"', '"%.1f"'), 'pstricks', (r'$t (\\unit{\\micro s})$', r'$\\log(V)$'), 'cp')
ep = [0.]*len(t.valori)
for i in range(len(ep)):
	ep[i]= t.errpost(log_V)
scrivivalori((t.valori, log_V.valori, V.valori, t.residui(log_V), ep), 'cp2')
scrivivalori((t.valori, t.residui(log_V), ep), 'graf.cp.res')
m = (t.interpolazionelineare(log_V)[2], t.interpolazionelineare(log_V)[3])
tau_par = (-1/m[0], m[1]/m[0]**2)
print 'tau = ',  tau_par

#calcolo della resistenza equivalente in parallelo:
#non è più necessario con C = -Vin/(Vout*R*m)
#req = (R[0]*ro[0]/(ro[0]+R[0]), math.sqrt((R[0]*ro[1])**2+(ro[0]*R[1])**2)/(ro[0]+R[0])**2)
c_cavi = -vin[0]/(vout[0]*R[0]*m[0])
cp = (c_cavi, c_cavi*math.sqrt((m[1]/m[0])**2+(R[1]/R[0])**2+(vin[1]/vin[0])**2+(vout[1]/vout[0])**2))
#print 'resistenza equivalente: ', req, req[1]/req[0]
print 'capacità parassita: ', cp, cp[1]/cp[0]

#3 calcolo di tau
print '\n 3 calcolo di tau'
T = DatiSperimentali('tau', 0, 0)
T = T.converti(1e-6)
DV = DatiSperimentali('tau', 1, 1)

T.bli(DV)
T.grafico(DV, 's', ('"%.0s"', '"%.1f"'), 'pstricks', (r'$t (\\unit{\\micro s})$', r'$\\Delta V (\\unit{V})$'), 'graf.tau')
ep = [0.]*len(T.valori)
for i in range(len(ep)):
	ep[i]= T.errpost(DV)
scrivivalori((T.valori, DV.valori, T.residui(DV), ep), 'tau2')
scrivivalori((T.valori, T.residui(DV), ep), 'graf.tau.res')
m = (T.interpolazionelineare(DV)[2], T.interpolazionelineare(DV)[3])
tau = [16.4/(4*m[0]), 0]
#scala = 0.03/math.sqrt(3)
#digit = 0.5/math.sqrt(3)
#errore = math.sqrt((scala*16.4)**2+digit**2)
vo = (16.4, 0.40499547322573043)
tau[1] = tau[0]*math.sqrt((vo[1]/vo[0])**2+(m[1]/m[0])**2)
print 'tau = ',  tau

#3.1 da tau calcolo la capacità, prima senza correzione per la capacità parassita
c1 = ((1/r[0]+1/ro[0])*tau[0], math.sqrt((tau[1]*((1/r[0]+1/ro[0])))**2+(tau[0]*r[1]/r[0]**2)**2+(tau[0]*ro[1]/ro[0]**2)**2))
print 'capacità del condensatore, senza contare la capacità parassita: ',  c1,  c1[1]/c1[0]
#correzione per la capacità parassita
c2 = (c1[0]-cp[0], math.sqrt(cp[1]**2+c1[1]**2))
print 'capacità del condensatore, contando la capacità parassita: ',  c2,  c2[1]/c2[0]

#verifica dell'amplificazione
a = (ro[0]/(r[0]+ro[0]), 0)
vin1 = (17.0, 0.5/math.sqrt(3))
vout1 = (16.4, 0.5/math.sqrt(3))
f = (13.32, 0)
ft = (1/(2*math.pi*tau[0]), 1/(2*math.pi*tau[0]**2)*tau[1])
Aprev = (a[0]/math.sqrt(1+(f[0]/ft[0])**2), 0)
Amis = (vout1[0]/vin1[0], 0)
print 'amplificazione prevista: ',  Aprev
print 'amplificazione misurata: ',  Amis, Aprev[0]-Amis[0]

#4 fase di transizione
V_trans = DatiSperimentali('trans', 1, 1)
def trans(n, V0, T, tau):
	#n dispari, n pari, 0
	if n%2 : return V0+(trans(n-1, V0, T, tau)-V0)*math.exp(-T/(2*tau))
	elif n>0 and (n+1)%2 : return trans(n-1, V0, T, tau)*math.exp(-T/(2*tau))
	else: return 0

l = [0.]*len(V_trans.valori)
for i in range(len(l)):
	l[i]=trans(i, 16.4, 266.0e-6, tau[0])
	V_trans.errori[i]=math.sqrt((0.2**2+(0.03*V_trans.valori[i])**2)/3)
V_prev = DatiSperimentali(l, 0, 0)
diff = V_prev-V_trans
scrivivalori((list(range(len(l))), V_trans.valori, V_trans.errori, l,  diff.valori), 'transp')
#for val in diff.valori: print val

#5 ricalcola capacità da esperienza tempo.rc
tau = (534.15371061e-6, 0.738610663508e-6)
c1 = ((1/r[0]+1/ro[0])*tau[0], math.sqrt((tau[1]*((1/r[0]+1/ro[0])))**2+(tau[0]*r[1]/r[0]**2)**2+(tau[0]*ro[1]/ro[0]**2)**2))
print 'capacità del condensatore, senza contare la capacità parassita: ',  c1,  c1[1]/c1[0]
#correzione per la capacità parassita
c2 = (c1[0]-cp[0], math.sqrt(cp[1]**2+c1[1]**2))
print 'capacità del condensatore, contando la capacità parassita: ',  c2,  c2[1]/c2[0]

res_t = DatiSperimentali('cp2', 3, 3)
res_T = DatiSperimentali('tau2', 2, 2)
t.grafico(res_t, 'n', ('"%.0s"', '"%.0s"'), 'pstricks', (r'$t (\\unit{\\micro s})$', r'$\\log(V)\\cdot 10^{-3}$'), 'graf.cp.res', 'yerr')
T.grafico(res_T, 'n', ('"%.0s"', '"%.0s"'), 'pstricks', (r'$t (\\unit{\\micro s})$', r'$\\Delta V (\\unit{mV})$'), 'graf.tau.res', 'yerr')

from gr import *
