# simple_backtrack.py
# Bill Hanson
#
# solve a single-row problem using backtracking
#
# imports
import numpy as np

prob = [7, 8, 7, 6, 1, 7]
target = 9

# general approach: set first value to true, then check if <= target
#   if so, mark it and try the next value to see if sum is <= target

problem = [9, 9, 8, 6, 2, 8]
target = 18

def subset_sum(nums, tgt):
    result = []
    def back_track(index, cur_subset, cur_sum):
        if cur_sum == tgt:
            result.append(cur_subset[:])                            # use a copy so you don't mung the original 
            return 
        if cur_sum > target or index == len(nums):
            return 
    
    # now try both including and excluding the current number
        cur_subset.append(nums[index])
        back_track(index + 1, cur_subset, cur_sum + nums[index])

        cur_subset.pop()
        back_track(index + 1, cur_subset, cur_sum)

    back_track(0, [], 0)
    
    return result

# main

final_result = subset_sum(problem, target)

print(final_result)

