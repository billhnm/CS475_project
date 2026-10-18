# Number Sums Puzzle Solver

Solves N×N Number Sums puzzles up to **N = 20** (400 cells), more than six times the size of the hardest commercial puzzles, and compares three AI search approaches on speed and robustness.

## Key Results

Puzzles were randomly generated with about 20% of cells in the solution (n = 100 per size).

| Puzzle size | 8×8 | 10×10 | 12×12 | 15×15 | 20×20 |
|---|---|---|---|---|---|
| **% solved: Backtracking** | 100% | 100% | 100% | 100% | 100% |
| % solved: Brute Force | 100% | 83% | 73% | 23% | 0% |
| % solved: Dynamic Programming | 100% | 83% | 73% | 23% | 0% |
| Mean runtime (s): Backtracking | 0.020 | 0.057 | 0.199 | 1.95 | 83.4 |
| Mean runtime (s): Brute Force | 0.0015 | 0.0034 | 0.0037 | 0.0059 | 0.017 |
| Mean runtime (s): Dynamic Programming | 0.0014 | 0.0031 | 0.0031 | 0.0051 | 0.012 |

**Takeaways**
- **Robustness vs. speed trade-off.** Backtracking (with constraint propagation via Google OR-Tools CP-SAT) solved every puzzle, but was ~10× slower than the others at 8×8 and ~5,000× slower at 20×20.
- **Row/column partitioning is fast but brittle.** Brute Force and Dynamic Programming solve one row or column at a time, which makes them very fast, but they stall whenever local constraints admit more than one subset. Their solve rate fell to 0% at 20×20.
- **Dynamic Programming was the fastest overall.** Runtimes were not normally distributed (Shapiro-Wilk p < 0.00001), so DP and Brute Force were compared with a permutation test; DP was significantly faster at every size (p ≤ 0.0056).
- **Suggested next step:** a hybrid solver that runs DP until it stalls, hands off to backtracking to break the impasse, then returns to DP.

Full methods, figures, and statistical analysis are in the [project report](Project_Report_BillHanson.pdf).

## The Problem

- **Given** an N×N grid of integers
- **where** each row and column has a target sum,
- **remove** integers until the remaining numbers exactly satisfy every row and column target.

This is an interlocking set of Subset Sum problems, so it is both a subset-sum problem (NP-complete) and a constraint satisfaction problem.

## Approach

- Iteratively applies a selected algorithm (Backtracking, Brute Force, or Dynamic Programming)
- Proceeds row-wise, then column-wise, across the grid
- Marks integers that must be present to satisfy a constraint, and removes integers that cannot be
- Repeats until a unique solution is found or the maximum number of iterations is reached

![Program flowchart](Puzzle_solver_flowchart.png)

## Usage

```bash
pip install -r requirements.txt
python build_puzzle.py      # generate puzzles of size N with a unique solution
python main_solver.py       # choose 1 = Brute Force, 2 = Dynamic Programming, 3 = Backtracking
```

## Files

| File | Purpose |
|---|---|
| `main_solver.py` | Main solver loop: steps through rows and columns, calling the selected algorithm |
| `subset_finding.py` | Subset-finding routines for each algorithm |
| `new_grid_backtrack.py` | Grid-level backtracking solver (OR-Tools CP-SAT) |
| `validity_operations.py`, `mask_operations.py` | Track required/eliminated cells |
| `puzzle_input.py` | Load puzzles from CSV or NPZ |
| `build_puzzle.py` | Generate N×N puzzles with unique solutions, up to N = 20 |
| `stat_analysis.py`, `overall_analysis.py` | Descriptive statistics, significance tests, and curve fits |
| `animate.py`, `build_animation.py` | Animate a solution step by step |

## Report and Presentation

- [Project Report (PDF)](Project_Report_BillHanson.pdf)
- [Video Presentation](https://youtu.be/ih_-wniEFok)
