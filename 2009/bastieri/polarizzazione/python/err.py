#coding=utf-8

from math import sqrt

def error(value, *couple):
    square = 0
    for tuple in couple:
        square += tuple[1]**2/tuple[0]**2
    return value*sqrt(square)
