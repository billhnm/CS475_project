# DP Subsets
# Bill Hanson

# Given a list of integers, determine all subsets that add up to a given number
#   Return the list of subsets, along with any number that is not in any subset

# List of numbers for testing
# numbers = [4, 7, 2, 1, 9, 5]
# target = 20

# Imports
import numpy as np

# 2nd cut: use dynamic programming
def dp_find_subsets(nums, target, l_mask):
    # Uses dynamic program to find all subsets of a list summing to target
    
    val_combos = []
    t_nums = nums.copy()          # save original numbers to reset mask
    t_mask = l_mask.copy()  

    # First, check for masked variables
        # don't consider masked numbers 
    for i in range(len(nums) + 1, -1, -1):      # iterate backwards to avoid index issues
        if l_mask[i] == 1: 
            # required number: decrement the target and don't include it
            target = target - nums[i]
            t_nums = np.delete(t_nums, i)
        elif l_mask[i] == -1:
            # invalid number: don't include it
            t_nums = np.delete(t_nums, i)
    
      # Initialize the list of lists
    dp = [[] for _ in range(target + 1)]
    dp[0] = [[]]  # Base case: one way to make sum 0 - the empty subset

    for num in nums:
        for i in range(target, num - 1, -1):
            for subset in dp[i - num]:
                dp[i].append(subset + [num])
    
    val_combos = dp[target]

    if len(val_combos) == 1:                    # Done if only 1 valid combo left
        for k in range(len(nums)):
            if (nums[k] in val_combos[0]) and (t_mask[k] == 0): # only reset mask if not already set
                t_mask[k] = 1
            else:
                if t_mask[k] == 0:                  # Don't reset if required
                    t_mask[k] = -1                  # Unused numbers not required

    return val_combos, t_mask





