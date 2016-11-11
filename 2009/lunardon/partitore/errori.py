#!/usr/bin/env python
#coding=utf-8

import math

a = 3**(-0.5)
#dizionari degli strumenti {FS:(percentuale,digit),...}
dizionario = {'FlukeVolt':{6:(0.7, 2e-3), 60:(1, 0.03), 62:(0, 2e-3)}, \
							'FlukeOhm':{600:(0.9, 0.2), 6000:(0.1, 1), 6002:(0, 0.2)}, \
							'TVolt':{0.2:(0.25, 1e-4),\
											2:(0.25, 1e-3), \
											20:(0.25, 0.01), \
											200:(0.25, 0.1)},\
							'TAmp':{200e-6:(0.75, 1e-7),\
											0.2:(0.75, 0.1e-3), \
											20e-3:(0.75, 0.01e-3)}, \
							'TOhm':{20e6:(1.5, 0.05e6), 2e6:(0.5, 0.001e6), 200e3:(0.5, 0.1e3)}}


def errore(misura, FS, strumento):
	"""strumento è un dizionario dove ci dato il fondo scala si ricavano errore percentuale ed errore di digit"""
	global a, dizionario
	s = dizionario[strumento][FS]
	b = misura*s[0]/100.
	c = s[1]
	return a*math.sqrt((b)**2+(c)**2)

misura = input('Misura: ')
FS = input ('Fondo scala: ')
strumento = raw_input('Strumento [FlukeVolt, FlukeOhm, TVolt, TAmp, TOhm]: ')
print 'errore: ',  errore(misura, FS, strumento)
