# scratch.py

from math import perm

n = 8

total8 = sum(perm(n, k) for k in range(1, n+1))

n = 20
total20 = sum(perm(n, k) for k in range(1, n+1))

print(total8)

print(f'{total20:e}')