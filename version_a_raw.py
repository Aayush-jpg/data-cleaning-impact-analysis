"""
Version A: Raw Data (No Cleaning)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

df = pd.read_csv('Reddit Tech Salary Sheet (Responses) - Form Responses 1.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('salaries', conn, index=False, if_exists='replace')
print(f"Total rows: {len(df)}")
print(f"\nFirst few rows:")
print(df.head())
salary_column = 'Total Base Salary in 2018 (in USD)'
sql_stats = f"""
SELECT 
    COUNT(*) as total_entries,
    SUM(CASE WHEN `{salary_column}` IS NULL THEN 1 ELSE 0 END) as null_count,
    SUM(CASE WHEN `{salary_column}` IS NOT NULL THEN 1 ELSE 0 END) as non_null_count,
    AVG(`{salary_column}`) as avg_salary
FROM salaries;
"""

result = pd.read_sql_query(sql_stats, conn)
print("\nSQL Query Results:")
print(result.to_string(index=False))
salaries = df[salary_column]

print(f"\n{'='*50}")
print(f"AVERAGE SALARY (RAW): ${result['avg_salary'].iloc[0]:,.2f}")
print(f"{'='*50}")
avg_salary = result['avg_salary'].iloc[0]
plt.figure(figsize=(12, 6))
salaries_plot = salaries.dropna()

plt.hist(salaries_plot, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(avg_salary, color='red', linestyle='--', linewidth=2, label=f'Average: ${avg_salary:,.0f}')
plt.xlabel('Salary (USD)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Salary Distribution - Raw Data (No Cleaning)\nAll Outliers Included', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Min salary: ${salaries_plot.min():,.2f}")
print(f"Max salary: ${salaries_plot.max():,.2f}")
print(f"Median salary: ${salaries_plot.median():,.2f}")
conn.close()

