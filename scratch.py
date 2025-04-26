# scratch.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

data = np.load('steps_Dynamic_Programming25_04_24_1849.npz')

steps = [data[key] for key in data]
'''
print(f'number of steps: {len(steps)}')
for i in range(5):
    print(steps[i])

print(steps[-1])
'''
temp2 = np.full((15, 15), '', dtype=str)

# Initialize an empty DataFrame to store all outputs
all_outputs = pd.DataFrame()
steps0_df = pd.DataFrame(steps[0])
all_outputs = all_outputs = pd.concat([all_outputs, steps0_df, pd.DataFrame([[''] * 15])], ignore_index=True)  # Add a blank row as a separator

for i in range(2, len(steps), 2):
    soln = 0
    temp1 = steps[i] * steps[0]

    for j in range(15):
        for k in range(15):
            if temp1[j][k] >= 0:
                temp2[j][k] = str(steps[0][j][k])
                soln += 1

    temp2_df = pd.DataFrame(temp2)  # Convert temp2 to a pandas DataFrame
    all_outputs = pd.concat([all_outputs, temp2_df, pd.DataFrame([[''] * 15])], ignore_index=True)  # Add a blank row as a separator

all_outputs.to_excel('all_temp2_outputs.xlsx', index=False, header=False)  # Save to Excel file