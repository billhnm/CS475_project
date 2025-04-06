# puzzle_swap.py
# Bill Hanson
#
# Inputs a puzzle input and creates a new puzzle by swapping either
#   two rows or two columns


# get imports
import numpy as np
from itertools import combinations
import os

# set up working dir
cur_dir = os.getcwd()
work_dir = 'CS475_project'
input_name = 's20x20_1_conv.csv'
input_path = os.path.join(cur_dir, work_dir, input_name)
# define functions 
'''
def load_puzzle_npz():
    # loads the puzzle from npz file where row and column targets
    #   are already defined
    puzzle_data = np.load('10x10_0.2.npz')
    puzzle_a = puzzle_data['arr_0']
    r_tgt = puzzle_data['arr_1']
    c_tgt = puzzle_data['arr_2']
    p_size = puzzle_a.shape[0]

    return puzzle_a, p_size, c_tgt, r_tgt
'''
def load_swap_puzzle():
    # Loads in a csv puzzle
    # Does not separate the targets from the puzzle, since we're going to swap them along with the rows
    # input from csv
    swap_grid = np.loadtxt(input_path, 
                           delimiter=',', dtype=int)  # note, need a '0' at 0,0
    # We know the array is square, so just pick 1st element of shape
    s_size = swap_grid.shape[0]

    return swap_grid, s_size

def determine_swap_combos(p_size):
    nums = range(1,p_size)
    s_combos = list(combinations(nums, 2))

    return s_combos

def swap_rows(grid_a, r1, r2):
    grid_a[[r1,r2]] = grid_a[[r2,r1]]

    return grid_a

def swap_columns(grid_a, c1, c2):
    grid_a[:,[c1,c2]] = grid_a[:,[c2,c1]]

    return grid_a

puzzle_a, puzzle_size = load_swap_puzzle()

swap_combos = determine_swap_combos(puzzle_size)

# set up directories

data_dir = 'data'
file_stub = '20x20_1'

for i in range(len(swap_combos)):
    puz_a = puzzle_a
    r1 = swap_combos[i][0]
    r2 = swap_combos[i][1]
    puz_b = swap_rows(puz_a, r1, r2)
    f_name = file_stub + 'r' + str(i) + '.csv'
    file_path = os.path.join(cur_dir, work_dir, data_dir, f_name)
    np.savetxt(file_path, puz_b, delimiter=',', fmt='%d')
   
for i in range(len(swap_combos)):
    puz_a = puzzle_a
    c1 = swap_combos[i][0]
    c2 = swap_combos[i][1]
    puz_b = swap_columns(puz_a, c1, c2)
    f_name = file_stub + 'c' + str(i) + '.csv'
    file_path = os.path.join(cur_dir, work_dir, data_dir, f_name)
    np.savetxt(file_path, puz_b, delimiter=',', fmt='%d')
#print(cur_dir)


# print(puzzle_a)
# puzzle_b = swap_rows(puzzle_a, 1, 2)
# print(puzzle_b)
#%% End puzzle_swap