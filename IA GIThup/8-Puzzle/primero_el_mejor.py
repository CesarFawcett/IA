# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:12:32 2022

@author: CesarFawcett
"""

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
def PrimeroM(inicial):
    nexp = 1
    visitados = set()  #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    nodo_actual = Nodo(inicial, None, None, 0, calcular_heurisitica(inicial))

    while nodo_actual.piezas_correctas < 9:             #Mientras el estado actual no tenga todas las piezas en su lugar:
        nexp = nexp +1
        sucesores = nodo_actual.encontrar_sucesores()   #Se buscan los sucesores del estado actual
        max_piezas_correctas = -1

        #Para cada nodo en los sucesores, se busca el que tenga más piezas en su lugar.
        for nodo in sucesores:   
            if nodo.piezas_correctas >= max_piezas_correctas and nodo not in visitados:
                max_piezas_correctas = nodo.piezas_correctas
                nodo_siguiente = nodo

            visitados.add(nodo_actual)

        #Si el nodo encontrado tiene más piezas en su lugar que el nodo actual, 
        #se asigna como nodo actual para repetir la búsqueda sobre éste.
        if nodo_siguiente.piezas_correctas >= nodo_actual.piezas_correctas:
            nodo_actual = nodo_siguiente
        #Si no, significa que se llegó a un máximo local y el algoritmo no debe seguir.
        else:
            print("\nSe llegó a un máximo local. No se encontró la meta.")
            break
    else:
        print("°°°°°¡Se encontró la Solucion!°°°°°°")
        print("total de nodos : ",nexp)        
    return nodo_actual.encontrar_camino(inicial)

#Función main.
def main():
    inicio = time.time()
    #estado_inicial =(1, 2, 3, 4, 5, 0, 7, 8, 6) #1 movimiento.
    #estado_inicial = (1, 0, 3, 4, 2, 5, 7, 8, 6)   #3 movimientos.
    estado_inicial = (1,2,3,4,5,0,6,7,8)   #13 movimientos.

    #Menú principal
    print("8-puzzle\n")
    print("El estado inicial del juego es: ")
    print("Corriendo PRIMERO EL MEJOR . Por favor espere.")
    nodos_camino = PrimeroM(estado_inicial)
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

