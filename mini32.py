# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 14:30:14 2015

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
    
def FirstOccurrence(vector, val):
    
    for i in range(len(vector)):
        if vector[i] == val:
            return i
    return -1
    

#inicializacion
server = 1
serversA = []#hora de atencion
serversD = []#hora de salida
for i in range(server):
    serversA.append([])#servers cola
    serversD.append([])
    
t = 0
Na = 0
Nd = 0
n = 0
ta = ProcPoi(0)#primer tiempo de llegada
td = [maxint]*server#vector td con cantidad de servidores
tdindex = [0]*server#vector con indices
#td = maxint#maximo entero posible
T = 60#tiempo limite
A = []#inicio atencion
D = []#final atencion
constante = 0
while t <= T or n > 0:
    #print "ta:"+str(ta)+" td:"+str(td)+" t:"+str(t)+" n:"+str(n)
    #raw_input("Inicio")
    if ta <= min(td) and ta <=T:
        #ingreso es menor que el menor de los servidores
        t = ta
        Na += 1
        n += 1
        ta = ProcPoi(t)#nuevo tiempo de llegada
        
        #servidore(s) estaban vacios y ahora hay uno nuevo
        if FirstOccurrence(td,maxint) != -1:
            #primer servidor atiende uno nuevo
            tempindex = FirstOccurrence(td,maxint)
            td[tempindex] = t + Exponencial(1)
            tdindex[tempindex] = Na#se guarda el numero de cliente
            #n += -1#ya se quito de la cola
            
        A.append(t)
        D.append(0.0)#se crea espacio para el siguiente
    elif min(td) < ta and min(td) <= T:
        #el menor de los servidores es antes que nuevo ingreso
        t = min(td)
        
        Nd += 1
        
        tempindex = FirstOccurrence(td,min(td))
        D[tdindex[tempindex]-1] = t
        
        if n <= len(td):#se queda vacio 
            td[tempindex] = maxint
        else:
            #aun hay en cola, entonces nuevo tiempo
            td[tempindex] = t + Exponencial(1)
            tdindex[tempindex] = max(tdindex)+1
        
        n += -1
        
    elif min(ta,min(td)) > T and n > 0:
        t = min(td)
        
        Nd += 1
        
        tempindex = FirstOccurrence(td,min(td))
        D[tdindex[tempindex]-1] = t
        
        if n <= len(td):#se queda vacio 
            td[tempindex] = maxint
        else:
            #aun hay en cola, entonces nuevo tiempo
            td[tempindex] = t + Exponencial(1)
            tdindex[tempindex] = max(tdindex)+1
        n += -1  
        
    elif min(ta,min(td)) > T and n == 0:
        break
        #n=0
    #print "td:"+str(min(td))+" ta:"+str(ta)+" n:"+str(n)+" t:"+str(t)
  
Tp = max(t - T, 0)#tiempo activo del servidor despues de cierre

if Tp == 0:
    print max(D)

inactivo = 0#tiempo que no atendio solicitudes
for i in range(1, min(len(A),len(D))):
    if A[i]>D[i-1]:#si el tiempo de llegada es mayor que la ultima salida
        inactivo += A[i]-D[i-1]

activo = D[len(D)-1]-inactivo#tiempo que atendio solicitudes
        
promedio = sum(D[i]-A[i] for i in range(len(A)))/len(A)#promedio de atencion (t)




#------------GENERICO----------