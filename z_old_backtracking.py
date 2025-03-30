# backtracking.py
# Bill Hanson
#
# Solves number sums grid as a CSP using backtracking with forward-checking
#
# imports
import numpy as np

def load_puzzle_csv():
    # takes a csv file and returns the puzzle_array, puzzle size, 
    #    and row and column targets
    # input from csv
    input_a = np.loadtxt("x_6x6_1.csv", 
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

def check_if_safe(row, col, puzzle_a, s_grid, p_size, row_tgt, col_tgt):
    # forward checks if selecting the r,c target is valid
    temp_s_grid = s_grid
    temp_sel = row, col

    # check the row sum
    for row in range(p_size):
        row_sum = 0
        for col in range(p_size):
            if temp_s_grid[row, col] == True:                  # update sum if assignment is true
                row_sum += puzzle_a[row, col]
                if row_sum > row_tgt[row]:
                    return False
    
    # now check the column sum
    for col in range(p_size):
        col_sum = 0
        for row in range(p_size):
            if temp_s_grid[row, col] == True:
                col_sum += puzzle_a[row, col]
                if col_sum > col_tgt[col]:
                    return False
    
    return True



# main
puzzle_array, puzzle_size, col_tgts, row_tgts = load_puzzle_csv()

selection_grid = np.zeros([puzzle_size, puzzle_size], dtype=bool)

print(row_tgts, col_tgts)
print(puzzle_array)
print(selection_grid)

for i in range(puzzle_size):
    for j in range(puzzle_size):
        check_if_safe(i, j, puzzle_array, selection_grid, puzzle_size, row_tgts, col_tgts)

print(selection_grid)