# coding=utf-8

import sys,  math, rpy, time
import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils

R = 8.3136 #costante dei gas
zeroassoluto = (-273.15, 0.01)

#FUNZIONI:
def legginumeri(nome, colonne):
    file = open(nome, 'r')
    righe = file.readlines()
    file.close()
    x = [0]*len(righe)
    y = [0]*len(righe)
    for i in range(len(righe)):
        num =righe[i].split() #crea una lista con i numeri in riga
        x[i]=float(num[colonne[0]-1]) #salva la colonna "ascissa" nella lista x e la colonna "ordinata" nella lista y
        y[i]=float(num[colonne[1]-1])
    return (x, y)

    #calcola la media pesata di una successione di dati (lista o upla) così disposta: dato errore dato errore ... dato errore
def mediapesata(upla):
    (numeratore, denominatore) = (0., 0.)
    lunghezza = int(math.floor(len(upla)/2))
    for i in range(lunghezza):
        numeratore += upla[2*i]/upla[2*i+1]**2
        denominatore+= upla[2*i+1]**(-2)
    return (numeratore/denominatore, denominatore**(-0.5))

def interpolazionelineare(x, y):
    rpy.set_default_mode(rpy.NO_CONVERSION) #serve per l'ultima parte in R
    linear_model = rpy.r.lm(rpy.r("y ~ x"), data = rpy.r.data_frame(x=x, y=y))
    rpy.set_default_mode(rpy.BASIC_CONVERSION)
    summary = rpy.r.summary(linear_model)
    #pendenza,errpendenza,intercetta,errintercetta
    risultati = (summary['coefficients'][0][0], \
                    summary['coefficients'][0][1], \
                    summary['coefficients'][1][0], \
                    summary['coefficients'][1][1])
    return risultati

def trovamassimo(upla):
    massimo = upla[0]
    for i in range(len(upla)):
        if massimo < upla[i]: massimo = upla[i]
    return massimo

def grafico(nomefile,colonne=(1, 2),etichetteassi=('x', 'y'), cifredecimali=('.g', '.g')):
    decimali=('"%'+cifredecimali[0]+'"','"%'+ cifredecimali[1]+'"')
    (x, y) = legginumeri(nomefile, colonne)
    parametri = interpolazionelineare(x, y)
    f = Gnuplot.Func('%.14f*x%+.14f' %(parametri[2], parametri[0]))
    glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
    glt('set tics nomirror;unset key;set format x %s;set format y %s' %decimali)
    glt.xlabel(etichetteassi[0])
    glt.ylabel(etichetteassi[1])
    glt.plot(Gnuplot.File(nomefile,  using=colonne), f)
#    time.sleep(10)
    
def graficoPST(nomefile,colonne=(1, 2),etichetteassi=('x', 'y'), cifredecimali=('.g', '.g')):
    glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
    glt('set terminal pstricks; set output %s' %('"' + nomefile+'.tex"'))
    decimali=('"%'+cifredecimali[0]+'"','"%'+ cifredecimali[1]+'"')
    (x, y) = legginumeri(nomefile, colonne)
    parametri = interpolazionelineare(x, y)
    f = Gnuplot.Func('%.14f*x%+.14f' %(parametri[2], parametri[0]))
    #glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
    glt('set tics nomirror;unset key;set format x %s;set format y %s' %decimali)
    glt('set xlabel %s; set ylabel %s' %etichetteassi)
    glt.plot(Gnuplot.File(nomefile,  every=10, using=colonne), f)
    glt('set output')

stringanomi = raw_input('Inserisci i nomi dei file da analizzare, separati da spazi: ')
ascissa = input('Colonna ascisse: ')
ordinata = input('Colonna ordinata: ')
colonne = (ascissa, ordinata)
print '\n'
filedati = stringanomi.split() #separa i nomi dei file
risultati = []
for file in filedati:
    (x, y)=legginumeri(file, colonne)
    #graficoPST(file, colonne, ('\"$1/P\\\ (\\\unit{Pa^{-1}})$\"', '\"$V\\\ (\\\unit{cm^3})$\"'), ('.0s', '.0s'))
    risultati.append(interpolazionelineare(x, y))
    del x, y #saranno riutilizzati in seguito
    #stampa i risultati in formato LaTeX-friendly
    
def graficoPST(nomefile,colonne=(1, 2),etichetteassi=('x', 'y'), cifredecimali=('.g', '.g')):
    glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
    glt('set terminal pstricks; set output %s' %('"' + nomefile+'.tex"'))
    decimali=('"%'+cifredecimali[0]+'"','"%'+ cifredecimali[1]+'"')
    (x, y) = legginumeri(nomefile, colonne)
    parametri = interpolazionelineare(x, y)
    f = Gnuplot.Func('%.14f*x%+.14f' %(parametri[2], parametri[0]))
    #glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
    glt('set tics nomirror;unset key;set format x %s;set format y %s' %decimali)
    glt('set xlabel %s; set ylabel %s' %etichetteassi)
    glt.plot(Gnuplot.File(nomefile, using=colonne), f)
    glt('set output')

for i in range(len(filedati)):
        print '%5s & % .4f & % .4f & % .5f & % .5f\\\\' %(filedati[i], risultati[i][0]*10**6, risultati[i][1]*10**6, risultati[i][2], risultati[i][3])
