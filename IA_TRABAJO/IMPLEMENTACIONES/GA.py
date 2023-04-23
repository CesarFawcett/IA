import random
import matplotlib.pyplot as plt
import time
from knapsack import Knapsack
import csv

class GA:
    def __init__(self, knapsack, population_size, mutation_rate, crossover_rate, elitism_rate, max_generations):
        self.knapsack = knapsack
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.max_generations = max_generations

    def create_individual(self):
        n = len(self.knapsack.values)
        individual = [random.randint(0, 1) for _ in range(n)]
        return individual

    def create_population(self):
        population = [self.create_individual() for _ in range(self.population_size)]
        return population

    def fitness(self, individual):
        return self.knapsack.value(individual)

    def mutate(self, individual):
        mutated_individual = individual.copy()
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                mutated_individual[i] = 1 - mutated_individual[i]
        return mutated_individual

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        else:
            return parent1.copy(), parent2.copy()

    def selection(self, population):
        return random.choices(population, weights=[self.fitness(individual) for individual in population], k=2)


    def main(self):
        population = self.create_population()
        best_individual = max(population, key=self.fitness)
        convergence = []
        best_solution_generation = 0
        start_time = time.time()
        for generation in range(self.max_generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.selection(population)
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])
            population = new_population
            current_best_individual = max(population, key=self.fitness)
            if self.fitness(current_best_individual) > self.fitness(best_individual):
               best_individual = current_best_individual
               best_solution_generation = generation
            convergence.append(self.fitness(current_best_individual))  
        end_time = time.time()
        time_elapsed = end_time - start_time
        return best_individual, convergence, time_elapsed, best_solution_generation


# Parámetros del GA
population_size = 1000
mutation_rate = 0.42
crossover_rate = 0.32
max_generations = 500
elitism_rate = 0.85
knapsack = Knapsack()
for i in range(1):
   ga = GA(knapsack, population_size, mutation_rate, crossover_rate, elitism_rate, max_generations)
   best_solution, convergence, time_elapsed, best_solution_generation = ga.main()


   print("Mejor solución encontrada:", best_solution)
   print("Tiempo empleado para encontrar la solución:", time_elapsed, "segundos")
   print("Número de iteraciones para encontrar la mejor solución:", best_solution_generation)
   print("Valor total de la mochila:", knapsack.value(best_solution))
   print("Número total de iteraciones:", max_generations * population_size)

   # Grafica
   plt.plot(convergence)
   plt.xlabel("Generaciones")
   plt.ylabel("Mejor valor mochila")
   plt.title("CONVERGENCIA ALGORITMO GENETICO")
   plt.show()
   with open('SolucionGA.csv', mode='a', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([knapsack.value(best_solution), time_elapsed, best_solution_generation])
