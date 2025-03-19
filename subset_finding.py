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