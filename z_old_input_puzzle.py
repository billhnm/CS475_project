# Input_puzzle
# Bill Hanson

# Inputs the puzzle file from csv, strips off the row 
#   and column targets and reads the puzzle into a numpy array

# imports
import numpy as np
from itertools import combinations

# define functions

def get_puzzle(input_a):
    # takes an input array and returns the puzzle_array, puzzle size, 
    #    and row and column targets
    # We know the array is square, so just pick 1st element of shape
    input_size = input_a.shape[0]

    # strip off row and column targets
    c_tgt = input_a[0,1:input_size]
    r_tgt = input_a[1:input_size,0]

    # delete the target row and column
    tmp_arr = np.delete(input_a, 0, 0)        # delete top row
    puzzle_a = np.delete(tmp_arr, 0, 1)     # delete first column
    puzzle_s = input_size - 1
    return puzzle_a, puzzle_s, c_tgt, r_tgt

def create_masks(p_size):
# sets up boolean masks given puzzle size
    c_mask = np.zeros([p_size],
                        dtype = int)
    r_mask = np.zeros([p_size],
                        dtype = int)
    p_mask = np.zeros([p_size, puzzle_size],
                        dtype = int)
    return c_mask, r_mask, p_mask

def initial_cut(p_size, p_array, r_tgt, c_tgt, p_mask):
# initial cut to mask values larger than row or column target
    for i in range(p_size):
        for j in range(p_size):
            if p_array[i,j] > r_tgt[i] or p_array[i,j] > c_tgt[j]:
                p_mask[i,j] = -1
    return(p_mask)

def bf_find_combinations(input_list, length):
    # Generates all combinations of a list with given length and returns a list of combination tuples  
    return list(combinations(input_list, length))

 #comment out for now
def bf_find_subsets(nums, target, l_mask):
    # returns brute force valid subset given a list of numbers and target
    test_sum = 0
    combo_list = []
    val_combos = []
    temp_combo = []
    t_nums = nums.copy()          # save original numbers to reset mask
    t_mask = l_mask.copy()
    
    # don't consider masked numbers 
    for i in range(len(t_nums)-1, -1, -1):      # iterate backwards to avoid index issues
        if t_mask[i] == 1: 
            # required number: don't include it and decrement target
            target = target - t_nums[i] 
            t_nums = np.delete(t_nums, i)
        elif t_mask[i] == -1:
            # invalid number: don't include it
            t_nums = np.delete(t_nums, i)

    for i in range(len(t_nums) + 1):
        temp_combo = bf_find_combinations(t_nums.tolist(), i)
        combo_list = combo_list + temp_combo

    # check if any add up to the target value
    for j in range(1, len(combo_list)):
        test_sum = sum(combo_list[j])
    
        if test_sum == target: 
            val_combos.append(combo_list[j])
                
    if len(val_combos) == 1:                    # Done if only 1 valid combo left
        for k in range(len(nums)):
            if t_mask[k] == 0:                              # only reset mask if not already set
                if nums[k] in val_combos[0]:
                    t_mask[k] = 1                           # everything in the last combo is needed
                else:
                    t_mask[k] = -1                          # not in the last combo, not needed

                   
    return val_combos, t_mask

''' #Comment out for now
# 2nd cut: use dynamic programming
def dp_find_subsets(nums, target, l_mask):
    # Uses dynamic program to find all subsets of a list summing to target
    
    val_combos = []
    t_nums = nums.copy()          # save original numbers to reset mask
    t_mask = l_mask.copy()  
    n_nums = nums.tolist()

    # First, check for masked variables
        # don't consider masked numbers 
    for i in range(len(n_nums) - 1, -1, -1):      # iterate backwards to avoid index issues
        if t_mask[i] == 1: 
            # required number: don't include it
            target = target - n_nums[i]           # decrement 
            t_nums = np.delete(t_nums, i)
        elif t_mask[i] == -1:
            # invalid number: don't include it
            t_nums = np.delete(t_nums, i)
    
      # Initialize the list of lists
    dp = [[] for _ in range(target + 1)]
    dp[0] = [[]]  # Base case: one way to make sum 0 - the empty subset

    for num in n_nums:
        for i in range(target, num - 1, -1):
            for subset in dp[i - num]:
                dp[i].append(subset + [num])
    
    val_combos = dp[target]
    
    if len(val_combos) == 1:                    # Done if only 1 valid combo left
        for k in range(len(n_nums)):
            if t_mask[k] == 0:                              # only reset mask if not already set
                if n_nums[k] in val_combos[0]:
                    t_mask[k] = 1                           # everything in the last combo is needed
                else:
                    t_mask[k] = -1                          # not in the last combo, not needed

    return val_combos, t_mask
'''
    
