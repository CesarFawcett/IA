# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 00:20:27 2022

@author: cfawcett
"""

import itertools
import collections
import time

class Node:
    #
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        if (self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    @property
    def score(self):
        return (self.g + self.h)

    @property
    def state(self):
        return str(self)

    @property 
    def path(self):

        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        return self.puzzle.solved

    @property
    def actions(self):
        return self.puzzle.actions

    @property
    def h(self):
        return self.puzzle.manhattan

    @property
    def f(self):
        return self.h + self.g

    def __str__(self):
        return str(self.puzzle)

class Solver:
    #
    def __init__(self, start):
        self.start = start

    def solve(self):
        nexp = 1
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            node = queue.popleft()
            nexp = nexp +1
            if node.solved:
                print("°°°°°¡Se encontró la Solucion!°°°°°°")
                print("total de nodos : ",nexp)
                return node.path

            for move, action in node.actions:
                child = Node(move(), node, action)

                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

class Puzzle:
   
    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        #
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property 
    def actions(self):
        #
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'derecha':(i, j-1),
                      'izquierda':(i, j+1),
                      'arriba':(i-1, j),
                      'abajo':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    @property
    def manhattan(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j]-1, 3)
                    distance += abs(x - i) + abs(y - j)
        return distance


    def copy(self):
  
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def pprint(self):
        for row in self.board:
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row

def main():
   inicio = time.time()
   # example of use     
   #board = [[1,2,3],[4,5,0],[7,8,6]] #1 movimiento
   #board = [[1,0,3],[4,2,5],[7,8,6]]  #3 movimientos.
   board = [[1,2,3],[4,5,0],[6,7,8]]  #13 movimientos.
   puzzle = Puzzle(board)
   s = Solver(puzzle)
   p = s.solve()

   steps = -1
   for node in p:
      print(node.action)
      node.puzzle.pprint()
      steps += 1
   fin = time.time()
   print("Tiempo de ejecucion :",fin-inicio)
   print("Numero de pasos a la solucion : " + str(steps))
if __name__ == "__main__":
    main()