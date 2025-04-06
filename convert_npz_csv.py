# scratch file

import numpy as np
import pandas as pd
import os

cur_dir = os.getcwd()
work_dir = 'CS475_project'
new_wd = os.path.join(cur_dir, work_dir)
os.chdir(new_wd)

# input_path = os.path.join(new_wd, input_name)

def load_puzzle_npz():
    # loads the puzzle from npz file where row and column targets
    #   are already defined
    puzzle_data = np.load('s20x20_1.npz')
    puzzle_a = puzzle_data['arr_0']
    r_tgt = puzzle_data['arr_1']
    c_tgt = puzzle_data['arr_2']
    p_size = puzzle_a.shape[0]

    return puzzle_a, p_size, c_tgt, r_tgt

array, size, ct, rt = load_puzzle_npz()
new_ct = np.insert(ct,0,0)
new_p = np.insert(array, 0, rt, axis = 1)
full_p = np.insert(new_p, 0, new_ct, axis=0)


f_name = 's20x20_1_conv.csv'
file_path = os.path.join(new_wd, f_name)
np.savetxt(file_path, full_p, delimiter=',', fmt='%d')


