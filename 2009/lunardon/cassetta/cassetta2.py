#coding=utf-8

import math

def residui(ascisse, ordinate, m, c):
	lista = []
	for i in range(len(ascisse)):
		lista.append(ordinate[i]-ascisse[i]*m-c)
	return lista

def errorepost(ascisse, ordinate, m, c):
	c = list(residui(ascisse, ordinate, m, c))
	sumsq = 0.
	n = len(ascisse)
	for residuo in c:
		sumsq += residuo**2
	return math.sqrt(sumsq/(n-2))

def leggivalori(file, colonna):
	lista = []
	fi = open(file)
	f = fi.readlines()
	for i in range(len(f)):
		lista.append(float(f[i].split()[colonna]))
	return lista


input = '52'

ascisse = leggivalori(input, 0)
ordinate = leggivalori(input, 1)
errordinate = leggivalori(input, 2)
m = 67.7593e-3
c = 0.00725045

e =  errorepost(ascisse, ordinate, m, c)

for i in range(len(ascisse)):
	print ascisse[i], residui(ascisse, ordinate, m, c)[i], errordinate[i], e
