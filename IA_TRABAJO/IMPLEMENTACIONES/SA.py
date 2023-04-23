import random
import math
import matplotlib.pyplot as plt
import time
from knapsack import Knapsack
import csv

class SA:
    def __init__(self, knapsack, initial_temperature, cooling_factor, max_iterations, max_temperature_levels=500):
        self.knapsack = knapsack
        self.initial_temperature = initial_temperature
        self.cooling_factor = cooling_factor
        self.max_iterations = max_iterations
        self.max_temperature_levels = max_temperature_levels

    def main(self):
        n = len(self.knapsack.values)
        current_solution = [0 for _ in range(n)]
        best_solution = current_solution.copy()
        temperature = self.initial_temperature
        current_values = []

        start_time = time.time()
        iteration_count = 0
        for temperature_level in range(self.max_temperature_levels):
            for iteration in range(self.max_iterations):
                neighbor = self.knapsack.generate_neighbor(current_solution)
                delta = self.knapsack.value(neighbor) - self.knapsack.value(current_solution)

                if delta > 0 or random.random() < math.exp(delta / temperature):
                    current_solution = neighbor

                    if self.knapsack.value(current_solution) > self.knapsack.value(best_solution):
                        best_solution = current_solution.copy()

                current_values.append(self.knapsack.value(current_solution))
                temperature *= self.cooling_factor
                iteration_count += 1
                if iteration_count >= self.max_iterations:
                    break

            if iteration_count >= self.max_iterations:
                break

        end_time = time.time()

        time_elapsed = end_time - start_time
        best_solution_iterations = current_values.index(self.knapsack.value(best_solution))
        total_iterations = len(current_values)
        return best_solution, current_values, time_elapsed, best_solution_iterations, total_iterations

initial_temperature = 2000000
cooling_factor = 0.99
max_iterations = 50000
max_temperature_levels = 2
knapsack = Knapsack()
for i in range(1):
   sa = SA(knapsack, initial_temperature, cooling_factor, max_iterations, max_temperature_levels)
   solution, current_values, time_elapsed, best_solution_iterations, total_iterations = sa.main()
   print("Solución encontrada:", solution)
   print("Valor total de la mochila:", knapsack.value(solution))
   print("Tiempo empleado para encontrar la solución:", time_elapsed, "segundos")
   print("Número de iteraciones para encontrar la mejor solución:", best_solution_iterations)
   print("Número total de iteraciones:", total_iterations)
   plt.plot(current_values, linestyle='-', color='red', marker='o')
   plt.xlabel("Nivel de temperatura")
   plt.ylabel("Valor de la mochila ")
   plt.title("CONVERGENCIA ALGORITMO ENFRIAMIENTO SIMULADO")
   plt.show()
   with open('SolucionSA.csv', mode='a', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([knapsack.value(solution), time_elapsed, best_solution_iterations])
