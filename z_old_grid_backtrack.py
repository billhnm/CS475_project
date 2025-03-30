# grid_backtrack.py
# Bill Hanson
#
# solve a single-solution grid problem using backtracking
#
# imports
import numpy as np

def load_puzzle_csv():
    # takes a csv file and returns the puzzle_array, puzzle size, 
    #    and row and column targets
    # input from csv
    input_a = np.loadtxt("x_8x8_1.csv", 
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

# general approach: set first value to true, then check if <= target
#   if so, mark it and try the next value to see if sum is <= target

puzzle_array, puzzle_size, column_target, row_target = load_puzzle_csv()

print(column_target)
print(row_target)
print(puzzle_array)




def solve_puzzle(p_array, p_size, c_tgt, r_tgt):
    iter = 0
    p_mask = [[0 for _ in range(p_size)] for _ in range(p_size)]

    def is_subset_valid(row, col, cell_value, include):
        def subset_sum_exists(values, target):
            if target == 0:                     # target is 0, subset exists
                return True
            if target < 0 or len(values) == 0:  # target is negative or no values left - no valid subset
                return False
            
            # include the first value
            if subset_sum_exists(values[1:], target - values[0]):
                return True
            # exclude the first value
            return subset_sum_exists(values[1:], target)    
        
        remaining_row_vals = [p_array[row][j] for j in range(p_size) if j != col and p_mask[row][j] == 0]
        remaining_col_vals = [p_array[i][col] for i in range(p_size) if i != row and p_mask[i][col] == 0]

        # adjust tgts based on include/exclude
        if include:
            row_target = r_tgt[row] - cell_value
            col_target = c_tgt[col] = cell_value
        else:
            row_target = r_tgt[row]
            col_target = c_tgt[col]
    
        # now check for valid row and col subsets
        return subset_sum_exists(remaining_row_vals, row_target) and subset_sum_exists(remaining_col_vals, col_target)

    def back_track(cell_index):  
                                         # step through grid cell-wise
        if cell_index == p_size * p_size: 
            # check to see if we're done              
            if all(r_tgt[i] == 0 for i in range(p_size)) and all(c_tgt[j] == 0 for j in range(p_size)):
                return True
            else:
                return False
        
        # cell index (1:mxm) converted to row, column
        row = cell_index // p_size
        col = cell_index % p_size

        # skip if mask != 0
        if p_mask[row][col] != 0:
            return back_track(cell_index + 1) 
        
        # Check the cell both ways
        cell_value = p_array[row][col]

        if is_subset_valid(row, col, cell_value, include=True):
            p_mask[row][col] = 1
            r_tgt[row] -= cell_value
            c_tgt[col] -= cell_value
            

            if back_track(cell_index + 1):
                return True   

            # undo the inclusion and backtrack
            p_mask[row][col] = 0
            r_tgt[row] += cell_value
            c_tgt[col] += cell_value   
         
        # now try excluding it
        if is_subset_valid(row, col, cell_value, include=False):
            p_mask[row][col] = -1
              
        if back_track(cell_index + 1):
            return True
        
        # backtrack from exclusion
        p_mask[row][col] = 0
        
        return False                # no solution yet
    
    # Restart backtracking at cell 0
    iter += 1
    print(iter)
    if back_track(0):
        return True, p_mask
    elif iter > 100:
        return False, p_mask
    else:
        return None, p_mask

status, final_mask = solve_puzzle(puzzle_array, puzzle_size, column_target, row_target)  


print(status)
print(final_mask)


''' Old code from simple_backtrack
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
''' 
