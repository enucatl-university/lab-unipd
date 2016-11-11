#!/usr/bin/env python
#coding=utf-8

from ds import *

tempi_carica=DatiSperimentali('carica', 0, 0)
volt_carica=DatiSperimentali('carica', 1, 1)
tempi_scarica=DatiSperimentali('scarica', 0, 0)
volt_scarica=DatiSperimentali('scarica', 1, 1)

def diff(lista):
	for i in range(len(lista)):
		lista[i]-=4.2
		lista[i]*=-1

def graficoresidui():
	a = DatiSperimentali('car.res', 0, 0)
	b = DatiSperimentali('car.res', 1, 1)
	a.grafico(b, 'n',  ('"%.0f"', '"%.2f"'), 'pstricks', (r'$t (\\unit{\\mu s})$', r'$\\log(V)$'), 'car.res', 'yerr')
	a = DatiSperimentali('scar.res', 0, 0)
	b = DatiSperimentali('scar.res', 1, 1)
	a.grafico(b, 'n',  ('"%.0f"', '"%.3f"'), 'pstricks', (r'$t (\\unit{\\mu s})$', r'$\\log(V_0-V)$'), 'scar.res', 'yerr')

#diff(volt_carica.valori)

log_volt_carica = volt_carica.applica(math.log)
log_volt_scarica = volt_scarica.applica(math.log)

for valore in log_volt_carica.valori: print valore
print ''
for valore in log_volt_scarica.valori: print valore

print 'carica'
print tempi_carica.corr()
risultati = tempi_carica.interpolazionelineare(log_volt_carica)
for item in risultati:
	print item
tau_c = -1/risultati[2]
errtau_c = risultati[3]/risultati[2]**2
print 'tau = %f \pm %f' %(tau_c,  errtau_c)
print 'errore a posteriori: ',  tempi_carica.errpost(log_volt_carica)
#tempi_carica.grafico(log_volt_carica, 's',  ('"%.0f"', '"%.1f"'), 'pstricks', (r'$t (\\unit{\\mu s})$', r'$\\log(V)$'), 'car')

l1 = [0.]*len(tempi_carica.valori)
for i in range(len(l1)):
	l1[i]= tempi_carica.errpost(log_volt_carica)
scrivivalori((tempi_carica.valori, tempi_carica.residui(log_volt_carica), l1), 'car.res')

print 'scarica'
print tempi_scarica.corr()
risultati = tempi_scarica.interpolazionelineare(log_volt_scarica)
for item in risultati:
	print item
tau_s = -1/risultati[2]
errtau_s = risultati[3]/risultati[2]**2
print 'tau = %f \pm %f' %(tau_s,  errtau_s)
print 'errore a posteriori: ',  tempi_scarica.errpost(log_volt_scarica)
print 'compatibilità: ',  compatib(tau_c, errtau_c, tau_s, errtau_s)

l2 = [0]*len(tempi_scarica.valori)
for i in range(len(l2)):
	l2[i]= tempi_scarica.errpost(log_volt_scarica)
scrivivalori((tempi_scarica.valori, tempi_scarica.residui(log_volt_scarica), l1), 'scar.res')

f = open('tau', 'w')
str = str(tau_c) + ' ' + str(errtau_c) + '\n' + str(tau_s) + ' '+ str(errtau_s)
f.write(str)
f.close()
t = DatiSperimentali('tau', 0, 1)
print 'media pesata: ', t.calcmediap(), '\pm',   t.calcerrmediap()
print 'taglio = ',  1/(2*math.pi*t.calcmediap())
#tempi_scarica.grafico(log_volt_scarica, 's',  ('"%.0f"', '"%.1f"'), 'pstricks', (r'$t (\\unit{\\mu s})$', r'$\\log(V_0-V)$'), 'scar')
print t.calcmediap()*1e-6/55.6e3
print (t.calcmediap()*1e-6/55.6e3)*math.sqrt((t.calcerrmediap()/t.calcmediap())**2+(170/55600)**2)
print '/////////////////////////////////////////////'
#graficoresidui()

