import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

df = pd.read_csv('Reddit Tech Salary Sheet (Responses) - Form Responses 1.csv')
conn = sqlite3.connect(':memory:')
df.to_sql('salaries', conn, index=False, if_exists='replace')

salary_column = 'Total Base Salary in 2018 (in USD)'

sql_check = f"""
SELECT 
    COUNT(*) as total_entries,
    SUM(CASE WHEN `{salary_column}` IS NULL THEN 1 ELSE 0 END) as null_count
FROM salaries;
"""

result = pd.read_sql_query(sql_check, conn)
print("="*60)
print("VERSION B: MODERATE CLEANING")
print("="*60)
print("\nOriginal Data:")
print(result.to_string(index=False))

sql_cleaned = f"""
SELECT 
    `{salary_column}` as salary
FROM salaries
WHERE `{salary_column}` IS NOT NULL
  AND `{salary_column}` >= 30000
  AND `{salary_column}` <= 350000;
"""

salaries_cleaned_df = pd.read_sql_query(sql_cleaned, conn)
salaries_cleaned = salaries_cleaned_df['salary']

sql_stats = f"""
SELECT 
    COUNT(*) as entries_after_cleaning,
    AVG(`{salary_column}`) as avg_salary,
    MIN(`{salary_column}`) as min_salary,
    MAX(`{salary_column}`) as max_salary
FROM salaries
WHERE `{salary_column}` IS NOT NULL
  AND `{salary_column}` >= 30000
  AND `{salary_column}` <= 350000;
"""

stats = pd.read_sql_query(sql_stats, conn)

sql_removed = f"""
SELECT 
    (SELECT COUNT(*) FROM salaries WHERE `{salary_column}` IS NOT NULL) as before,
    (SELECT COUNT(*) FROM salaries 
     WHERE `{salary_column}` IS NOT NULL 
     AND `{salary_column}` >= 30000 
     AND `{salary_column}` <= 350000) as after;
"""

removed_stats = pd.read_sql_query(sql_removed, conn)
total_removed = removed_stats['before'].iloc[0] - removed_stats['after'].iloc[0]

avg_salary = stats['avg_salary'].iloc[0]

print("\nCleaning Rules Applied:")
print("  • Removed null values")
print("  • Removed salaries < $30,000 (part-time/interns)")
print("  • Removed salaries > $350,000 (extreme outliers)")

print(f"\nData Points: {stats['entries_after_cleaning'].iloc[0]:,}")
print(f"Removed: {total_removed:,} entries ({total_removed/removed_stats['before'].iloc[0]*100:.1f}%)")

print("\n" + "="*60)
print(f"AVERAGE SALARY: ${avg_salary:,.2f}")
print("="*60)

print(f"\nMin: ${stats['min_salary'].iloc[0]:,.2f}")
print(f"Max: ${stats['max_salary'].iloc[0]:,.2f}")
print(f"Median: ${salaries_cleaned.median():,.2f}")

plt.figure(figsize=(14, 7))
plt.hist(salaries_cleaned, bins=60, edgecolor='black', alpha=0.75, color='#2ecc71')
plt.axvline(avg_salary, color='red', linestyle='--', linewidth=2.5, 
            label=f'Average: ${avg_salary:,.0f}')
plt.axvline(salaries_cleaned.median(), color='blue', linestyle=':', linewidth=2, 
            label=f'Median: ${salaries_cleaned.median():,.0f}')
plt.xlabel('Salary (USD)', fontsize=13, fontweight='bold')
plt.ylabel('Frequency', fontsize=13, fontweight='bold')
plt.title('Version B: Moderate Cleaning\nIncludes High Earners & Senior Roles', 
          fontsize=15, fontweight='bold', pad=20)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

conn.close()