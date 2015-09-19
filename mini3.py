# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 23:32:24 2015

@author: Kevin
"""
from random import random
from math import log
from sys import maxint
#generador de tiempos de ocurrencia
def gent (s):
    lambdaG = 1#lambda de proceso
    returnG = s-(1.0/lambdaG)*log(random())
    return returnG

#inicializacion

t = 0
Na = 0
Nd = 0
n = 0
ta = gent(0)
td = maxint#maximo entero posible
T = 60#tiempo limite
A = []
D = []
while t <= T:
    if ta <= td and ta <=T:
        t = ta
        Na += 1
        n += 1
        ta = gent(t)
        if n == 1:
            #--------ERROR
            td = t + gent(0)#cambiar por tiempo de servicio
            #----------
        A.append(t)
    elif td < ta and td <= T:
        t = td
        n += -1
        Nd += 1
        if n == 0:
            td = maxint
        else:
            #--------ERROR
            td = t + gent(0)#cambiar por tiempo de servicio
            #----------
        D.append(t)
    elif min(ta,td) > T and n > 0:
        t = td
        n += -1
        Nd += 1
        if n > 0:
            #--------ERROR
            td = t + gent(0)#cambiar por tiempo de servicio
            #----------
        D.append(t)
    elif min(ta,td) > T and n == 0:
        n = 0
Tp = max(t - T, 0)