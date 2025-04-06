# stat_analysis.py
# Bill Hanson
#
# Performs statistical analysis of CS475 data. 
#   Includes plots, descriptive stats, paired t-tests and ANOVA

# Imports
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel, f_oneway, shapiro
import statsmodels.api as sm
from statsmodels.formula.api import ols

# set up file import
cur_dir = os.getcwd()
work_dir = 'CS475_project'
bt_fname = 'Backtracking_25_04_06_0503.pkl'
bt_input_name = os.path.join(cur_dir, work_dir, bt_fname)
bf_fname = 'Brute_Force_25_04_05_1946.pkl'
bf_input_name = os.path.join(cur_dir, work_dir, bf_fname)  
dp_fname = 'Dynamic_Programming_25_04_05_1947.pkl'
dp_input_name = os.path.join(cur_dir, work_dir, dp_fname)


bf_df = pd.read_pickle(bf_input_name)
bt_df = pd.read_pickle(bt_input_name)
dp_df = pd.read_pickle(dp_input_name) 
 
# add puzzle index for paired comparisons
bf_df['puzzle_id'] = bf_df.index
bt_df['puzzle_id'] = bt_df.index
dp_df['puzzle_id'] = dp_df.index

# put them all into one dataframe
df_all = pd.concat([bf_df, bt_df, dp_df], ignore_index=True)
df_bf_dp = pd.concat([bf_df, dp_df], ignore_index=True)

# initial description and summary stats
summary1 = df_all.groupby('Algorithm')[['Runtime']].describe()
print(summary1)
summary2 = df_all.groupby('Algorithm')[['Iterations']].describe()
print(summary2)


print()
df_median = df_all.groupby('Algorithm')[['Runtime']].median() 
df_skew = df_all.groupby('Algorithm')[['Runtime']].skew()
print(f'Median: {df_median}')
print(f'Skew: {df_skew}')
print()

# Create initial boxplots and histogram
# Boxplots
sns.boxplot(x = 'Algorithm', y = 'Runtime', data = df_all, order = ['Dynamic_Programming', 'Brute_Force', 'Backtracking'])
plt.title("Runtime Distribution by Algorithm - 20x20 puzzles")
plt.show()

sns.boxplot(x = 'Algorithm', y = 'Runtime', data = df_bf_dp)
plt.suptitle("Runtime Distribution by Algorithm - 20x20 puzzles")
plt.title('Brute Force vs Dynamic Programming', fontsize = 10)
plt.show()

# histogram
sns.histplot(data = df_all, x = 'Runtime', hue = 'Algorithm', bins = 45, kde = False, element = 'step')
plt.title('Runtime Distribution by Algorithm - 20x20 puzzles')
plt.show()

sns.histplot(data = df_bf_dp, x = 'Runtime', hue = 'Algorithm', bins = 45, kde = False, element = 'step')
plt.suptitle('Runtime Distribution by Algorithm - 20x20 puzzles')
plt.title('Brute Force vs Dynamic Programming', fontsize = 10)
plt.show()

# Check for normality

for alg in df_all['Algorithm'].unique():
    stat, p = shapiro(df_all[df_all['Algorithm'] == alg]['Runtime'])
    print(f'Shapiro-Wilk for {alg} runtime: p = {p:.4f}')
print()
# result: not normally distributed for 8x8

# ANOVA

model = ols('Runtime ~ C(Algorithm)', data = df_all).fit()
anova_result = sm.stats.anova_lm(model, typ = 2)
print(anova_result)
print()

# do permutation test to check for difference in means
runtime_pivot = df_all.pivot(index='puzzle_id', columns='Algorithm', values='Runtime')

bf_vals = runtime_pivot['Brute_Force'].values
dp_vals = runtime_pivot['Dynamic_Programming'].values

# observed difference in means
obs_diff = np.mean(bf_vals) - np.mean(dp_vals)

# permutation test
n_permutations = 10000
diffs = np.zeros(n_permutations)

for i in range(n_permutations):
    combined = np.concatenate([bf_vals, dp_vals])
    np.random.shuffle(combined)
    new_bf = combined[:len(bf_vals)]
    new_dp = combined[len(bf_vals):]
    diffs[i] = np.mean(new_bf) - np.mean(new_dp)

p_val = np.mean(np.abs(diffs) >= np.abs(obs_diff))
print(f'Observed difference - BF vs DP: {obs_diff:.4f}, p-value: {p_val:.4f}')
print()

# plot the null distribution
plt.hist(diffs, bins=40, edgecolor='k')
plt.axvline(obs_diff, color='red', linestyle = '--', label = 'Observed difference')
plt.axvline(-obs_diff, color='red', linestyle = '--')
plt.title('Permutation Null Distribution')
plt.legend()
plt.show()
print()

# one-way anova using permutation test since values not normally distributed
# Observed F-statistic
groups = [df_all[df_all['Algorithm'] == alg]['Runtime'].values for alg in df_all['Algorithm'].unique()]
F_obs, _ = f_oneway(*groups)

# Permutation test
F_null = []
for _ in range(10000):
    shuffled = df_all['Runtime'].sample(frac=1, replace=False).reset_index(drop=True)
    df_perm = df_all.copy()
    df_perm['shuffled_runtime'] = shuffled
    groups_perm = [df_perm[df_perm['Algorithm'] == alg]['shuffled_runtime'].values for alg in df_perm['Algorithm'].unique()]
    F, _ = f_oneway(*groups_perm)
    F_null.append(F)

p_val = np.mean(np.array(F_null) >= F_obs)
print(f"Observed F: {F_obs:.4f}, p-value: {p_val:.4f}")

# Save the combined file 
output_fname = '20x20_combined.pkl'
combined_name = os.path.join(cur_dir, work_dir, output_fname)
df_all.to_pickle(combined_name)