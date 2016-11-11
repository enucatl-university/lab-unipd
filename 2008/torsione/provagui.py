# coding=utf-8

import ds
from myGui import *

app = QtGui.QApplication([]) # Crea un'applicazione Qt, ...
Window = QtGui.QMainWindow() # ... una finestra, ...
ui = Ui_MainWindow() # ... e una user interface.
ui.setupUi(Window) # Infila la finestra nella user interface

def leggi():
        nomifile = ui.lineEdit.text()
        val = ui.spinValori.value()
        err = ui.spinValori.value()
        dati = ds.TanteSerie(nomifile, val-1, err-1)
        return dati

def vedimedia():
        dati = leggi()
        (medie,  rms, stdev,  errmed) = ([], [], [], [])
        ui.textBrowser.setText('#    media     rms     stdev')
        for i in range(len(dati.serie)):
                medie.append(dati.serie[i].calcmedia())
                rms.append(dati.serie[i].calcrms())
                stdev.append(dati.serie[i].calcstdev())
                errmed.append(dati.serie[i].calcerrmedia())
                ui.textBrowser.append('%-i %7g %7g %7g %7g' %(i, medie[i], rms[i], stdev[i],  errmed[i]))
        
#def vedimedia():
#        dati = leggi()
#        ui.textBrowser.setText('Interpolazione lineare')
#        for i in range(len(dati.serie)):
#                ui.textBrowser.append("""Intercetta = %g \\pm %g
#Pendenza = %g \\pm %g""" %dati.serie[i][val-1].interpolazionelineare(dati.serie[i][err-1]))
        
app.connect(ui.Bmedia,QtCore.SIGNAL("clicked()"),vedimedia)

def run():
        Window.show() # mostra il dialog precedentemente creato
        return app.exec_() # esegue l'applicazione ed esce dal
        #programma ritornando lo stesso intero che ritorna app.exec_()

if __name__ == "__main__":
        run()
