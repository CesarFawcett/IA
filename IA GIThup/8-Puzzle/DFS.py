# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:12:32 2022

@author: CesarFawcett
"""
from collections import deque
import time


#Clase que define un nodo en el 8-puzzle.
class Nodo:
    nexp = 1
    def __init__(self, estado, padre, movimiento, profundidad, piezas_correctas):        
        self.estado = estado                        #Posición atual de las piezas.
        self.padre = padre                          #Nodo desde el que se llega a este nodo.
        self.movimiento = movimiento                #Movimiento para encontrar este nodo desde el padre.
        self.profundidad = profundidad              #Posición del nodo en el árbol de búsqueda.
        self.piezas_correctas = piezas_correctas    #Total de piezas en su lugar para este estado.
    #Método para mover las piezas en direcciones posibles.
    def mover(self, direccion):
        estado = list(self.estado)
        ind = estado.index(0)

        if direccion == "arriba":            
            if ind not in [6, 7, 8]:                
                temp = estado[ind + 3]
                estado[ind + 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "abajo":            
            if ind not in [0, 1, 2]:                
                temp = estado[ind - 3]
                estado[ind - 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "derecha":            
            if ind not in [0, 3, 6]:                
                temp = estado[ind - 1]
                estado[ind - 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "izquierda":            
            if ind not in [2, 5, 8]:                
                temp = estado[ind + 1]
                estado[ind + 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None        

    #Método que encuentra y regresa todos los nodos sucesores del nodo actual.
    def encontrar_sucesores(self):
        sucesores = []
        sucesorU = self.mover("arriba")
        sucesorD = self.mover("abajo")
        sucesorR = self.mover("derecha")
        sucesorL = self.mover("izquierda")
        
        sucesores.append(Nodo(sucesorU, self, "arriba", self.profundidad + 1, calcular_heurisitica(sucesorU)))
        sucesores.append(Nodo(sucesorD, self, "abajo", self.profundidad + 1, calcular_heurisitica(sucesorD)))
        sucesores.append(Nodo(sucesorR, self, "derecha", self.profundidad + 1, calcular_heurisitica(sucesorR)))
        sucesores.append(Nodo(sucesorL, self, "izquierda", self.profundidad + 1, calcular_heurisitica(sucesorL)))
        
        sucesores = [nodo for nodo in sucesores if nodo.estado != None]  
        return sucesores

    #Método que encuentra el camino desde el nodo inicial hasta el actual.
    def encontrar_camino(self, inicial):
        camino = []
        nodo_actual = self
        while nodo_actual.profundidad >= 1:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        
        return camino

    #Método que imprime ordenadamente el estado (piezas) de un nodo.
    def imprimir_nodo(self):
        renglon = 0
        for pieza in self.estado:
            if pieza == 0:
                print(" ", end = " ")
            else:
                print (pieza, end = " ")
            renglon += 1
            if renglon == 3:
                print()
                renglon = 0       

#Función que calcula la cantidad de piezas que están en su lugar para un estado dado.
def calcular_heurisitica(estado):
    correcto = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    valor_correcto = 0
    piezas_correctas = 0
    if estado:
        for valor_pieza, valor_correcto in zip(estado, correcto):
            if valor_pieza == valor_correcto:
                piezas_correctas += 1
            valor_correcto += 1
    return piezas_correctas   

#Algoritmo Primero Elmejor.
def dfs(inicial, meta, profundidad_max):
    nexp = 1
    visitados = set()   #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    frontera = deque()  #Pila de nodos aún por explorar. Se agrega el nodo inicial.
    frontera.append(Nodo(inicial, None, None, 0, calcular_heurisitica(inicial)))
    
    while frontera:                         #Mientras haya nodos por explorar:
        nodo = frontera.pop()               #Se toma el primer nodo de la pila.

        if nodo.estado not in visitados:    #Si no se había visitado, 
            visitados.add(nodo.estado)      #se agrega al conjunto de visitados.
            nexp = nexp +1
        else:                               #Si ya se visitó,
            continue                        #se ignora.
        
        if nodo.estado == meta:             #Si es una meta, se regresa el camino para llegar a él y termina el algoritmo.
           print("°°°°°¡Se encontró la Solucion!°°°°°°")
           print("total de nodos : ",nexp)           
           return nodo.encontrar_camino(inicial)
        else:                               #Si no es una meta:             
            if profundidad_max > 0:                             #Si se estableció una búsqueda con profundidad limitada
                if nodo.profundidad < profundidad_max:          #y no se ha llegado al límite,                 
                    frontera.extend(nodo.encontrar_sucesores()) #se agregan los sucesores a los nodos por explorar.
            else:                                               #Si no se estableció una búsqueda con profundidad limitada,
                frontera.extend(nodo.encontrar_sucesores())     #se agregan los sucesores a los nodos por explorar.


#Función main.
def main():
    inicio = time.time()
    estado_final = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    estado_inicial =(1, 2, 3, 4, 5, 0, 7, 8, 6) #1 movimiento.
    #estado_inicial = (1, 0, 3, 4, 2, 5, 7, 8, 6)   #3 movimientos.

    #Menú principal
    print("8-puzzle\n")
    print("El estado inicial del juego es: ")
    print("Corriendo DFS . Por favor espere.")
    print("\n¿Establecer un límite de profundidad?")
    print("Escriba el límite como un entero mayor que 0")
    print("o el numero 0 para continuar sin límite.")
    profundidad_max = int(input("Profundidad: "))
    print("Corriendo DFS. Por favor espere.")
    nodos_camino = dfs(estado_inicial, estado_final, profundidad_max)
        
    #Se imprime el camino si existe 
    if nodos_camino:
        print("\nEstado inicial:")
        (Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial))).imprimir_nodo()
        
        for nodo in nodos_camino:
          print("\nSiguiente movimiento:", nodo.movimiento)
          print("Estado actual:")
          nodo.imprimir_nodo()  
    else:
        print ("\nNo se encontró un camino con las condiciones dadas.")
    
    fin = time.time()
    print("Tiempo de ejecucion :",fin-inicio)
    print("Numero de pasos a la solucion : ",len(nodos_camino))
    return 0    
     
if __name__ == "__main__":
    main()

