# animate.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# declare functions

def create_animation_fancy(puzzle_states):
    """
    Create an animated MP4 showing the solving process.
    Adds a 'flash maroon' → 'fade gray' effect before numbers disappear.
    """

    fig, ax = plt.subplots(figsize=(7, 7))
    plt.axis('off')

    def get_diff_mask(prev, curr):
        """Find which cells changed between two puzzle states."""
        return (prev != curr) & ~(pd.isnull(prev) & pd.isnull(curr))

    # Expand frames: each real frame becomes 2 subframes (flash + fade)
    expanded_states = []
    for idx in range(len(puzzle_states)):
        expanded_states.append((puzzle_states[idx], False))  # Normal frame
        expanded_states.append((puzzle_states[idx], True))   # Flash/fade frame

    def update(frame_idx):
        ax.clear()
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 15)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor('white')

        real_frame = frame_idx // 2
        flashing = (frame_idx % 2 == 1)

        current, _ = expanded_states[frame_idx]
        prev = puzzle_states[real_frame - 1] if real_frame > 0 else np.full_like(current, '', dtype=object)
        diff_mask = get_diff_mask(prev, current)

        for i in range(current.shape[0]):
            for j in range(current.shape[1]):
                val = current[i, j]
                color = 'black'
                weight = 'normal'
                if diff_mask[i, j]:
                    if flashing:
                        color = 'dimgray'  # fade to gray on second subframe
                    else:
                        color = 'maroon'   # flash maroon on first subframe
                    weight = 'bold'
                if val != '':
                    ax.text(j + 0.5, current.shape[0] - 0.5 - i, val, ha='center', va='center', fontsize=10, color=color, fontweight=weight)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(expanded_states),
        init_func=lambda: None,
        blit=False,
        repeat=False
    )

    output_path = 'puzzle_solution_animation_fancy.mp4'
    ani.save(output_path, writer='ffmpeg', fps=2)  # Faster FPS to compensate for double frames
    print(f"Fancy animation saved to {output_path}")


def create_animation(puzzle_states):
    """
    Create an animated MP4 showing the step-by-step solving of a subset sum puzzle.
    Highlights disappearing numbers in red before removing them.
    
    Args:
        puzzle_states (list of np.array): List of 15x15 puzzle states as numpy arrays (dtype=object).
    """
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.axis('off')

    def get_diff_mask(prev, curr):
        """Find which cells changed between two puzzle states."""
        return (prev != curr) & ~(pd.isnull(prev) & pd.isnull(curr))

    def update(frame):
        ax.clear()
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 15)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor('white')  # Background white
        
        current = puzzle_states[frame]
        prev = puzzle_states[frame - 1] if frame > 0 else np.full_like(current, '', dtype=object)
        diff_mask = get_diff_mask(prev, current)

        for i in range(current.shape[0]):
            for j in range(current.shape[1]):
                val = current[i, j]
                color = 'black'
                weight = 'normal'
                if diff_mask[i, j]:
                    color = 'maroon'  # Highlight changes in maroon (matches your theme)
                    weight = 'bold'
                if val != '':
                    ax.text(j + 0.5, current.shape[0] - 0.5 - i, val, ha='center', va='center', fontsize=10, color=color, fontweight=weight)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(puzzle_states),
        init_func=lambda: None,
        blit=False,
        repeat=False
    )

    output_path = 'puzzle_solution_animation.mp4'
    ani.save(output_path, writer='ffmpeg', fps=1)
    print(f"Animation saved to {output_path}")


data = np.load('steps_Dynamic_Programming25_04_24_1849.npz')

steps = [data[key] for key in data]
'''
print(f'number of steps: {len(steps)}')
for i in range(5):
    print(steps[i])

print(steps[-1])
'''
temp2 = np.full((15, 15), '', dtype=str)

puzzle_states = []

# Save the starting board
puzzle_states.append(np.array(steps[0], dtype=object))

for i in range(2, len(steps), 2):
    temp1 = steps[i] * steps[0]

    # Build temp2 fresh each time
    temp2 = [['' for _ in range(15)] for _ in range(15)]  # Start blank

    for j in range(15):
        for k in range(15):
            if temp1[j][k] >= 0:
                temp2[j][k] = str(steps[0][j][k])

    puzzle_states.append(np.array(temp2, dtype=object))  # Append as array

create_animation_fancy(puzzle_states)