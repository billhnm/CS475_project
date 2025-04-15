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
from scipy.optimize import curve_fit
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.metrics import mean_squared_error, r2_score

# set up file import
cur_dir = os.getcwd()
work_dir = 'CS475_project'
'''
bf_fname = 'Brute_Force_25_04_08_1146.pkl'
bf_input_name = os.path.join(cur_dir, bf_fname)
dp_fname = 'Dynamic_Programming_25_04_08_1146.pkl'
dp_input_name = os.path.join(cur_dir, dp_fname)
bt_fname = 'Backtracking_25_04_08_1146.pkl'
bt_input_name = os.path.join(cur_dir, bt_fname)

df_bf = pd.read_pickle(bf_input_name)
df_dp = pd.read_pickle(dp_input_name)
df_bt = pd.read_pickle(bt_input_name)
# rename 'Puzzle size' to 'Puzzle_size'
# df_all = df_all.rename(columns = {'Puzzle size': 'Puzzle_size'})
# put them all into one dataframe
df_all = pd.concat([df_bf, df_dp, df_bt], ignore_index=True)
'''
# read into df_all
df_fname = 'All_runs_combined.pkl'
df_input_name = os.path.join(cur_dir, work_dir, df_fname)
df_all = pd.read_pickle(df_input_name)

'''
# count number solved by each algo
bt_solved = len(df_all[(df_all['Algorithm'] == 'Backtracking') & (df_all['Output string'] == 'Solved')])
print(f'{bt_solved}% of puzzles solved by Backtracking')
bf_solved = len(df_all[(df_all['Algorithm'] == 'Brute_Force') & (df_all['Output string'] == 'Solved')])
print(f'{bf_solved}% of puzzles solved by Brute Force')
dp_solved = len(df_all[(df_all['Algorithm'] == 'Dynamic_Programming') & (df_all['Output string'] == 'Solved')])
print(f'{dp_solved}% of puzzles solved by Dynamic Programming')

end_conditions = df_all['Output string'].unique
print(end_conditions)
'''
# separate by algorithm
df_bt = df_all.loc[df_all['Algorithm'] == 'Backtracking']
df_bf = df_all.loc[df_all['Algorithm'] == 'Brute_Force']
df_dp = df_all.loc[df_all['Algorithm'] == 'Dynamic_Programming']
#df_bf_dp = df_all.loc[df_all['Algorithm'] != 'Backtracking']

#print(df_bt.head)
# put them all into one dataframe
# df_all = pd.concat([r8_df, r10_df, r12_df, r15_df, r20_df], ignore_index=True)
#df_bf_dp = pd.concat([bf_df, dp_df], ignore_index=True)


'''
# looks like backtracking runtimes grows exponentially
# set up exponential curve fit
x = df_bt['Puzzle size']
x = x ** 2                  # regress on number of spots
y = df_bt['Runtime']
y = y[y > 0]                # Avoid log(0)
x = x.loc[y.index]

log_y = np.log(y)

# perform linear regression on log(y)
coeffs = np.polyfit(x, log_y, deg = 1)

log_a, log_b = coeffs[1], coeffs[0]

#print(coeffs)
#print(log_a, log_b)

a = np.exp(log_a)
b = np.exp(log_b)

# predictions
y_fit = a * (b ** x)

# plot the results
plt.scatter(x, y, label = 'Runtime')
plt.plot(x, y_fit, color = 'green', label = 'Exponential Fit')
plt.legend()
plt.suptitle('Backtracking: Runtime vs. Puzzle Size')
plt.title('Exponential Fit: y = a * b^x')
plt.show()

print(f'Fitted model: y = {a:.3e} * {b:.3f}^x')

# look at fit quality via r2 and MSE
r2 = r2_score(y, y_fit)
mse = mean_squared_error(y, y_fit)

print(f'R²: {r2:.4f}, MSE: {mse:.4f}')


# looks like dp or bf runtimes grows non-linearly
# set up polynomical curve fit
x = df_bf['Puzzle size']
x = x                   # regress on number of spots
y = df_bf['Runtime']
# y = y[y > 0]                # only needed for log(0)
x = x.loc[y.index]


# perform linear regression on log(y)
coeffs = np.polyfit(x, y, deg = 2)
#print(coeffs)
poly_eqn = np.poly1d(coeffs)
print(poly_eqn)

a, b, c = coeffs[2], coeffs[1], coeffs[0]

# predictions
y_fit = a + b*x + c*(x**2)

# plot the results
plt.scatter(x, y, label = 'Runtime')
plt.plot(x, y_fit, color = 'green', label = 'Polynomial Fit')
plt.legend()
plt.suptitle('Brute Force: Runtime vs. Puzzle Size')
plt.title('Polynomial Fit: y = a + b*x + c*(x**2)')
plt.show()

print(f'Fitted model: y = {a:.3e} + {b:.3e}*x + {c:.3e}*x^2')

# look at fit quality via r2 and MSE
r2 = r2_score(y, y_fit)
mse = mean_squared_error(y, y_fit)

print(f'R²: {r2:.4f}, MSE: {mse:.4f}')
'''

'''
# OLS regression on BF and DP  runtime vs puzzle size
bf_result = sm.OLS.from_formula(formula = 'Runtime ~ Puzzle_size', data = df_bf).fit()
dp_result = sm.OLS.from_formula(formula = 'Runtime ~ Puzzle_size', data = df_dp).fit()

print(bf_result.summary())
print(bf_result.summary())
'''
'''
# initial description and summary stats
summary1 = df_all.groupby(['Puzzle size', 'Algorithm'])[['Runtime']].describe()
print(summary1)
summary2 = df_all.groupby(['Puzzle size', 'Algorithm'])[['Iterations']].describe()
print(summary2)

print()
df_median = df_all.groupby(['Puzzle size', 'Algorithm'])[['Runtime']].median() 
df_skew = df_all.groupby(['Puzzle size', 'Algorithm'])[['Runtime']].skew()
print(f'Median: {df_median}')
print()
print(f'Skew: {df_skew}')
print()
'''

# Create initial boxplots and histogram
'''
# Line plot
sns.lineplot(data = df_bf_dp, x = 'Puzzle size', y = 'Runtime',  hue = 'Algorithm', estimator = 'mean')
plt.suptitle("Runtime by Puzzle Size and Algorithm")
plt.title('Brute Force vs Dynamic Programming', fontsize = 10)
plt.show()
'''

sns.boxplot(x = 'Puzzle size', y = 'Runtime', hue = 'Algorithm', data = df_bt)
plt.suptitle("Runtime Distribution by Puzzle Size")
plt.title('Backtracking', fontsize = 10)
plt.show()

'''
# histogram
sns.histplot(data = df_bf_dp, x = 'Runtime', hue = 'Puzzle size', bins = 45, kde = False, element = 'step')
plt.suptitle('Runtime Distribution by Puzzle Size')
plt.title('Brute Force and Dynamic Programming', fontsize = 10)
plt.show()

sns.histplot(data = df_bt, x = 'Iterations', bins = 60, kde = False, element = 'step')
plt.title('Pre-filtered Grid Distribution for Backtracking, n=100')
plt.xlabel('Number Pre-filtered out of 64 possible')
plt.show()


# Save the combined file 
output_fname = 'All_8.2_combined.pkl'
combined_name = os.path.join(cur_dir, output_fname)
df_all.to_pickle(combined_name)
'''