
from pydoc import doc
from anneal import SimAnneal
import matplotlib.pyplot as plt
import random
from file_controller import read_file

num = 8
while(num != 4 and num != 12 and num != 8):
    num = int(input("Ingresar N:"))
nataques = (num*(num-1))/2
print(nataques)
tablero = read_file(num)

def read_coords():
    coords = []
    for line in tablero:
        coords.append(line)
    return coords

# def read_coords(path):
#     coords = []
#     with open(path, "r") as f:
#         for line in f.readlines():          
#             line = [float(x.replace("\n", "")) for x in line.split(" ")]
#             coords.append(line)
#     return coords

def generate_random_coords(num_nodes):
    return [[int(random.uniform(0, 4)), int(random.uniform(0, 4))] for i in range(num_nodes)]

if __name__ == "__main__":
    coords = read_coords()
    sa = SimAnneal(coords,nataques,num ,stopping_iter=5000)
    sa.anneal()
    plt.plot(sa.fitness_list_cell)
    plt.ylabel('Population Fitness')
    plt.xlabel('Generation')
    plt.show()
   
  
