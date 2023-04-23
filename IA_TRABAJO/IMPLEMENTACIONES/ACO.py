import random
import time
import matplotlib.pyplot as plt
from knapsack import Knapsack
import csv

class ACO:
    def __init__(self, knapsack, num_ants, num_generations, alpha, beta, evaporation_rate):
        self.knapsack = knapsack
        self.num_ants = num_ants
        self.num_generations = num_generations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_trails = [1.0 for _ in range(len(knapsack.values))]

    def select_item(self, available_items):
        probabilities = []
        total = sum(self.pheromone_trails[i] ** self.alpha * (self.knapsack.values[i] / self.knapsack.weights[i]) ** self.beta for i in available_items)
        for i in available_items:
            prob = (self.pheromone_trails[i] ** self.alpha * (self.knapsack.values[i] / self.knapsack.weights[i]) ** self.beta) / total
            probabilities.append(prob)
        return random.choices(available_items, probabilities)[0]

    def construct_solution(self):
        solution = [0] * len(self.knapsack.values)
        available_items = list(range(len(self.knapsack.values)))
        weight = 0
        while available_items:
            item = self.select_item(available_items)
            if weight + self.knapsack.weights[item] <= self.knapsack.capacity:
                solution[item] = 1
                weight += self.knapsack.weights[item]
            available_items.remove(item)
        return solution

    def update_pheromones(self, best_solution):
        for i in range(len(self.pheromone_trails)):
            self.pheromone_trails[i] = (1 - self.evaporation_rate) * self.pheromone_trails[i]
        for i in range(len(best_solution)):
            if best_solution[i]:
                self.pheromone_trails[i] += self.knapsack.value(best_solution)

    def run(self):
        best_solution = None
        best_value = 0
        convergence = []
        start_time = time.time()
        for generation in range(self.num_generations):
            solutions = [self.construct_solution() for _ in range(self.num_ants)]
            for solution in solutions:
                value = self.knapsack.value(solution)
                if value > best_value:
                    best_solution = solution
                    best_value = value
                    best_iteration = self.num_ants * generation
            self.update_pheromones(best_solution)
            convergence.append(best_value)
        end_time = time.time()
        time_elapsed = end_time - start_time
        total_iterations = self.num_ants * self.num_generations
        return best_solution, convergence, time_elapsed, best_iteration, total_iterations
# Parámetros del algoritmo de colonia de hormigas
num_ants = 600
num_generations = 60
alpha = 0.6
beta = 0.8
evaporation_rate = 0.2
knapsack = Knapsack()
contador = 0

for i in range(30):
  aco = ACO(knapsack, num_ants, num_generations, alpha, beta, evaporation_rate)
  best_solution, convergence, time_elapsed, best_iteration, total_iterations = aco.run()
  print("Mejor solución encontrada:", best_solution)
  print("Tiempo empleado para encontrar la solución:", time_elapsed, "segundos")
  print("Número de iteraciones para encontrar la mejor solución:", best_iteration)
  print("Mejor solución con su respectivo valor total:", knapsack.value(best_solution))
  print("Número total de iteraciones:", total_iterations)
  contador += 1
  print("Ronda : ", contador)
  # grafica
  plt.plot(convergence)
  plt.xlabel("Generaciones")
  plt.ylabel("Mejor Valor Mochila")
  plt.title("CONVERGENCIA ALGORITMO COLONIA DE HORMIGAS")
  plt.show()
  with open('SolucionACO.csv', mode='a', newline='') as file:
     writer = csv.writer(file)
     writer.writerow([knapsack.value(best_solution), time_elapsed, best_iteration])
  