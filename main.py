import random
from itertools import product
import os
import time

def int_to_ship(n):
  return " " if n in [0,1] else str(n)

class Game:
  def __init__(self, size=10, ship_lengths=[5,4,3,3,2]):
    self.board = Board(size=size, autofill=True, ship_lengths=ship_lengths)
    self.hits_board = Board(size=size, ship_lengths=ship_lengths)
    self.shots = 0
    self.hits = 0

  def show_hits_board(self):
    os.system("clear")
    print(f"Shots: {self.shots}\tHits: {self.hits}\n")
    self.hits_board.show(numbers=True)
    print()

  def distance_grid(self):
    d = Board(size=self.board.size)
    # initialize with max values
    for cell in self.board.cells():
      d[cell] = self.board.size
    
    for cell in self.board.cells():
      d[cell] = 0 if self.hits_board[cell] == "X" else 1 + min(d[neighbour] for neighbour in self.hits_board.orthogonal_neighbours(cell))

    for cell in reversed(self.board.cells()):
      d[cell] = 0 if self.hits_board[cell] == "X" else 1 + min(d[neighbour] for neighbour in self.hits_board.orthogonal_neighbours(cell))

    return d

  def empty_cells_next_to_hits(self):
    return [ cell for cell in self.board.cells() if self.distance_grid()[cell] == 1 and self.hits_board[cell] == 0 ]

  def play(self, autoplay=False, strategy=None):
    while not self.game_won():
      self.show_hits_board()
      try:
        print("Please enter a square to aim at in the form \"<row>,<column>\"")
        if autoplay:
          if strategy == 1:
            try:
              sq = random.choice(self.empty_cells_next_to_hits())
            except IndexError:
              sq = random.choice(self.hits_board.empty_odds())
          else:
            # pick at random
            sq = random.choice(self.hits_board.empty_cells())
        else:
          sq = input()
        if sq == "cheat":
          os.system("clear")
          print("Having a sneaky look...\n")
          self.board.show(numbers=True)
          time.sleep(1)
          continue
        if sq == "exit":
          return
        if sq == "ai":
          self.play(autoplay=True, strategy=1)
        if self.board.size <= 10 and "," not in sq:
          i, j = map(int, sq)
        else:
          i, j = map(int, sq.split(","))
        self.fire(i,j)
        if not autoplay:
          time.sleep(0.5)
      except (ValueError, IndexError):
        pass

    self.show_hits_board()
    print("Game over")
    print(f"You sank {len(self.board.ships)} ships in {self.shots} shots")
  
  def fire(self,i,j):
    if self.hits_board[i,j] == 0:
      if self.board[i,j] > 1:
        self.hits_board[i,j] = "X"
        self.hits += 1
        print(f"Hit at {i,j}!")
      else:
        self.hits_board[i,j] = "."
        print(f"Miss at {i,j}.")
    else:
      print(f"Already shot at {i,j}.")
    self.shots += 1
    # time.sleep(0.25)

  def game_won(self):
    return self.hits == sum(self.board.ship_lengths)

