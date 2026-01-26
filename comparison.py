"""
Comparison: Raw vs Cleaned vs Strict

This is the WOW moment - see how different cleaning approaches change the results.

Approach: Python + SQL

This comparison uses both:
- SQL queries to calculate averages for each version
- Python for visualization and comparison analysis

Each version's average is calculated using SQL, then compared using Python.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

# Load CSV with Python
df = pd.read_csv('Reddit Tech Salary Sheet (Responses) - Form Responses 1.csv')

# Create in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Load data into SQL database
df.to_sql('salaries', conn, index=False, if_exists='replace')

salary_column = 'Total Base Salary in 2018 (in USD)'

# SQL Queries for all three versions

# Version A: Raw (no cleaning) - SQL Query
sql_raw = f"""
SELECT 
    AVG(`{salary_column}`) as avg_salary,
    COUNT(*) as data_points
FROM salaries;
"""
result_raw = pd.read_sql_query(sql_raw, conn)
avg_raw = result_raw['avg_salary'].iloc[0]
salaries_raw = df[salary_column].dropna()

# Version B: Basic cleaning - SQL Query
sql_basic = f"""
SELECT 
    AVG(`{salary_column}`) as avg_salary,
    COUNT(*) as data_points
FROM salaries
WHERE `{salary_column}` IS NOT NULL
  AND `{salary_column}` <= 300000;
"""
result_basic = pd.read_sql_query(sql_basic, conn)
avg_basic = result_basic['avg_salary'].iloc[0]
sql_basic_data = f"SELECT `{salary_column}` as salary FROM salaries WHERE `{salary_column}` IS NOT NULL AND `{salary_column}` <= 300000;"
salaries_basic_df = pd.read_sql_query(sql_basic_data, conn)
salaries_basic = salaries_basic_df['salary']

# Version C: Strict cleaning - SQL Query
# First calculate percentile
salaries_no_null = df[salary_column].dropna()
percentile_98_5 = salaries_no_null.quantile(0.985)

sql_strict = f"""
SELECT 
    AVG(`{salary_column}`) as avg_salary,
    COUNT(*) as data_points
FROM salaries
WHERE `{salary_column}` IS NOT NULL
  AND `{salary_column}` <= {percentile_98_5}
  AND `{salary_column}` >= 20000
  AND `{salary_column}` <= 250000;
"""
result_strict = pd.read_sql_query(sql_strict, conn)
avg_strict = result_strict['avg_salary'].iloc[0]
sql_strict_data = f"SELECT `{salary_column}` as salary FROM salaries WHERE `{salary_column}` IS NOT NULL AND `{salary_column}` <= {percentile_98_5} AND `{salary_column}` >= 20000 AND `{salary_column}` <= 250000;"
salaries_strict_df = pd.read_sql_query(sql_strict_data, conn)
salaries_strict = salaries_strict_df['salary']

# Create comparison table
comparison_data = {
    'Version': ['Raw', 'Cleaned', 'Strict'],
    'Avg Salary': [f'${avg_raw:,.0f}', f'${avg_basic:,.0f}', f'${avg_strict:,.0f}'],
    'Data Points': [int(result_raw['data_points'].iloc[0]), int(result_basic['data_points'].iloc[0]), int(result_strict['data_points'].iloc[0])]
}

comparison_df = pd.DataFrame(comparison_data)
print("="*60)
print("COMPARISON TABLE")
print("="*60)
print(comparison_df.to_string(index=False))
print("="*60)

# Visual comparison: Bar chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart comparing averages
versions = ['Raw', 'Cleaned', 'Strict']
averages = [avg_raw, avg_basic, avg_strict]
colors = ['red', 'green', 'orange']

bars = ax1.bar(versions, averages, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_ylabel('Average Salary (USD)', fontsize=12)
ax1.set_title('Average Salary Comparison\nHow Cleaning Changes the Story', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, avg in zip(bars, averages):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'${avg:,.0f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Overlay distribution comparison
ax2.hist(salaries_raw.dropna(), bins=50, alpha=0.5, label='Raw', color='red', edgecolor='black')
ax2.hist(salaries_basic, bins=50, alpha=0.5, label='Cleaned', color='green', edgecolor='black')
ax2.hist(salaries_strict, bins=50, alpha=0.5, label='Strict', color='orange', edgecolor='black')
ax2.axvline(avg_raw, color='red', linestyle='--', linewidth=2, alpha=0.7)
ax2.axvline(avg_basic, color='green', linestyle='--', linewidth=2, alpha=0.7)
ax2.axvline(avg_strict, color='orange', linestyle='--', linewidth=2, alpha=0.7)
ax2.set_xlabel('Salary (USD)', fontsize=12)
ax2.set_ylabel('Frequency', fontsize=12)
ax2.set_title('Distribution Comparison', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Calculate the difference
difference_raw_cleaned = avg_raw - avg_basic
difference_cleaned_strict = avg_basic - avg_strict
difference_raw_strict = avg_raw - avg_strict

print(f"\n{'='*60}")
print("IMPACT ANALYSIS")
print(f"{'='*60}")
print(f"Raw vs Cleaned: ${difference_raw_cleaned:,.2f} difference ({difference_raw_cleaned/avg_raw*100:.1f}% lower)")
print(f"Cleaned vs Strict: ${difference_cleaned_strict:,.2f} difference ({difference_cleaned_strict/avg_basic*100:.1f}% lower)")
print(f"Raw vs Strict: ${difference_raw_strict:,.2f} difference ({difference_raw_strict/avg_raw*100:.1f}% lower)")
print(f"{'='*60}")

# Close database connection
conn.close()

