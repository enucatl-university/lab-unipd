# coding=utf-8

from ds import *

def trovagamma(file, grafici='n'):
        smorz = DatiSperimentali(file, 2, 2)
        tempi1 = DatiSperimentali(file, 0, 0)
        tempi2 = DatiSperimentali(file, 0, 0)
#        if grafici != 'n':
#                tempi1.grafico(smorz,\
#                        terminal='postscript', output=str(file)+'.eps', \
#                        cifre=('"%.0f"', '"%.1f"'),\
#                        etichetteassi=('Tempo (s)', 'Posizione (giri)'))
        smorz.slice(fine=800)
        #trova massimi e minimi:
        max = DatiSperimentali((list(massimi(smorz.valori)), ), 0, 0)
        min = DatiSperimentali((list(minimi(smorz.valori)), ))
        max.converti(1/(2*math.pi))
        min.converti(1/(2*math.pi))
        max = max.logaritmo()
        min = min.logaritmo()
        #indici e tempi a cui corrispondono massimi e minimi
        indmax = list(indmassimi(smorz.valori)) 
        indmin = list(indminimi(smorz.valori))
        tempi1.scegliind(indmax)
        tempi2.scegliind(indmin)
        if grafici != 'n':
                tempi1.grafico(max, interp=1,\
                        terminal='pstricks', output=('massimi' + str(file)+'.tex'), \
                        cifre=('"%.0f"', '"%.1f"'),\
                        etichetteassi=('Tempo (\\\unit{s})', 'Posizione (\\\unit{giri})'))
                tempi2.grafico(min, interp=1,\
                        terminal='pstricks', output=('minimi' + str(file) +'.tex'), \
                        cifre=('"%.0f"', '"%.1f"'),\
                        etichetteassi=('Tempo (\\\unit{s})', 'Posizione (\\\unit{giri})'))
        a = tempi1.interpolazionelineare(max)
        b = tempi2.interpolazionelineare(min)
        fudge = [[a[0], b[0]], [a[1], b[1]], [a[2], b[2]], [a[3], b[3]]]
        gamma = DatiSperimentali(fudge, 2, 3)
        print 'compatibilità: ', compatib(a[2], a[3], b[2], b[3])
        #print a[2], a[3], b[2], b[3]
        return gamma

def trovaG(M, l, r, R, omega0):
        G = [0, 0]
        G[0] = M[0]*l[0]*R[0]**2*omega0[0]**2/(math.pi*r[0]**4)
        G[1] = G[0]*math.sqrt((M[1]/M[0])**2\
                                      +(2*R[1]/R[0])**2\
                                      +(2*omega0[1]/omega0[0])**2\
                                      +(l[1]/l[0])**2\
                                      +(4*r[1]/r[0])**2)
        return G
nomifile = '900 910 920 930 940 950 960 961 962 963 964 965 966 967 968 969 970 971 980 990 1000'
ampiezze = TanteSerie(nomifile, 3, 3)
medie = [[], []]

#COSTANTI
l = (0.75, 0.005) #lunghezza del filo
R = (11.35e-3, 0.1e-3) #raggio del cilindro
M = (115.5e-3, 0.1e-3)  #massa del cilindro
r = (0.2e-3, 0.01e-3)   #raggio del filo


for ser in ampiezze.serie:
        medie[0].append(ser.calcmedia())
        medie[1].append(ser.calcerrmedia())

ff = nomifile.split()
for i in range(len(ff)):
        print '%s & %.7f & %.7f \\\\' %(ff[i], medie[0][i], medie[1][i])
ampmed = DatiSperimentali(medie, 0, 1)
fudge = [nomifile.split(), ]
freq = DatiSperimentali(fudge)
freq.converti(1e-3)
indmax = ampmed.valori.index(max(ampmed.valori))
print """L'ampiezza massima registrata è %.5f ± %.5f giri,
per una frequenza forzante di %.3f Hz""" %(max(ampmed.valori), ampmed.errori[indmax],freq.valori[indmax])
freq.grafico(ampmed,
             terminal='pstricks', output='ampiezza', \
             cifre=('"%.2f"', '"%.1f"'),\
             etichetteassi=('Frequenza forzante (\\\unit{Hz})',\
             'Ampiezza (\\\unit{giri})'))

fudge = [[ampmed.valori[indmax], ampmed.valori[indmax+1]], [ampmed.errori[indmax], ampmed.errori[indmax+1]]]
aR = DatiSperimentali(fudge, 0, 1) #ampiezza di risonanza
fR = (freq.valori[indmax], 0.001/3) #frequenza di risonanza
print 'Ampiezza di risonanza: %.7f \pm %.7f' %(aR.calcmediap(),  aR.calcerrmediap())

file1 = 'smorz'
file2 = 'smorza'
gamma1 = trovagamma(file1, 'n')
gamma2 = trovagamma(file2, 'n')

gamma = gamma1+gamma2

print """gamma %.6f \pm %.6f""" %(-gamma.calcmediap(), gamma.calcerrmediap())
ga = (-gamma.calcmediap(), gamma.calcerrmediap())

omega0 = [0, 0]
f0 = [0, 0]
gsupi = [0, 0]
gsupi[0] = -gamma.calcmediap()/(math.sqrt(2)*math.pi)
gsupi[1] =gamma.calcerrmediap()/(math.sqrt(2)*math.pi)
f0[0] = math.sqrt(fR[0]**2+gsupi[0]**2)
f0[1] = f0[0]**(-1)*math.sqrt((fR[0]*fR[1])**2+(gsupi[0]*gsupi[1])**2)
omega0[0]=2*math.pi*f0[0]
omega0[1]=2*math.pi*f0[1]
print 'freq. propria: %.5f \pm %.5f' %(f0[0], f0[1])
G = trovaG(M, l, r, R, omega0)
print '%.1e \pm %.1e' %(G[0], G[1]) #kg/ms

Q=[0, 0]
Q[0] = omega0[0]/(2*ga[0])
Q[1] = Q[0]*math.sqrt((omega0[1]/omega0[0])**2+(ga[1]/ga[0])**2)
print '%.2f \pm %.2f' %(Q[0], Q[1])
