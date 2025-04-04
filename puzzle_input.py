# puzzle_input.py
# Bill Hanson
#
# Inputs a puzzle input and creates targets and puzzle mask
#   plus makes a first cut by removing obviously invalid numbers

# get imports
import numpy as np
import os

# define path
cur_dir = os.getcwd()
work_dir = 'CS475_project'
csv_name = '8x8_2.csv'
csv_input_name = os.path.join(cur_dir, work_dir, csv_name)
npz_name = '10x10_0.2.npz'
npz_input_name = os.path.join(cur_dir, work_dir, npz_name)

# define functions

def load_puzzle_npz(n_in_name):
    # loads the puzzle from npz file where row and column targets
    #   are already defined
    puzzle_data = np.load(n_in_name)
    puzzle_a = puzzle_data['arr_0']
    r_tgt = puzzle_data['arr_1']
    c_tgt = puzzle_data['arr_2']
    p_size = puzzle_a.shape[0]

    return puzzle_a, p_size, c_tgt, r_tgt

def load_puzzle_csv(c_in_name):
    # takes a csv file and returns the puzzle_array, puzzle size, 
    #    and row and column targets
    # input from csv
    input_a = np.loadtxt(c_in_name, 
                           delimiter=',', dtype=int)  # note, need a '0' at 0,0
    # We know the array is square, so just pick 1st element of shape
    input_size = input_a.shape[0]

    # strip off row and column targets
    c_tgt = input_a[0,1:input_size]
    r_tgt = input_a[1:input_size,0]

    # delete the target row and column
    tmp_arr = np.delete(input_a, 0, 0)        # delete top row
    puzzle_a = np.delete(tmp_arr, 0, 1)     # delete first column
    p_size = input_size - 1
    return puzzle_a, p_size, c_tgt, r_tgt

def create_masks(p_size):
    # sets up boolean masks given puzzle size
    c_mask = np.zeros([p_size], dtype=int)
    r_mask = np.zeros([p_size], dtype=int)
    p_mask = np.zeros([p_size, p_size], dtype=int)
    return c_mask, r_mask, p_mask

def initial_cut(p_size, p_array, r_tgt, c_tgt, p_mask):
    # initial cut to mask values larger than row or column target
    for i in range(p_size):
        for j in range(p_size):
            if p_array[i,j] > r_tgt[i] or p_array[i,j] > c_tgt[j]:
                p_mask[i,j] = -1
    return p_mask

#%% End puzzle_input