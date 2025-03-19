# mask_operations.py
# Bill Hanson
#
# Takes a set of combinations and finds both invalid and 
#   requird numbers

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