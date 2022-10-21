from calendar import c
import math
import random
from traceback import print_tb
import visualize_tsp
import matplotlib.pyplot as plt
import time


class SimAnneal(object):
    def __init__(self, coords, nataques, nnnnnnn ,T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.coords = coords
        self.nnnnnnn = nnnnnnn
        self.N = len(coords)
        self.coords_without_queens = 0;
        self.T = math.sqrt(self.N) if T == -1 else T
        self.T_save = self.T  # save inital T to reset if batch annealing is used
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 1e-8 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1
        self.max_ataques = nataques
        self.nodes = [i for i in range(self.N)]
        # Eduard
        self.initial_queens_positions = []
        for positions in self.coords:
            if(positions[2] != 0):
                self.initial_queens_positions.append(positions)
        self.fitness_list_cell = []
        self.best_solution_table = None
        self.best_fitness_table = self.max_ataques

        self.best_solution = None
        self.best_fitness = float("Inf")
        self.fitness_list = []

    def initial_solution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour).
        """
        #ORIGINAL
        # cur_node = random.choice(self.nodes)  # start from a random node
        # solution = [cur_node]
        # free_nodes = set(self.nodes)
        # free_nodes.remove(cur_node)

    
        # while free_nodes:
        #     next_node = min(free_nodes, key = lambda x: self.dist(cur_node, x))  # nearest neighbour
        #     free_nodes.remove(next_node)
        #     solution.append(next_node)
        #     cur_node = next_node

        # cur_fit = self.fitness(solution)

        # if cur_fit < self.best_fitness:  # If best found so far, update best fitness
        #     self.best_fitness = cur_fit
        #     self.best_solution = solution
        # self.fitness_list.append(cur_fit)

        # Eduard
        # Initial queens positions
        cur_positions = self.initial_queens_positions
        solution_cells = [cur_positions]
    
        free_cells = [elem for elem in self.coords if elem not in cur_positions]
     
        # Number of queens
        queens = [i+1 for i in range(len(cur_positions))]
        self.numerodereinas = queens
        table = []
        for j in range(self.nnnnnnn*self.nnnnnnn) :  
            #Genero 4 numeros rand diferentes  
            num = []
            x = 0
            while (x < 4):
                num_ram = random.randint(0, len(self.coords)-1)
                if(num_ram in num):
                    x = x - 1
                else:
                    num.append(num_ram)
                x = x + 1
               
            for k in range(len(num)):
                table.append(self.coords[num[k]])
                           
            solution_cells.append(table)
            table = []
   
        cur_fit_table = self.fitness_table(solution_cells[0])
        aux_cur_fit_table = cur_fit_table
        for i in range(len(solution_cells)+1):
            if i < len(solution_cells):
                if cur_fit_table < self.best_fitness_table:
                    self.best_solution_table = solution_cells[i] 
                    self.best_fitness_table =  cur_fit_table
                       
                cur_fit_table = self.fitness_table(solution_cells[i])
                self.fitness_list_cell.append(cur_fit_table)
                if  cur_fit_table == self.max_ataques:
                        break 
        print(self.fitness_list_cell)
        print(self.best_fitness_table)
        #Eduard end          
           
        return solution_cells, aux_cur_fit_table 
        #return solution, cur_fit

    def dist_cells(self, cell_0, cell_1):
        """
            Euclidean distance between two nodes.
        """
        return math.sqrt((cell_0[0] - cell_1[0]) ** 2 + (cell_0[1] - cell_1[1]) ** 2)

    def dist(self, node_0, node_1):
        """
        Euclidean distance between two nodes.
        """
        coord_0, coord_1 = self.coords[node_0], self.coords[node_1]
        return math.sqrt((coord_0[0] - coord_1[0]) ** 2 + (coord_0[1] - coord_1[1]) ** 2)

    def fitness_table(self, pos): 
        aux = []
        for i in range(len(pos)):
            aux.append(pos[i][0])
        horizontal_collisions = sum([aux.count(queen)-1 for queen in aux])/2 
        diagonal_collisions = 0
        for i in range(len(pos)):
            j=i+1
            while(j<4):
                if(abs(pos[i][0] - pos[j][0]) == abs(pos[i][1] - pos[j][1])):
                    diagonal_collisions += 1
                j += 1
        fit = int(self.max_ataques-(diagonal_collisions +horizontal_collisions))
        return fit

    def fitness(self, solution):
        """
        Total distance of the current solution path.
        """
        cur_fit = 0
        for i in range(self.N):
            cur_fit += self.dist(solution[i % self.N], solution[(i + 1) % self.N])
        return cur_fit

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate, index):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty p_accept(..) if candidate is worse.
        """
        candidate_fitness = self.fitness_table(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness, self.cur_solution[index] = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness, self.cur_solution[index] = candidate_fitness, candidate
        

    def anneal(self):
        """
        Execute simulated annealing algorithm.
        """
        # Initialize with the greedy solution.
        self.cur_solution, self.cur_fitness = self.initial_solution()
        p = 0
        print("Starting annealing.")
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter  and p < self.nnnnnnn*self.nnnnnnn:
            candidate = list(self.cur_solution[p])
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)

            self.cur_solution[i : (i + l)] = reversed(self.cur_solution[i : (i + l)])

            self.accept(candidate, p)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)
            p = p + 1

        print("Best fitness obtained: ", self.best_fitness)
        improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
        print(f"Improvement over greedy heuristic: {improvement : .2f}%")

    def batch_anneal(self, times=10):
        """
        Execute simulated annealing algorithm `times` times, with random initial solutions.
        """
        for i in range(1, times + 1):
            print(f"Iteration {i}/{times} -------------------------------")
            self.T = self.T_save
            self.iteration = 1
            self.cur_solution, self.cur_fitness = self.initial_solution()
            self.anneal()

    def visualize_routes(self):
        """
        Visualize the TSP route with matplotlib.
        self.best_fitness_table
        """
        visualize_tsp.plotTSP([6], self.coords)

    def plot_learning(self):
        """
        Plot the fitness through iterations.
        """
        plt.plot([i for i in range(len(self.fitness_list_cell))], self.fitness_list_cell)
        plt.ylabel("Fitness")
        plt.xlabel("Iteration")
        plt.show()
