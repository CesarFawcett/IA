import random
import csv

class Knapsack:
    def __init__(self):
        self.capacity = None
        self.values = []
        self.weights = []
        self.read_knapsack_data_from_csv()
    
    def read_knapsack_data_from_csv(self):
        with open("input8.csv", newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')   
            is_first_row = True
            for row in csv_reader:
                if is_first_row:
                    is_first_row = False
                    continue
                if self.capacity is None:
                    self.capacity = int(row[0])
                else:
                    self.values.append(int(row[1]))
                    self.weights.append(int(row[2]))
  
    def value(self, solution):
        total_value = 0
        total_weight = 0
        for i in range(len(solution)):
            if solution[i]:
                total_value += self.values[i]
                total_weight += self.weights[i]
        return total_value if total_weight <= self.capacity else 0

    def generate_neighbor(self, solution):
        index = random.randint(0, len(solution) - 1)
        neighbor = solution.copy()
        neighbor[index] = 1 - neighbor[index]
        return neighbor