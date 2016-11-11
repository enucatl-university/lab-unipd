#coding=utf-8

from ds import *

def delta(misura, uplaerr):
	return misura*uplaerr[0]/100. + uplaerr[1]

def sigma(misura, uplaerr):
	return math.sqrt((0.58*misura*uplaerr[0]/100.)**2+(0.58*uplaerr[1])**2)

def sigmaP(r1, r2, sr1, sr2):
	return math.sqrt(r2**4/(r1+r2)**4*sr1**2+r1**4/(r1+r2)**4*sr2**2)

def sigmaR(i, si, v, sv):
	return math.sqrt(sv**2/i**2+v**2/i**4*si**2)

def sigmaRG(v0, sv0, vab, svab, rc, src):
	return math.sqrt((v0/vab-1)**2*src**2+rc**2/vab**2*sv0**2+rc**2*v0**2/vab**4*svab**2)

def sigmaRG2(i, si, v0, sv0, vab, svab):
	return (1/i)*math.sqrt(sv0**2+svab**2 +((v0-vab)*si/i)**2)

def errperc(misura,  errore):
	return errore/misura*100

ddp = (0.7,  0.002)
cap = (1.9,  2)
res1 = (0.9,  0.2)
res11 = (0.9,  1)
int=(0.75,  0.1)

file = 'potenziometro'
cacca = DatiSperimentali(file, 1, 2)


#def ciao():
#	return 0
print 'Compatibilità:'
a = 135.9
sa = 0.6
b = 135.8
sb = 0.7
print compatib(a, sa, b, sb)
a = 34.
sa = 0.1
b = 34.2
sb = 0.2
print compatib(a, sa, b, sb)
#
#r1 = 68.
#sr1 = 0.4
#r2 = 67.9
#sr2 = 0.4
#
#print """resistenze:""",  sigmaP(r1, r2, sr1, sr2)
##
##c2 = 103.
##sc2 = 1.6
##c3 = 224.
##sc3 = 2.7
###
###print sigmaP(c2, c3, sc2, sc3)
##
#i = 38e-3
#si = 0.4e-3
#v = 2.59
#sv = 0.011
#
#print """resistenze:""", sigmaR(i, si, v, sv)
#
#i = 40e-3
#si = 0.2e-3
#v = 2.717
#sv = 0.011
#
#print """resistenze:""", sigmaR(i, si, v, sv)
#
#i = 45e-3
#si = 0.4e-3
#v = 0.273
#sv = 0.002
#
#print sigmaR(i, si, v, sv)
#
#v0 = 3.098
#sv0 = 0.013
#vab = 2.925
#svab =0.012
#i = 18.13e-3
#si = 0.1e-3
#
#print (v0-vab)/i, sigmaRG2(i, si, v0, sv0, vab, svab)
#
#lrc = [26.3, 51.6, 152.0]
#slrc = [0.2, 0.3, 0.8]
#v0 = 3.095
#sv0 = 0.013
#vab = [2.292, 2.674, 2.915]
#svab = [0.009, 0.011, 0.012]
#
#for i in range(len(lrc)):
#	print lrc[i]*(v0/vab[i]-1)
#	print sigmaRG(v0, sv0, vab[i], svab[i], lrc[i], slrc[i])
#
##misureres=[68.0, 67.9, 464.9, 33.3, 503.7, 504.0, 135.8, 34.2, 26.3, 51.6, 76.0, 101.5, 127.0, 152., 177.3, 202.4, 227.7, 252.8]
##
##print """misure resistenza:"""
##for misura in misureres:
##	print """%.1f %.1f %.1f""" %(misura,  delta(misura, res1),  sigma(misura, res1))
##
##misurecap=[1., 103., 224., 71., 324.]
##print """misure capacità:"""
##for misura in misurecap:
##	print """%.1f %.1f %.1f""" %(misura,  delta(misura, cap),  sigma(misura, cap))
##
#misureddp =[2.292,2.674,2.915, 3.108, 2.037, 1.931, 1.776, 1.619, 1.494, 1.352, 2.590, 2.443, 2.307, 2.168, 2.717, 2.603, 2.449, 2.309, 2.175, 2.039, 1.906, 1.774, 1.636, 1.497, 3.098, 2.925,0.273]
#print """misure ddp:"""
#for misura in misureddp:
#	print """%.3f %.3f""" %(misura,  sigma(misura, ddp))
##
##misureint =[40.0, 38.3, 36., 34., 32., 30., 28., 26.1, 24., 22., 18.13]
##print """misure intensità corrente:"""
##for misura in misureint:
##	print """%.1f %.2f""" %(misura,  sigma(misura, int))

perc = [68.1, 67.9, 45., 0.273, 6.07, 3.098, 18.13, 2.925, 9.5,  3.095, 9.2, 8.1, 9.4]
err = [0.8, 0.4, .4, .002, .07, .013, .1, .012, 0.9, .013, .2, .3, .9]

print 'Percentuali:'
for i in range(len(perc)):
	print perc[i],  err[i], errperc(perc[i], err[i])
