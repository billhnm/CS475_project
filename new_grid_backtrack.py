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

def create_masks(p_size):
    # sets up boolean masks given puzzle size
    c_mask = np.zeros([p_size], dtype=int)
    r_mask = np.zeros([p_size], dtype=int)
    p_mask = np.zeros([p_size, p_size], dtype=int)
    return c_mask, r_mask, p_mask

def initial_cut(p_size, p_array, r_tgt, c_tgt, p_mask):
    # initial cut to mask values larger than row or column target
    for i in range(p_size):
        for j in range(p_size):
            if p_array[i,j] > r_tgt[i] or p_array[i,j] > c_tgt[j]:
                p_mask[i,j] = -1
    return p_mask

def determine_row_column(c_index, r_tgts, c_tgts, p_array, p_mask, p_size):
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

def find_subsets(nums, tgt, mask):
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

puzzle_array, puzzle_size, column_targets, row_targets = load_puzzle_csv()

column_mask, row_mask, puzzle_mask = create_masks(puzzle_size)

# now make the initial cut
puzzle_mask = initial_cut(puzzle_size, puzzle_array, row_targets, column_targets, puzzle_mask)

# general approach: set first value to true, then check if it fits into target 
#   for both its row and column
#   if so, mark it and try the next value to see if sum is <= target

print(puzzle_array)
print(puzzle_mask)


for cell_index in range(puzzle_size * puzzle_size):
    row, column, row_nums, col_nums, row_mask, col_mask, row_tgt, col_tgt, cell_value = determine_row_column(cell_index, 
                                                                                row_targets, column_targets, 
                                                                                puzzle_array, puzzle_mask, puzzle_size)

    row_subsets = find_subsets(row_nums, row_tgt, row_mask)
    col_subsets = find_subsets(col_nums, col_tgt, col_mask)

    valid_cell = is_cell_valid(cell_value, row_subsets, col_subsets)

    if valid_cell == False:
        puzzle_mask[row, column] = -1

print(puzzle_mask)