class Board:
  def __init__(self, size=8, autofill=False, ship_lengths=[5,4,3,3,2], letters=False):
    self.grid = [ [ 0 for _ in range(size) ] for _ in range(size) ]
    self.size = size
    # self.ships = { 5: 1, 4: 1, 3: 2, 2: 1 } # length: number
    self.ship_lengths = ship_lengths
    self.ships = []
    if autofill:
      self.populate_grid()

  def __str__(self):
    # display = lambda cell: str(cell.length) if isinstance(cell, Ship) else " "
    return "\n".join(" ".join(map(int_to_ship, row)) for row in self.grid)

  def __repr__(self):
    return f"{self.size} x {self.size} board with {len(self.ship_lengths)} ships of lengths {self.ship_lengths}"

  def show(self, numbers=False, debug=False):
    if numbers:
      print("  " + " ".join(map(str, range(self.size))))
      print("\n".join(str(i) + " " + " ".join(map(int_to_ship, row)) for i, row in enumerate(self.grid)))
    elif debug:
      print("\n".join(" ".join(map(str, row)) for row in self.grid))
    else:
      print(self)

  def __getitem__(self, coords):
    i, j = coords
    return self.grid[i][j]

  def __setitem__(self, coords, value):
    i, j = coords
    self.grid[i][j] = value

  def rows(self):
    return [ row for row in self.grid ]

  def cols(self):
    return [ [ row[i] for row in self.grid ] for i in range(self.size) ]

  def cells(self):
    return list(product(range(self.size), repeat=2))

  def empty_cells(self):
    return [ cell for cell in self.cells() if self[cell] == 0 ]

  def empty_odds(self):
    return [ (i,j) for i,j in self.cells() if (i+j)%2 == 1 and self[(i,j)] == 0 ]

  def clear(self):
    # self.grid = [ [ 0 for i in range(self.size) ] for _ in range(self.size) ]
    for cell in self.cells():
      self[cell] = 0
    self.ships = []

  def populate_grid(self, allow_adjacencies=False):
    try:
      for ship_length in self.ship_lengths:
        coords = self.find_random_space(ship_length)
        self.place_ship(coords, aura=not allow_adjacencies)
    except IndexError:
      print("Could not populate grid")
      
  def find_spaces(self, ship_length):
    # find possible spaces
    possible_spaces = []
    # horizontal spaces
    for i, row in enumerate(self.rows()):
      for j in range(self.size):
        if row[j:j+ship_length] == [ 0 for _ in range(ship_length) ]:
          possible_spaces.append([(i,j), (i,j+ship_length-1)])
    # vertical spaces
    for j, col in enumerate(self.cols()):
      for i in range(self.size):
        if col[i:i+ship_length] == [ 0 for _ in range(ship_length) ]:
          possible_spaces.append([(i,j), (i+ship_length-1,j)])         
    return possible_spaces

  def find_random_space(self, ship_length):
    return random.choice(self.find_spaces(ship_length))

  def place_ship(self, coords, aura=True):
    start, end = coords
    self.ships.append(Ship(coords))

    if start[0] == end[0]:
      # horizontal
      l = end[1] - start[1] + 1
      if aura:
        for j in range(l):
          self.place_aura((start[0], start[1] + j))
      for j in range(l):
        self[start[0], start[1] + j] = l
      
    elif start[1] == end[1]:
      # vertical
      l = end[0] - start[0] + 1
      if aura:
        for i in range(l):
          self.place_aura((start[0] + i, start[1]))
      for i in range(l):
        self[start[0] + i, start[1]] = l

    else:
      print("Invalid coordinates")

  def neighbours(self, coords):
    i, j = coords
    return [ (i+di, j+dj) for di, dj in product([-1,0,1], repeat=2) if 0 <= i+di < self.size and 0 <= j+dj < self.size ]

  def orthogonal_neighbours(self, coords):
    i, j = coords
    return [ (i+di, j+dj) for di, dj in [(1,0), (-1,0), (0,1), (0,-1)] if 0 <= i+di < self.size and 0 <= j+dj < self.size ]
  
  def place_aura(self, coords):
    for cell in self.neighbours(coords):
      self[cell] = 1


class Ship:
  def __init__(self, coords):
    self.start, self.end = coords
    if self.start[0] == self.end[0]:
      self.length = self.end[1] - self.start[1] + 1
    else:
      self.length = self.end[0] - self.start[0] + 1

  def __repr__(self):
    return f"Ship of length {self.length} from {self.start} to {self.end}"

if __name__ == "__main__":
  print("Play yourself (1) or watch AI (2)?")
  response = int(input())
  g = Game()
  if response == 1:
    g.play()
  else:
    g.play(autoplay=True, strategy=1)