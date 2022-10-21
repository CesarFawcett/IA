import pandas as pd
import numpy as np
<<<<<<< HEAD
=======
import time
import os
archivo = 'Tableros2.xlsx'
>>>>>>> 6aebbbae92492507760e22d0c09a8caf877604d0

archivo = 'Tableros2.xlsx'

def abrir(n):
    hoja = "N=" + str(n)
    tablero = pd.read_excel(archivo, sheet_name=hoja, header=None)
    tablero = tablero.to_numpy()
    pos = list()
    mesa = [[0]*n for i in range(n)]

    for i, v in np.ndenumerate(tablero):
        ls = list(i)
        if(v == 'x' or v == 'X'):
            mesa[ls[0]][ls[1]] = v
            pos.append([ls[0], ls[1]])
    print("pos:", pos)
    #print("pos String:", listatostr(pos))

    return listatostr(pos), generargrafo(pos, mesa, n)

# ArribaIzq, Arriba, ArribaDer, Der, Abajoder, Abajo, AbajoIzq, Izq
sentidoFila = [-1, -1, -1, 0, 1, 1, 1, 0]
sentidoColumna = [-1, 0, 1, 1, 1, 0, -1, -1]


def generargrafo(pos, mesa, n):
    caso = 0
    if os.path.exists("grafo.txt"):
        os.remove("grafo.txt")
    
    file = open("grafo.txt", "a")
    grafo = {}
    visitados = []
    novisitados = [listatostr(pos)]

    reinas = [i for i in range(0, n)]  # Lista de 0 a n
    cantMov = [i for i in range(1, n)]  # Lista de 1 a n-1

    while(novisitados):
        
        # print(novisitados)
        # time.sleep(5)
        pos = novisitados.pop(0)

        posreinasSTR = ""
        for x in strtolista(pos):  # Convierte posreinas de matriz a string
            posreinasSTR = posreinasSTR + str(x[0]) + str(x[1])
        if(pos not in visitados):

            visitados.append(pos)
            novisitados = list(set(novisitados) - set(visitados))

            
            # time.sleep(5)

            pos = strtolista(pos)
            
            for i in reinas:  # Ejecuta por cada reina que exista
                posReina = [pos[i][0], pos[i][1]]  # [x,y] de la reina i
                
                

                # Ejecuta por cada posible movimiento de las reinas
                for f, c in zip(sentidoFila, sentidoColumna):
                    # print("\nRfila: ", f, " RCol: ", c)

                    # Ejecuta por cada posible distancia a mover (de 1 a n-1)
                    for dist in cantMov:
                        # La casilla objetivo
                        obj = [(posReina[0] + (f * dist)), (posReina[1] + (c * dist))]
                        objdentro = ((0 <= obj[0] < n) and (0 <= obj[1] < n))

                        # print("obj:", obj)
                        # print("posreina:", posReina, " objetivo: ", obj, " dist:", dist)
                        # print("el obj esta dentro del tablero?", objdentro)

                        if(objdentro):  # Si el mov esta dentro del tablero
                            # print("trabajando con la reina:", posReina)
                            # print("pos:", pos)
                            # print("contenido de ", obj, ": ", mesa[obj[0]][obj[1]])

                            if(mesa[obj[0]][obj[1]] != 'x' and mesa[obj[0]][obj[1]] != 'X'):  # Si la casilla objetivo esta vacia
                                # print("posreinas:", posreinasSTR)
                                # print("posreinas not in grafo?", (posreinasSTR not in grafo))
                                if(posreinasSTR not in grafo):
                                    grafo[posreinasSTR] = []
                                    #file.write("\nNV---" + ''.join(novisitados) + ", ")
                                    file.write("\n" + posreinasSTR + ": ")
                                    caso += 1
                                    print("Generando caso #" + str(caso))
                                # print("grafo:", grafo)

                                agregar = posreinasSTR
                                agregar = list(agregar)
                                agregar[i*2] = str(obj[0])
                                agregar[(i*2) + 1] = str(obj[1])
                                agregar = ''.join(agregar)


                                novisitados.append(agregar)

                                # print("valor q se agrega al grafo: ", agregar)

                                grafo[posreinasSTR].append(agregar)
                                file.write(agregar + ", ")

                                # print("grafo:", grafo, "\n")

                            else:  # Si la casilla objetivo no esta vacia
                                break
                        else:
                            break
            # del f, c
            # print("nov:", novisitados)
            # print("vis:", visitados)
    file.close()
    return grafo


def listatostr(lista):
    ret = ""
    for x in lista:
        ret = ret + str(x[0]) + str(x[1])
    return ret


def strtolista(str):
    ret = list()
    str = list(str)
    for i in range(int(len(str)/2)):
        ret.append([int(str[2*i]), int(str[(2*i)+1])])
    return ret


# def validarCasilla()
if (__name__ == "__main__"):
    pass
    
