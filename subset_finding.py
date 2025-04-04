# subset_finding.py
# Bill Hanson
#
# Finds valid combinations using either Brute Force (bf) methods [works]
#   or Dynamic Programming (dp) methods [FIXME: not working yet]
#   or Backtracking (bt) methods [FIXME: not yet implemented]
# 
# Get imports
from itertools import combinations
import numpy as np
#from validity_operations import is_cell_valid

# Define functions
def bf_find_combinations(input_list, length):
    # Generates all combinations of a list with given length and returns a list of combination tuples  
    return list(combinations(input_list, length))

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

    for num in t_nums:
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

def bt_determine_row_column(c_index, r_tgts, c_tgts, p_array, p_mask, p_size):
    rw = c_index // p_size
    col = c_index % p_size 
    r_nums = p_array[rw,:]
    c_nums = p_array[:,col]
    r_mask = p_mask[rw,:]
    c_mask = p_mask[:,col]
    r_tgt = r_tgts[rw]
    c_tgt = c_tgts[col]
    c_value = p_array[rw, col]

    return rw, col, r_nums, c_nums, r_mask, c_mask, r_tgt, c_tgt, c_value

def bt_find_subsets(nums, tgt, mask):
    t_mask = mask.tolist()
    t_nums = nums.tolist()
    t_tgt = tgt
    result = []

    for i in range(len(t_nums) - 1, -1, -1):            # screen out values already set, iterate backwards to avoid index probs
        if t_mask[i] == -1:
            del t_nums[i]
        if t_mask[i] == 1:                              # decrement target and don't consider
            t_tgt = t_tgt - t_nums[i]
            del t_nums[i]

    def local_backtrack(idx, cur_subset, cur_sum):
    
        if cur_sum == t_tgt:
            result.append(cur_subset[:])                            # use a copy so you don't mung the original 
            return 
        if cur_sum > t_tgt or idx == len(t_nums):
            return 
    
    # now try both including and excluding the current number
        cur_subset.append(t_nums[idx])
        local_backtrack(idx + 1, cur_subset, cur_sum + t_nums[idx])

        cur_subset.pop()
        local_backtrack(idx + 1, cur_subset, cur_sum)

    local_backtrack(0, [], 0)
        
    return result

def bt_just_find_subsets(nums, tgt):
    t_nums = nums.tolist()
    t_tgt = tgt
    result = []

    def local_backtrack(idx, cur_subset, cur_sum):
    
        if cur_sum == t_tgt:
            result.append(cur_subset[:])                            # use a copy so you don't mung the original 
            return 
        if cur_sum > t_tgt or idx == len(t_nums):
            return 
    
    # now try both including and excluding the current number
        cur_subset.append(t_nums[idx])
        local_backtrack(idx + 1, cur_subset, cur_sum + t_nums[idx])

        cur_subset.pop()
        local_backtrack(idx + 1, cur_subset, cur_sum)

    local_backtrack(0, [], 0)
        
    return result 

def create_bt_array(p_size, p_array, p_mask, r_tgts, c_tgts):
    b_mask = []
    for cell_index in range(p_size * p_size):
        row, column, row_nums, col_nums, row_mask, col_mask, row_tgt, col_tgt, cell_value = bt_determine_row_column(cell_index, 
                                                                                r_tgts, c_tgts, 
                                                                                p_array, p_mask, p_size)

        row_subsets = bt_find_subsets(row_nums, row_tgt, row_mask)
        col_subsets = bt_find_subsets(col_nums, col_tgt, col_mask)

        valid_cell = is_cell_valid(cell_value, row_subsets, col_subsets)

        if valid_cell == False:
            p_mask[row, column] = -1

    # print(puzzle_mask)
    # redo mask for backtrack: change -1 to 0, 0 to plus one -- just add 1 to everything
    changer_mask = np.ones([p_size, p_size], dtype=int)
    b_mask = p_mask + changer_mask

    # print(bt_mask)
    # now multiply bt_mask * puzzle -- valid numbers remain, invalids replaced by zeros
    bt_p_array = p_array * b_mask

    # print(bt_puzzle_array)

    # one more scrub with new array for invalid numbers
    for cell_index in range(p_size * p_size):
        row, column, row_nums, col_nums, row_mask, col_mask, row_tgt, col_tgt, cell_value = bt_determine_row_column(cell_index, 
                                                                                r_tgts, c_tgts, 
                                                                                bt_p_array, b_mask, p_size)

        row_subsets = bt_just_find_subsets(row_nums, row_tgt)
        col_subsets = bt_just_find_subsets(col_nums, col_tgt)

        valid_cell = is_cell_valid(cell_value, row_subsets, col_subsets)

        if valid_cell == False:
            b_mask[row, column] = 0

    b_p_array = p_array * b_mask

    return b_p_array