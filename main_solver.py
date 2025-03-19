# main_solver.py
# Bill Hanson
#
# Main solver logic: steps through puzzle rows and columns
#   Calls other modules for operations
#
# Get imports
import numpy as np
from puzzle_input import load_puzzle_csv as load_puzzle, create_masks, initial_cut
from subset_finding import bf_find_subsets as find_subsets
from mask_operations import find_invalid_nums, find_required_nums

# Main program

# Declare needed variables
done = False

puzzle_array, puzzle_size, col_tgt, row_tgt = load_puzzle()

# load the puzzle from npz file 
# puzzle_data = np.load('10x10_0.2.npz')
# puzzle_array = puzzle_data['arr_0']
# row_tgt = puzzle_data['arr_1']
# col_tgt = puzzle_data['arr_2']

puzzle_size = puzzle_array.shape[0]

main_col_mask, main_row_mask, puzzle_mask = create_masks(puzzle_size)

print(row_tgt, col_tgt)
print(puzzle_array)

# Make the first cut 
puzzle_mask = initial_cut(puzzle_size, puzzle_array, row_tgt, col_tgt, puzzle_mask)
print(puzzle_mask)

iter = 0
while not done:
    # print("Starting new iteration of the loop")
    
    for i in range(puzzle_size):                    # step through the rows
        if main_row_mask[i] == 0:
            cur_row = puzzle_array[i,:]
            cur_row_mask = puzzle_mask[i,:]
            cur_row_tgt = row_tgt[i]

            valid_combos, upd_row_mask = find_subsets(cur_row, cur_row_tgt, cur_row_mask)
            #print(valid_combos)
            # Update main row mask
            if 0 not in cur_row_mask:    
                main_row_mask[i] = 1  
            else: 
                main_row_mask[i] = 0
            # Update puzzle mask
            puzzle_mask[i,:] = upd_row_mask
    
            next_row_mask = find_invalid_nums(valid_combos, cur_row, upd_row_mask)
            if 0 not in upd_row_mask:    
                main_row_mask[i] = 1 
            else: 
                main_row_mask[i] = 0
            # Update puzzle mask
            puzzle_mask[i,:] = next_row_mask
        #'''
            new_row_mask = find_required_nums(valid_combos, cur_row, next_row_mask)
            if 0 not in next_row_mask:    
                main_row_mask[i] = 1 
            else: 
                main_row_mask[i] = 0
            # Update puzzle mask
            puzzle_mask[i,:] = new_row_mask

    for i in range(puzzle_size):                    # step through the columns
        if main_col_mask[i] == 0:
            cur_col = puzzle_array[:,i]
            cur_col_mask = puzzle_mask[:,i]
            cur_col_tgt = col_tgt[i]

            valid_combos, upd_col_mask = find_subsets(cur_col, cur_col_tgt, cur_col_mask)
            #print(valid_combos)
            if 0 not in cur_col_mask:    
                main_col_mask[i] = 1 
            else: 
                main_col_mask[i] = 0
            # Update puzzle mask
            puzzle_mask[:,i] = upd_col_mask      

            next_col_mask = find_invalid_nums(valid_combos, cur_col, upd_col_mask)
            if 0 not in upd_col_mask:    
                main_col_mask[i] = 1 
            else:   
                main_col_mask[i] = 0
            # Update puzzle mask
            puzzle_mask[:,i] = next_col_mask
        #'''
            new_col_mask = find_required_nums(valid_combos, cur_col, next_col_mask)
            if 0 not in next_col_mask:    
                main_col_mask[i] = 1 
            else: 
                main_col_mask[i] = 0
            # update puzzle mask
            puzzle_mask[:,i] = new_col_mask
        #'''
     
    print('targets (r,c) ', row_tgt, col_tgt)
    print('main row mask: ', main_row_mask)
    print('main col mask: ', main_col_mask)
    print('puzzle mask: ', puzzle_mask)
    
    if np.all(puzzle_mask != 0) or (np.all(main_row_mask == 1) and np.all(main_col_mask == 1)):
        done = True
        print('done condition met')
    iter += 1
    if iter > 1000:
        done = True
        print('No solution after 1000 iterations')

print("Exited loop")

solution_array = puzzle_mask * puzzle_array

print('targets (r,c) ', row_tgt, col_tgt)

print(solution_array)

print(f'Number of elements in solution array: {np.sum(solution_array > 0)}')

if iter > 1000:
    print('No solution found after 1000 iterations')
else: 
    print(f'Done in {iter} iterations')