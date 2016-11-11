# coding=utf-8

"""DatiSperimentali: strumenti per analisi dati di base.
author: Matteo Abis, 05/2008
author_email: webmaster@latinblog.org
url: www.latinblog.org"""

import sys, math, time, rpy, Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils

def compatib(a, sigmaa, b, sigmab):
        return abs(a-b)/math.sqrt(sigmaa**2+sigmab**2)

def ritornaindice(lista, listaindici):
        for indice in listaindici:
                yield lista[indice]

def massimi(lista):
        for i in range(1, len(lista)-1):
                if lista[i] > lista [i-1] and lista[i] > lista[i+1]:
                        yield abs(lista[i])

def minimi(lista):
        for i in range(1, len(lista)-1):
                if lista[i] < lista [i-1] and lista[i] < lista[i+1]:
                        yield abs(lista[i])
                        
def indmassimi(lista):
        for i in range(1, len(lista)-1):
                if lista[i] > lista [i-1] and lista[i] > lista[i+1]:
                        yield i

def indminimi(lista):
        for i in range(1, len(lista)-1):
                if lista[i] < lista [i-1] and lista[i] < lista[i+1]:
                        yield i

def leggivalori(file, colonna):
        #se file legge dal file
        try:
                f = open(file)
                for line in f.readlines():
                        yield float(line.split()[colonna])
        #se lista/upla/dizionario legge la componente "colonna"
        except TypeError:
                try:
                        for elem in file[colonna]:
                                yield float(elem)
                except TypeError:
                        for elem in file:
                                yield elem
        except IOError:
                print 'File non trovato!'
                
def scrivivalori(elenchi, nome):
        """elenchi è una tupla/lista di tuple/liste (le colonne del file)
        che contengono i dati da trascrivere."""
        file = open(nome, 'w')
        numcolonne = len(elenchi)
        stringa = ''
        for i in range(len(elenchi[0])):
                try:
                        for j in range(numcolonne):
                                stringa += str(elenchi[j][i]) + ' '
                        stringa += '\n'
                        file.write(stringa)
                except IndexError: break
        file.close()
        
def test(elemento):
        """Funzione da modificare a scelta per scegliere dei parametri"""
        return True

def chiudigrafico():
        """funzione per non chiudere immediatamente i grafici dopo il disegno"""
        raw_input('Premi invio per chiudere il grafico...')