print '%5s & %7s & %7s & %8s & %8s \n\n' %('Temp', '$V_0$', '$\\sigma_{V_0}$', '$PV$', '$\\sigma_{PV}$')
pendenze =  []
intercette =  []
medie =  []
lunghezza = int(math.floor(len(risultati)/2))
for i in range(lunghezza):
    intercette.append((risultati[2*i][0], \
                     risultati[2*i][1], \
                     risultati[2*i+1][0],
                     risultati[2*i+1][1]))
    pendenze.append((risultati[2*i][2], \
                     risultati[2*i][3], \
                     risultati[2*i+1][2],
                     risultati[2*i+1][3]))
for i in range(lunghezza):
    medie.append((mediapesata(intercette[i]), mediapesata(pendenze[i])))
    print '%5s & % .4f & % .4f & % .5f & % .5f\\\\' %(filedati[2*i], medie[i][0][0]*10**6, medie[i][0][1]*10**6, medie[i][1][0], medie[i][1][1])
print '%5s & %7s & %7s & %8s & %8s (medie pesate)\n\n' %('Temp', '$V_0$', '$\\sigma_{V_0}$', '$PV$', '$\\sigma_{PV}$')
file = open('tempmedie', 'r')
scrivi = open('t-pv', 'w')
lines = file.readlines()
file.close()
stringa = ''
for i in range(len(lines)):
    stringa += str(medie[i][1][0]) +' '+ str(lines[i])
scrivi.write(stringa)
scrivi.close()
#graficoPST('t-pv', etichetteassi=('\"nRT\\\ (\\\unit{J})\"','\"$T\\\ (\\\unit{\\\celsius})$\"'), cifredecimali=('.2f', '.0f'))
(x, y)=legginumeri('t-pv', colonne)
#temperatura assoluta con errore, numero di moli con errore
ten = interpolazionelineare(x, y)
print '% .1f & % .1f & % .6f & % .6f\\\\' %ten
print '%7s & %7s & %8s & %8s\n\n' %('$T_0$', '$\\sigma_{T_0}$', '$1/nR$', '$\\sigma_{1/nR}$')
#trova veramente il numero di moli n = 1/beta R
ten2 = [ten[0], ten[1],1/R/ten[2],ten[3]/R/ten[2]**2]
ten = tuple(ten2)
print '% .1f & % .1f & % .6f & % .6f\\\\' %ten
print '%7s & %7s & %8s & %8s\n\n' %('$T_0$', '$\\sigma_{T_0}$', '$n$', '$\\sigma_{n}$')
print 'compatibilità zero assoluto = %.2f\n\n' %(abs(ten[0]-zeroassoluto[0])/math.sqrt(ten[1]**2+zeroassoluto[1]**2))
del x, y, stringa
pressioniminime=[]
#ESPANSIONE:
for i in range(len(filedati)):
    (x, y)=legginumeri(filedati[i], colonne)
    pressioniminime.append(1/trovamassimo(x))
#print pressioniminime
file = open('tempmedie', 'r')
filescrittura = 't-pminesp'
scrivi = open(filescrittura, 'w')
lines = file.readlines()
file.close()
stringa = ''
for i in range(len(lines)):
    stringa +=  str(pressioniminime[2*i])+' '+ lines[i]
scrivi.write(stringa)
scrivi.close()
#graficoPST(filescrittura, (2, 1), ('\"T\\\ (\\\unit{\\\celsius})\"', '\"$P_{min}\\\ (\\\unit{kPa})$\"'), ('.0f', '.0s'))
(y, x)=legginumeri('t-pminesp', colonne)
#Pmin con errore, PT con errore
eefesp = interpolazionelineare(x, y)
#COMPRESSIONE:
file = open('tempmedie', 'r')
filescrittura = 't-pmincomp'
scrivi = open(filescrittura, 'w')
lines = file.readlines()
file.close()
stringa = ''
for i in range(len(lines)):
    stringa +=  str(pressioniminime[2*i+1])+' '+ lines[i]
scrivi.write(stringa)
scrivi.close()
#graficoPST(filescrittura, (2, 1), ('\"T\\\ (\\\unit{\\\celsius})\"', '\"$P_{min}\\\ (\\\unit{kPa})$\"'), ('.0f', '.0s'))
(y, x)=legginumeri(filescrittura, colonne)
eefcomp = interpolazionelineare(x, y)
print 'compressione: $nR/V_max = %.1f \\pm %.1f$' %(eefcomp[2], eefcomp[3])
print 'espansione:  $nR/V_max = %.1f \\pm %.1f$' %(eefesp[2], eefesp[3])
vmax = (ten[2]*R/eefcomp[2], ten[2]*R/eefcomp[2]*math.sqrt((ten[3]/ten[2])**2+(eefcomp[3]/eefcomp[2])**2), ten[2]*R/eefesp[2],ten[2]*R/eefesp[2]*math.sqrt((ten[3]/ten[2])**2+(eefesp[3]/eefesp[2])**2))
vmaxcm = (vmax[0]*10**6, vmax[1]*10**6, vmax[2]*10**6, vmax[3]*10**6) #unità in cm3
print """
VOLUME MASSIMO
compressione: %.2f \\pm %.2f
espansione:   %.2f \\pm %.2f""" %vmaxcm
print 'media pesata: %.2f \\pm %.2f\n\n' %mediapesata(vmaxcm)
