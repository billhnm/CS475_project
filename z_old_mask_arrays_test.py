# masked arrays testing

import numpy as np
import numpy.ma as ma
from itertools import combinations

def bf_find_combinations(input_list, length):
    # Generates all combinations of a list with given length and returns a list of combination tuples  
    return list(combinations(input_list, length))

ta = np.array(range(1,6), dtype = int)
print(ta)
l_ta = ta.tolist()

mta = ma.masked_array(ta, mask=[0,0,0,0,0])
print(mta)

# now mask a value
mta[2:4]  = ma.masked
l_mta = mta.tolist()
print(l_mta)
l_mta = [x for x in l_mta if x is not None]
print(l_mta)

combos = bf_find_combinations(l_ta, 2)
print(combos)
combos2 = bf_find_combinations(l_mta, 2)
print(combos2)

'''
combos2a = list(combos2)
print(combos2a)
print(combos2a[0])
for i in range(len(combos2a)):
    combos2a[i] = [x for x in combos2a[i] if x is not None]
print(combos2a)
'''