# coding=utf-8

import sys,  math, Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils, rpy

ascissa = 1
ascissa -=1
ordinata = 2
ordinata -=1
filedati = raw_input('Nome file: ')
interpolazioni = [0]*12
rpy.set_default_mode(rpy.NO_CONVERSION)

file = open(filedati, 'r')
lines = file.readlines()
x = [0]*len(lines)
y = [0]*len(lines)
for i in range(len(lines)):
    num =lines[i].split('\t')
    x[i]=float(num[ascissa])
    y[i]=float(num[ordinata])
linear_model = rpy.r.lm(rpy.r("y ~ x"), data = rpy.r.data_frame(x=x, y=y))
print type(linear_model)
rpy.set_default_mode(rpy.BASIC_CONVERSION)
linear_model.as_py()['coefficients']
summary = rpy.r.summary(linear_model)
print """Intercetta: %g ± %g
Coefficiente angolare: %g ± %g
""" % (summary['coefficients'][0][0], summary['coefficients'][0][1], summary['coefficients'][1][0], summary['coefficients'][1][1])
