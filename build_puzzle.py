# Build_puzzle.py
# Bill Hanson

# Creates a number sum puzzle given a puzzle size

# imports
import numpy as np
import random

# define functions
def weighted_solution_nums():
    elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    weights = [0.105, 0.123, 0.11, 0.11, 0.12, 0.1, 0.112, 0.1, 0.12]

    weighted_integer = random.choices(elements, weights, k=1)
    
    return weighted_integer[0]

def weighted_filler_nums():
    elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # bias to higher numbers and primes
    weights = [0.03, 0.04, 0.07, 0.05, 0.13, 0.06, 0.18, 0.2, 0.24]

    weighted_filler = random.choices(elements, weights, k=1)
    
    return weighted_filler[0]

def create_puzzle(p_size, prob):
    # creates a puzzle given a puzzle size and probability of a number
    puzzle = np.zeros([p_size, p_size],
                        dtype = int)
    for i in range(p_size):
        for j in range(p_size):
            if random.random() < prob:
                puzzle[i,j] = weighted_solution_nums()
            else:
                puzzle[i,j] = 0
    return puzzle

def create_targets(puzzle, p_size):
    # creates the row and column targets given a puzzle
    row_targets = np.zeros([p_size],
                        dtype = int)
    col_targets = np.zeros([p_size],
                        dtype = int)
    
    for i in range(p_size):         # sum the rows and columns to create targets
        row_targets[i] = sum(puzzle[i,:])
        col_targets[i] = sum(puzzle[:,i])
    
    for i in range(puzzle_size):    # check to make sure that we don't have any empty rows or columns
                                    # if so, add a random number to the row or column
        if row_targets[i] == 0:
            puzzle[i,(random.randint(0,puzzle_size-1))] = weighted_solution_nums()
        if col_targets[i] == 0:
            puzzle[(random.randint(0,puzzle_size-1)),i] = weighted_solution_nums()
    
    # re-sum the rows and columns to recreate targets
    for i in range(puzzle_size):
        row_targets[i] = sum(puzzle[i,:])
        col_targets[i] = sum(puzzle[:,i])
        
    return row_targets, col_targets

def finish_puzzle(puzzle, p_size):
    # fills in the 0 entries in the puzzle with weighted random integers
    for i in range(p_size):
        for j in range(p_size):
            if puzzle[i,j] == 0:
                puzzle[i,j] = weighted_filler_nums()
    return puzzle

# Constants
#prob = 0.33
#puzzle_size = 7
# get inputs
puzzle_size = int(input('Enter the puzzle size: '))
prob = float(input('Enter the probability of a number: '))
num_puzzles = int(input('Number of puzzles? '))

for i in range(num_puzzles):
# Create the puzzle
    puzzle = create_puzzle(puzzle_size, prob)

    # Create the row and column targets
    row_targets, col_targets = create_targets(puzzle, puzzle_size)

    # Now fill in the 0 entries in the puzzle with random integers
    puzzle = finish_puzzle(puzzle, puzzle_size)
    ps = puzzle_size
    pr = round(prob,2)
    name_string = str(ps)+'x'+str(ps)+'_'+str(pr)+'-'+ str(i) + '.npz'

    # now save the puzzle, row targets, and column targets
    np.savez(name_string, puzzle, row_targets, col_targets)

# just to check, let's reload the puzzle and print it out
# load the puzzle  
'''
puzzle_data = np.load(name_string)
puzzle = puzzle_data['arr_0']
row_targets = puzzle_data['arr_1']
col_targets = puzzle_data['arr_2']

print('Puzzle:')
print(puzzle)
print('Row Targets:')
print(row_targets)
print('Column Targets:')
print(col_targets)
'''