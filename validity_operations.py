# validty_operations.py
# Bill Hanson
#
# Takes a set of combinations and finds both invalid and 
#   required numbers
# Called from main solver

# Get imports
import numpy as np

# define functions

def find_invalid_nums(combos, nums, l_mask):
    # first, flatten the valid list to just numbers (saves us a nested loop)
    flat_nums = [item for sublist in combos for item in sublist]
    t_mask = l_mask.copy()
    
    for i in range(len(nums)):
        if t_mask[i] == 0:          # only check if mask isn't already set
            if nums[i] not in flat_nums:
                t_mask[i] = -1

    return t_mask

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

def is_cell_valid(c_value, r_subsets, c_subsets):
    r_valid = False
    c_valid = False
    cell_valid = False
    for i in range(len(r_subsets)):
        if c_value in r_subsets[i]:
            r_valid = True
            continue
    for j in range(len(c_subsets)):
        if c_value in c_subsets[j]:
            c_valid = True
            continue
    if r_valid == True and c_valid == True:
        cell_valid = True
    
    return cell_valid

def create_bt_mask(p_size, p_array, p_mask, r_tgts, c_tgts):
    b_mask = []
    for cell_index in range(p_size * p_size):
        row, column, row_nums, col_nums, row_mask, col_mask, row_tgt, col_tgt, cell_value = determine_row_column(cell_index, 
                                                                                r_tgts, c_tgts, 
                                                                                p_array, p_mask, p_size)

        row_subsets = find_subsets(row_nums, row_tgt, row_mask)
        col_subsets = find_subsets(col_nums, col_tgt, col_mask)

        valid_cell = is_cell_valid(cell_value, row_subsets, col_subsets)

        if valid_cell == False:
            p_mask[row, column] = -1

    # redo mask for backtrack: change -1 to 0, 0 to plus one -- just add 1 to everything
    changer_mask = np.ones([p_size, p_size], dtype=int)
    b_mask = p_mask + changer_mask

    return b_mask