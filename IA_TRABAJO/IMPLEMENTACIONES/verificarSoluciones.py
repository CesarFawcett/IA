# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 20:14:39 2023

@author: cesarfawcettdp

Realizado para sacar promedios y graficar los datos recolectados en la solucion
"""
import pandas as pd
import matplotlib.pyplot as plt

# Lee el archivo CSV
df = pd.read_csv('SolucionSA.csv', header=None)

# Promedio Datos
promedio = df[0].mean()

# Extrae las columnas deseadas
#columna1 = df[1]
columna2 = df[1]
#columna3 = df[2]

# GRAFICA DISPERSION
plt.scatter(range(len(columna2)), columna2, label='valor total mochila')
#plt.scatter(range(len(columna2)), columna2, label='tiempo')
#plt.scatter(range(len(columna3)), columna3, label='Columna 3')
plt.title('Gráfica de dispersión')
plt.xlabel('ITERACION')
plt.ylabel('VALOR MAXIMO MOCHILA ')
plt.legend()
plt.show()
#GRAFICA LINEAS
plt.plot(columna2)
plt.title('Gráfica de línea')
plt.xlabel('ITERACIONES PROPIAS')
plt.ylabel('TIEMPO  ')
plt.show()
#GRAFICA
plt.bar(range(len(columna2)), columna2)
plt.title('Gráfica de barras')
plt.xlabel('ITERACION')
plt.ylabel('VALOR MAXIMO MOCHILA  ')
plt.show()
#DATOS PROMEDIADOS Y PROMEDIOS
# Imprime los promedios
print('Promedios:')
print(promedio)

# Imprime la tabla
#print('Tabla:')
#print(df)




