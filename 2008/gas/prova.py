import math, rpy

def leggivalori(file, colonna):
        for line in file.readlines():
                yield float(line.split()[colonna])


class DatiSperimentali(list):
        """Gli oggetti di questa classe sono pensati come serie
        di osservazioni di una grandezza fisica.
        Gli attributi sono quindi self.valori e self.errori
        che sono due liste.
        I metodi hanno nome calc+nomeattributocorrispondente"""
        def __init__(self, file, colonnavalori=0, colonnaerrori=1, *args):
                super(DatiSperimentali, self).__init__(self, *args)
                self.assegnavalori(file, colonnavalori, colonnaerrori)
                
        def assegnavalori(self, file, colonnavalori, colonnaerrori):
                self.valori = list(leggivalori(file, colonnavalori))
                self.errori = list(leggivalori(file, colonnaerrori))
                
        def calcmedia(self):
                media = 0.
                for valore in self.valori:
                        media += valore
                n = float(len(self.valori))
                self.media = media/n
                return self.media
                
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
                self.stdev = math.sqrt(n/(n-1))
                return self.stdev
                
        def calcmediap(self):
                numeratore, denominatore = 0.
                for i in range(len(self.valori)):
                        numeratore   += self.valori[i]/self.errori[i]**2
                        denominatore += self.errori[i]**(-2)
                self.mediapesata = numeratore/denominatore
                return self.mediapesata
        
        def calcerrmediap(self):
                denominatore = 0.
                for errore in self.errori:
                        denominatore += self.errori**(-2)
                self.erroremediapesata = denominatore**(-0.5)
                return self.erroremediapesata
        
        def interpolazionelineare(self, other):
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
        
        def calcmassimo(self):
                massimo = self.valori[0]
                for valore in self.valori:
                        if massimo < valore: massimo = valore
                self.massimo = massimo
                return self.massimo
        
        def calcminimo(self):
                minimo = self.valori[0]
                for valore in self.valori:
                        if minimo > valore: massimo = valore
                self.minimo = minimo
                return self.minimo
f = open('0c')
pv = DatiSperimentali(f)
print pv.calcmedia(),  pv.calcstdev()
