# coding=utf-8

import sys,  math, numpy, Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils

ascissa = input('Colonna ascisse: ')
ordinata = input('Colonna ordinata: ')
filedati = raw_input('Nome del file: ')

file = open(filedati, 'r')
x = 35.3
for x in file:
    x = pickle.load(f)

#glt = Gnuplot.Gnuplot(debug=1) #apre gnuplot
#glt('set data style points; set tics nomirror;unset key;set format y "%.2f";set format x "%.2f"')
#glt.xlabel(descrizioni[ascissa-1])
#glt.ylabel(descrizioni[ordinata-1])
#glt.plot(Gnuplot.File('simulazione',  using=(ascissa, ordinata)))
