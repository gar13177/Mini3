# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 14:30:14 2015

@author: Kevin
"""

from random import random
from math import log
from sys import maxint

def Exponencial(lam):
    return -(1.0/lam)*log(random())

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
    
def Active( A, D):
    #A es tiempo de llegada
    #D es tiempo de salida
    result = min(A)#se mantiene inactivo hasta la primera llegada
    for i in range(1,len(A)):
        if A[i]>D[i-1]:#paso un tiempo inactivo
            result += A[i]-D[i-1]
    result = max(D)-result#tiempo activo es el ultimo momento de trabajo menos inactivo    
    return result
    
def EnCola( A, D):
    #A es tiempo de llegada
    #D es tiempo de salida
    result = 0#no se mantuvo en cola
    total = 0#cantidad
    for i in range(1,len(A)):
        if A[i]<D[i-1]:#como es menor el de llegada, estuvo en cola
            result += D[i-1]-A[i]#tiempo en cola: tiempo atendido-tiempo llegada
            total += 1
    return result,total
    

#inicializacion
#HOST 1
lam = 100
server = 3

#HOST 2
#lam = 10
#server = 1

lamPoi = 40


serversA = []#hora de atencion
serversD = []#hora de salida
for i in range(server):
    serversA.append([])#cada server tiene su propia cola
    serversD.append([])#cada server tiene su propia cola
    
t = 0
Na = 0
Nd = 0
n = 0
ta = Exponencial(lamPoi)#primer tiempo de llegada
td = [maxint]*server#vector td con cantidad de servidores
tdindex = [0]*server#vector con indices
#td = maxint#maximo entero posible

T = 3600#tiempo limite

A = []#inicio atencion
D = []#final atencion
constante = 0
while t <= T or n > 0:
    
    if ta <= min(td) and ta <=T:
        #ingreso es menor que el menor de los servidores
        t = ta
        Na += 1
        n += 1
        ta = t + Exponencial(lamPoi)#nuevo tiempo de llegada
        
        #servidore(s) estaban vacios y ahora hay uno nuevo
        if FirstOccurrence(td,maxint) != -1:
            #servidor libre atiende inmediatamente
            tempindex = FirstOccurrence(td,maxint)
            td[tempindex] = t + Exponencial(lam)
            tdindex[tempindex] = Na#se guarda el numero de cliente
            
        A.append(t)
        D.append(0.0)#se crea espacio para el siguiente
    elif min(td) < ta and min(td) <= T:
        #el menor de los servidores es antes que nuevo ingreso
        t = min(td)
        
        Nd += 1
        
        tempindex = FirstOccurrence(td,min(td))
        D[tdindex[tempindex]-1] = t#como ya ingreso, se guarda la hora de salida
        
        #tdindex guarda el numero de cliente
        serversA[tempindex].append(A[tdindex[tempindex]-1])
        serversD[tempindex].append(D[tdindex[tempindex]-1])        
        
        if n <= len(td):#se queda vacio 
            td[tempindex] = maxint
        else:
            #aun hay en cola, entonces nuevo tiempo
            td[tempindex] = t + Exponencial(lam)
            tdindex[tempindex] = max(tdindex)+1
        
        n += -1
        
    elif min(ta,min(td)) > T and n > 0:
        t = min(td)
        
        Nd += 1
        
        tempindex = FirstOccurrence(td,min(td))
        D[tdindex[tempindex]-1] = t
        
        #tdindex guarda el numero de cliente
        serversA[tempindex].append(A[tdindex[tempindex]-1])
        serversD[tempindex].append(D[tdindex[tempindex]-1]) 
        
        if n <= len(td):#se queda vacio 
            td[tempindex] = maxint
        else:
            #aun hay en cola, entonces nuevo tiempo
            td[tempindex] = t + Exponencial(lam)
            tdindex[tempindex] = max(tdindex)+1
        n += -1  
        
    elif min(ta,min(td)) > T and n == 0:
        break#no tiene sentido continuar

    #print "td:"+str(min(td))+" ta:"+str(ta)+" n:"+str(n)+" t:"+str(t)
  
Tp = max(t - T, 0)#tiempo activo del servidor despues de cierre

if Tp == 0:
    print max(D)


#estadisticas por servidor
serversStats = []#estadisticas de todos los servidores
for k in range(len(serversA)):
    #i guarda el indice del servidor
    stats = []
    stats.append(len(serversA[k]))#cantidad atendida
    if stats[0]!=0:
        stats.append(Active(serversA[k], serversD[k]))#tiempo activo
        stats.append(max(max(serversD[k]),T)-stats[-1])#tiempo inactivo = ultimo tiempo-tiempo activo
        t1,t2 = EnCola(serversA[k], serversD[k])
        stats.append(t1)#tiempo que hicieron cola
        stats.append(t2)#cantidad que hizo cola
        stats.append(float(stats[-4])/len(serversA[k]))#tiempo promedio
        stats.append(max(max(serversD[k])-T,0))#tiempo activo despues de cierre
    else:
        stats.append(0)
        stats.append(0)
        stats.append(0)
        stats.append(0)
        stats.append(0)
        stats.append(0)
    
    serversStats.append(stats)
        
promedio = sum(D[i]-A[i] for i in range(len(A)))/len(A)#promedio de atencion (t)




#------------GENERICO----------