class DatiSperimentali(list):
        """Gli oggetti di questa classe sono pensati come serie
        di osservazioni di una grandezza fisica.
        Gli attributi sono quindi self.valori e self.errori
        che sono due liste.
        I metodi hanno in generale nome calc+nomeattributocorrispondente"""
        def __init__(self, file, colonnavalori=0, colonnaerrori=0, *args):
                """il parametro 'file' può essere il nome di un file """
                super(DatiSperimentali, self).__init__(self, *args)
                self.assegnavalori(file, colonnavalori, colonnaerrori)
                
        def assegnavalori(self, file, colonnavalori, colonnaerrori):
                self.valori = list(leggivalori(file, colonnavalori))
                self.errori = list(leggivalori(file, colonnaerrori))
        
        def sceglivalori(self):
                """Sceglie i valori secondo una funzione 'test' da definire altrove"""
                for i in range(len(self.valori)):
                        if not test(self.valori[i]):
                                del self.valori[i]
                                del self.errori[i]
                                
        def slice(self, inizio=0, fine=10, passo=1):
                self.valori=self.valori[inizio:fine:passo]
                self.errori=self.errori[inizio:fine:passo]
                #return DatiSperimentali((self.valori, self.errori), 0, 1)
                
        def calcmedia(self):
                media = 0.
                for valore in self.valori:
                        media += valore
                n = float(len(self.valori))
                self.media = media/n
                return self.media
                
        def __add__(self, other):
                self.valori += other.valori
                self.errori += other.errori
                return DatiSperimentali((self.valori, self.errori), 0, 1)
                
        def calcrms(self):
                self.calcmedia()
                radicando = 0.
                for valore in self.valori:
                        radicando += (valore-self.media)**2
                n = float(len(self.valori))
                self.rms = math.sqrt(radicando/n)
                return self.rms
                
        def calcstdev(self):
                self.calcrms()
                n = float(len(self.valori))
                self.stdev = math.sqrt(n/(n-1))*self.rms
                return self.stdev
                
        def calcerrmedia(self):
                return self.calcstdev()/len(self.valori)
                
        def calcmediap(self):
                (numeratore, denominatore) = (0., 0.)
                for i in range(len(self.valori)):
                        numeratore   += self.valori[i]/self.errori[i]**2
                        denominatore += self.errori[i]**(-2)
                self.mediapesata = numeratore/denominatore
                return self.mediapesata
        
        def calcerrmediap(self):
                denominatore = 0.
                for errore in self.errori:
                        denominatore += errore**(-2)
                self.erroremediapesata = denominatore**(-0.5)
                return self.erroremediapesata
        
        def interpolazionelineare(self, other):
                """x.interpolazionelineare(y) esegue l'i.l. con x in ascissa e y in ordinata.
                x e y devono essere due oggetti della classe DatiSperimentali."""
                rpy.set_default_mode(rpy.NO_CONVERSION)
                linear_model = rpy.r.lm(rpy.r("y ~ x"), data = rpy.r.data_frame(x=self.valori, y=other.valori))
                rpy.set_default_mode(rpy.BASIC_CONVERSION)
                summary = rpy.r.summary(linear_model)
                #pendenza,errpendenza,intercetta,errintercetta
                risultati = (summary['coefficients'][0][0], \
                            summary['coefficients'][0][1], \
                            summary['coefficients'][1][0], \
                            summary['coefficients'][1][1])
                return risultati
                
        def converti(self, fattore):
                for i in range(len(self.valori)):
                        self.valori[i] *= fattore
                for i in range(len(self.errori)):
                        self.errori[i] *= fattore
        
        def grafico(self, other, \
                    interp='n', \
                    cifre=('"%.0s*10^{%S}"','"%.0s*10^{%S}"'), \
                    terminal='x11', \
                    etichetteassi=('x', 'y'), \
                    output='grafico'):
                glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
                glt('set tics nomirror; unset key; set format x %s; set format y %s' %cifre)
                glt('set terminal %s' %terminal)
                glt('set output "%s"' %output)
                glt.xlabel(etichetteassi[0])
                glt.ylabel(etichetteassi[1])
                nome = 'temp'
                colonne = (1, 2)
                scrivivalori((self.valori, other.valori), nome)
                if interp != 'n':
                        parametri = self.interpolazionelineare(other)
                        f = Gnuplot.Func('%.14f*x%+.14f' %(parametri[2], parametri[0]))
                        glt.plot(Gnuplot.File(nome, using=colonne), f)
                        if terminal == 'x11': chiudigrafico()
                        return
                glt.plot(Gnuplot.File(nome, using=colonne))
                glt('set output')
                if terminal == 'x11': chiudigrafico()
        
        def logaritmo(self):
                n = len(self.valori)
                for i in range(n):
                        self.errori[i]/=self.valori[i]
                        if self.valori[i]>1e-6:
                                self.valori[i]=math.log(self.valori[i])
                        else: self.valori[i]=0
                return DatiSperimentali((self.valori, self.errori), 0, 1)
                        
        def scegliind(self, listaindici):
                self.valori = list(ritornaindice(self.valori, listaindici))
                self.errori = list(ritornaindice(self.errori, listaindici))
                
class TanteSerie(DatiSperimentali):
        """Gli oggetti di questa classe sono pensati come contenitori di più serie di
        osservazioni della stessa grandezza fisica"""
        def __init__(self, file, colonnavalori=0, colonnaerrori=0, *args):
                """il parametro 'file' può essere il nome di un file """
                super(DatiSperimentali, self).__init__(self, *args)
                self.assegnavalori(file, colonnavalori, colonnaerrori)
        
        def assegnavalori(self, file, colonnavalori, colonnaerrori):
                self.serie = []
                nomifile = file.split(' ')
                for i in range(len(nomifile)):
                        a = DatiSperimentali(nomifile[i], colonnavalori, colonnaerrori)
                        self.serie.append(a)
        
