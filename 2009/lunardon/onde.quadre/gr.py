#!/usr/bin/env python
#coding=utf-8

from os import listdir
from re import *
import scriptutil as SU

def dotsize():
	SU.freplace('.', shellglobs=('*.tex',), namefs=(lambda s: '.svn' not in s,), regexl=(('dotsize=.01', 'dotsize=.08', None),))

l = listdir('./')
for file in l:
	if 'tex' in file:
		nome = file.split('.tex')[0]
		print """
\\begin{figure}[p]\caption{Grafico.}
\centering
\include{%s}
\end{figure}""" %nome
dotsize()
