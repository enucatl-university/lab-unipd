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

ddp20 = (0.25,  0.01)
ddp2 = (0.25,  0.001)
ddp02 = (0.25,  0.0001)
int = (0.5, 0.001)

#file = ['filo254', 'filo508', 'lung']
#
#a = []
#for f in file:
#	a.append(DatiSperimentali(f, 1))
#
#corr = []
#for f in file:
#	corr.append(DatiSperimentali(f, 0))
#c = corr[0].valori + corr[1].valori+corr[2].valori
#
#b = a[0].valori + a[1].valori+a[2].valori
#for i in range(len(b)):
#	print '%.3f %.3f %.3f' %(c[i], b[i],  sigma(b[i], ddp20))

print '*****************'
f = 'temp'
a =DatiSperimentali(f, 1)
corr = DatiSperimentali(f, 0)
c = corr.valori
b = a.valori
for i in range(len(b)):
	print '%.3f %.4f %.4f' %(c[i], b[i],  sigma(b[i], ddp2))

print '***************************'
f = 'filo1016'
a =DatiSperimentali(f, 1)
corr = DatiSperimentali(f, 0)
c = corr.valori
b = a.valori
for i in range(len(b)):
	print '%.3f %.4f %.4f' %(c[i], b[i],  sigma(b[i], ddp2))

print '***************************'
file = ['filo508', 'filo1016', 'filo254', 'temp']

corr = []
for f in file:
	corr.append(DatiSperimentali(f, 0))
c = corr[0].valori + corr[1].valori+corr[2].valori+corr[3].valori

for i in range(len(c)):
	print '%.3f %.4f' %(c[i], sigma(c[i], int))
