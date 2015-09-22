# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 23:32:24 2015

@author: Kevin
"""
from random import random
from math import log, exp
from sys import maxint

def Exponencial(lam):
    return -(1/lam)*log(random(),exp(1))

#generador de tiempos de ocurrencia
def ProcPoi (s):
    lambdaG = 1#lambda de proceso
    returnG = s-(1.0/lambdaG)*log(random())
    return returnG

#inicializacion

t = 0
Na = 0
Nd = 0
n = 0
ta = ProcPoi(0)
td = maxint#maximo entero posible
T = 60#tiempo limite
A = []
D = []

while t <= T or n > 0:
    if ta <= td and ta <=T:
        t = ta
        Na += 1
        n += 1
        ta = ProcPoi(t)
        if n == 1:
            #--------ERROR
            td = t + Exponencial(1)#cambiar por tiempo de servicio
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
            td = t + Exponencial(1)#cambiar por tiempo de servicio
            #----------
        D.append(t)
    elif min(ta,td) > T and n > 0:
        t = td
        n += -1
        Nd += 1
        if n > 0:
            #--------ERROR
            td = t + Exponencial(1)#cambiar por tiempo de servicio
            #----------
        D.append(t)
    elif min(ta,td) > T and n == 0:
        n = 0
Tp = max(t - T, 0)#tiempo activo del servidor despues de cierre

inactivo = 0#tiempo que no atendio solicitudes
for i in range(1, min(len(A),len(D))):
    if A[i]>D[i-1]:#si el tiempo de llegada es mayor que la ultima salida
        inactivo += A[i]-D[i-1]

activo = D[len(D)-1]-inactivo#tiempo que atendio solicitudes
        
promedio = sum(D[i]-A[i] for i in range(len(A)))/len(A)#promedio de atencion (t)

