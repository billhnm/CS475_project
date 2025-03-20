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

        if r_tgt[row] >= cell_value and c_tgt[col] >= cell_value:
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
