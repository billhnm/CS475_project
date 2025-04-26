# Build Animation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === Step 1: Load Puzzle States ===
xls_path = 'all_temp2_outputs.xlsx'  # Path to your file

df = pd.read_excel(xls_path, header=None)

TARGET_COLS = 15

def clean_row(row):
    values = row.dropna().values
    if len(values) < TARGET_COLS:
        return np.append(values, [''] * (TARGET_COLS - len(values)))
    return values[:TARGET_COLS]

puzzles = []
temp_grid = []

for _, row in df.iterrows():
    if row.isnull().all():
        if temp_grid:
            puzzles.append(np.array(temp_grid))
            temp_grid = []
    else:
        cleaned = clean_row(row)
        temp_grid.append(cleaned)

if temp_grid:
    puzzles.append(np.array(temp_grid))

puzzle_states = []
for grid in puzzles:
    # Force the entire grid to object type early
    grid_obj = grid.astype(object)
    # Now replace '' (empty string) with np.nan safely
    processed = np.where(grid_obj == '', np.nan, grid_obj)
    puzzle_states.append(processed)

# === Step 2: Set Up Animation ===
fig, ax = plt.subplots(figsize=(7, 7))
plt.axis('off')

def get_diff_mask(prev, curr):
    return (prev != curr) & ~(pd.isnull(prev) & pd.isnull(curr))

def update(frame):
    ax.clear()
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('white')

    current = puzzle_states[frame]
    prev = puzzle_states[frame - 1] if frame > 0 else np.full_like(current, '', dtype=object)
    diff_mask = get_diff_mask(prev, current)

    for i in range(15):
        for j in range(15):
            val = current[i, j]
            color = 'black'
            weight = 'normal'
            if diff_mask[i, j]:
                color = 'red'
                weight = 'bold'
            if val and val != 'nan':
                ax.text(j + 0.5, 14.5 - i, val, ha='center', va='center', fontsize=10, color=color, fontweight=weight)
    return []

# === Step 3: Export Animation ===
output_video_path = 'puzzle_solution_animation.mp4'

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(puzzle_states),
    blit=False,
    repeat=False
)

ani.save(output_video_path, writer='ffmpeg', fps=1)
print(f"Animation saved as {output_video_path}")