# main_solver.py
# Bill Hanson
#
# Main solver logic: steps through puzzle rows and columns
#   Calls other modules for operations
#
# loads and runs appropriate modules given the type of analysis and data file
# standard imports
import numpy as np
import pandas as pd
import os
import time
import datetime
from validity_operations import find_invalid_nums, find_required_nums
from puzzle_input import load_puzzle_csv, load_puzzle_npz, create_masks, initial_cut

algo_to_run = int(input('Enter algorithm: 1 = brute force, 2 = dynamic programming, 3 = backtracking - '))

if algo_to_run == 1:
    from subset_finding import bf_find_subsets as find_subsets
    from subset_finding import bf_find_combinations
    algo_string = 'Brute_Force'
elif algo_to_run == 2:
    from subset_finding import dp_find_subsets as find_subsets
    algo_string = 'Dynamic_Programming'
elif algo_to_run == 3:
    from ortools.sat.python import cp_model
    from subset_finding import is_cell_valid, bt_determine_row_column, bt_find_subsets, bt_just_find_subsets, create_bt_array
    from validity_operations import create_bt_mask
    from new_grid_backtrack import solve_grid
    algo_string = "Backtracking"
else: 
    print('Algorithm not recognized')

# Main program

# Declare needed variables
done = False
solution_found = False
final_string = ''
output_record = []
output_list = []

# create the input names
cur_dir = os.getcwd()
work_dir = 'CS475_project'
data_dir = 'data'
file_stub = '12x12_2_'
file_type = '.csv'

#npz_name = '10x10_0.2.npz'
#npz_input_name = os.path.join(cur_dir, work_dir, npz_name)
# load the puzzle

# type_input = int(input('What type of file? 1 for csv, 2 for npz: '))

#if type_input == 1: 
#    puzzle_array, puzzle_size, col_tgt, row_tgt = load_puzzle_csv(csv_input_name)
#elif type_input == 2:
#    puzzle_array, puzzle_size, col_tgt, row_tgt = load_puzzle_npz(npz_input_name)
#else:
#    print('Unrecognized file type')

# set up loop to step through files in batch

for i in range(100):
    file_num = str(i)
    file_name = file_stub + file_num + file_type
    csv_input_name = os.path.join(cur_dir, work_dir, data_dir, file_name)
    # reset variables
    puzzle_array = []
    puzzle_mask = []
    col_tgt = []
    row_tgt = []
    main_col_mask = []
    main_row_mask = []
    valid_combos = []
    upd_col_mask = []
    upd_row_mask = []
    new_col_mask = []
    new_row_mask = []
    next_col_mask = []
    new_row_mask = []
    solution_array = []
    solution_found = False
    done = False
    output_list = []
     
    puzzle_array, puzzle_size, col_tgt, row_tgt = load_puzzle_csv(csv_input_name)

    # start timer
    start_time = time.perf_counter()

    puzzle_size = puzzle_array.shape[0]

    main_col_mask, main_row_mask, puzzle_mask = create_masks(puzzle_size)

    # Make the first cut 
    puzzle_mask = initial_cut(puzzle_size, puzzle_array, row_tgt, col_tgt, puzzle_mask)
    #print(puzzle_mask)

    if algo_to_run == 1 or algo_to_run == 2:
    # Main Row-wise solver -- calls either BF or DP functions
        iter = 0
        while not done:
            # print("Starting new iteration of the loop")
            old_puzzle_mask = puzzle_mask                   # save to check to see if we've made progress
            for i in range(puzzle_size):                    # step through the rows
                if main_row_mask[i] == 0:
                    cur_row = puzzle_array[i,:]
                    cur_row_mask = puzzle_mask[i,:]
                    cur_row_tgt = row_tgt[i]

                    valid_combos, upd_row_mask = find_subsets(cur_row, cur_row_tgt, cur_row_mask)
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
            
                    new_row_mask = find_required_nums(valid_combos, cur_row, next_row_mask)
                    if 0 not in next_row_mask:    
                        main_row_mask[i] = 1 
                    else: 
                        main_row_mask[i] = 0
                    # Update puzzle mask
                    puzzle_mask[i,:] = new_row_mask
            # End row loop

            for i in range(puzzle_size):                    # step through the columns
                if main_col_mask[i] == 0:
                    cur_col = puzzle_array[:,i]
                    cur_col_mask = puzzle_mask[:,i]
                    cur_col_tgt = col_tgt[i]

                    valid_combos, upd_col_mask = find_subsets(cur_col, cur_col_tgt, cur_col_mask)
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
                
                    new_col_mask = find_required_nums(valid_combos, cur_col, next_col_mask)
                    if 0 not in next_col_mask:    
                        main_col_mask[i] = 1 
                    else: 
                        main_col_mask[i] = 0
                    # update puzzle mask
                    puzzle_mask[:,i] = new_col_mask
            # End column loop

            # check for done, stalled, or unsolvable condition
            if np.all(puzzle_mask != 0) or (np.all(main_row_mask == 1) and np.all(main_col_mask == 1)):
                done = True
                solution_found = True
                final_string = 'Solved'
                # print(f'Solved in {iter} iterations')
            iter += 1
            if iter > 10 and np.array_equal(old_puzzle_mask, puzzle_mask):
                done = True
                final_string = 'Stalled after ' + str(iter) + ' iterations'
            if iter > 250:
                done = True
                final_string = 'Found no solution after 250 iterations'

        # change puzzle mask so invalid nums = 0
        puzzle_mask[puzzle_mask == -1] = 0
        solution_array = puzzle_mask * puzzle_array
        #print(solution_array)
        # end BF or DP solver

    if algo_to_run == 3:
        # Main BT solver
        bt_puzzle_array = create_bt_array(puzzle_size, puzzle_array, puzzle_mask, row_tgt, col_tgt)
        
        # main BT solver using solve_grid
        solution = solve_grid(bt_puzzle_array, row_tgt, col_tgt, puzzle_size) 

        # assuming we get a solution, print it out
        if solution:
            # create the (0,1) mask
            solution_mask = []
            for i in range(puzzle_size):
                rw_mask = [solution[(i, j)] for j in range(puzzle_size)]
                solution_mask.append(rw_mask)    

            # now multiply the puzzle by the mask to get the result
            # print('\nSolution Array')
            solution_array = solution_mask * puzzle_array
            final_string = 'Solved'
            iter = 1
            #print(solution_array)

        else:
            final_string = 'No backtrack solution found'
            iter = 0

    end_time = time.perf_counter()
    run_time = round(end_time - start_time, 5)
    # time_string = 'Done in ' + str(run_time) + ' seconds'

    output_list = [algo_string, puzzle_size, run_time, iter, final_string]
    output_record.append(output_list)
# 
# End main loop -- files all done

# write output record to dataframe, then write it to pickle as timestamped file

output_df = pd.DataFrame(output_record, columns = ['Algorithm', 'Puzzle size', 'Runtime', 'Iterations', 'Output string'])
time_now = datetime.datetime.now()
time_stamp = time_now.strftime('%y_%m_%d_%H%M')
cur_dir = os.getcwd()
work_dir = 'CS475_project'
output_name = algo_string + '_' + time_stamp + '.pkl'
output_path = os.path.join(cur_dir, work_dir, output_name)
output_df.to_pickle(output_path)




    