# now, find any member of the list that's not in a valid combo
def find_invalid_nums(combos, nums, l_mask):
    # first, flatten the valid list to just numbers (saves us a nested loop)
    flat_nums = [item for sublist in combos for item in sublist]
    t_mask = l_mask.copy()
    
    for i in range(len(nums)):
        if t_mask[i] == 0:          # only check if mask isn't already set
            if nums[i] not in (flat_nums):
                t_mask[i] = -1

    return t_mask

# Now, find any member of the list that MUST be in the solution

def find_required_nums(combos, nums, l_mask):
    # General approach: step through valid solutions and see if any number is in all of them
    t_mask = l_mask.copy()
    n_nums = nums.tolist()
    for i in range(len(n_nums)):
        if t_mask[i] == 0 and n_nums.count(n_nums[i]) == 1:          # only check if mask isn't already set and there is only one instance of number 
            valid_count = 0
            for j in range(len(combos)):
                if n_nums[i] in combos[j] and t_mask[i] == 0:
                    valid_count += 1

            if valid_count == len(combos):
                t_mask[i] = 1
                # print(nums[i], ' is needed in all combinations')
    return t_mask


#%% Main program

# Declare needed variables
done = False

#input from csv
input_arr = np.loadtxt("x_8x8_1.csv",
                       delimiter = ',', dtype = int)  # note, need a '0' at 0,0

puzzle_array, puzzle_size, col_tgt, row_tgt = get_puzzle(input_arr)

''' 

# load the puzzle from npz file 
puzzle_data = np.load('10x10_0.2.npz')
puzzle_array = puzzle_data['arr_0']
row_tgt = puzzle_data['arr_1']
col_tgt = puzzle_data['arr_2']
'''
puzzle_size = puzzle_array.shape[0]

main_col_mask, main_row_mask, puzzle_mask = create_masks(puzzle_size)

print(row_tgt, col_tgt)
print(puzzle_array)

# Make the first cut 
puzzle_mask = initial_cut(puzzle_size, puzzle_array, row_tgt, col_tgt, puzzle_mask)
print(puzzle_mask)

iter = 0
while not done:
    #print('Starting new loop iteration')
    

    for i in range(puzzle_size):                    # step through the rows
        if main_row_mask[i] == 0:
            cur_row = puzzle_array[i,:]
            cur_row_mask = puzzle_mask[i,:]
            cur_row_tgt = row_tgt[i]
            # old_puzzle_mask = puzzle_mask

            valid_combos, upd_row_mask = bf_find_subsets(cur_row, cur_row_tgt, cur_row_mask)
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
 
        #'''

    for i in range(puzzle_size):                    # step through the columns
        if main_col_mask[i] == 0:
            cur_col = puzzle_array[:,i]
            cur_col_mask = puzzle_mask[:,i]
            cur_col_tgt = col_tgt[i]
            # old_puzzle_mask = puzzle_mask

            valid_combos, upd_col_mask = bf_find_subsets(cur_col, cur_col_tgt, cur_col_mask)
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


    #print('targets (r,c) ', row_tgt, col_tgt)
    #print('main row mask: ', main_row_mask)
    #print('mmain col mask: ', main_col_mask)
    #print('puzzle mask: \n', puzzle_mask)
    
    if np.all(puzzle_mask != 0) or (np.all(main_row_mask == 1) and np.all(main_col_mask == 1)):
        done = True
        print('done condition met')
    #else:
        #print('not done yet')
    iter += 1
    if iter > 1000:
        done = True
        #print('No solution after 2500 iterations')

    # Additional debug prints to check the loop condition
    # print(f"done: {done}")
    # print(f"np.all(puzzle_mask != 0): {np.all(puzzle_mask != 0)}")    

# print('exited loop')

solution_array = puzzle_mask * puzzle_array

print('targets (r,c) ', row_tgt, col_tgt)

print(solution_array)

print(f'Number of elements in solution array: {np.sum(solution_array > 0)}')

if iter > 1000:
    print('No solution found after 1000 iterations')
else: print(f'Done in {iter} iterations')
