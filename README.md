# Data Cleaning Impact Analysis

## The Question

**What is the average salary?**

A simple question. Three different answers.

## The Problem

The same dataset produces wildly different conclusions depending on how you clean it. This project demonstrates how preprocessing decisions—not the data itself—determine your results.

## The Experiment

I analyzed tech salary data using three different cleaning strategies:

### Version A: Raw Data (No Cleaning)
- Load everything
- Remove nothing
- Keep all outliers
- **Result: Completely unusable**

### Version B: Moderate Cleaning
- Remove null values
- Remove salaries < $30,000
- Remove salaries > $350,000 (extreme outliers)
- **Scope: Retains salaries between the selected thresholds**

### Version C: Conservative Cleaning
- Remove null values
- Remove salaries < $40,000
- Remove salaries > $110,000
- Remove top 3% (statistical outliers)
- **Scope: A narrower salary range; seniority is not established by these filters**

## The Results

| Version | Average | Median | Data Points | Removed |
|---------|---------|--------|-------------|---------|
| **Raw (A)** | $27,572,945 | N/A | 4,500 | 0% |
| **Moderate (B)** | $79,310 | $70,175 | 3,850 | 14% |
| **Conservative (C)** | $78,944 | $68,000 | 3,200 | 29% |

### Interpreting the comparison

The reported moderate and conservative **means** are $79,310 and $78,944, a difference of **$366**. Their **medians** are $70,175 and $68,000, a difference of **$2,175**.

Compare means with means and medians with medians. Comparing $79,310 with $68,000 mixes two different statistics.

## Why This Matters

Salary thresholds change which observations remain in the analysis. A salary cutoff alone cannot establish a person's seniority, employment type, or whether a record is an error.

The stricter version removes more observations without greatly changing the reported mean. That makes the exclusions themselves worth investigating: which groups were removed, and does the remaining sample still answer the original question?

The raw average should trigger a review of units, currencies, parsing, and extreme values before drawing conclusions.

## Key Insight

**Data is not objective. Preprocessing choices drive business decisions.**

This is the real skill in data science—not just calculating numbers, but understanding:
- What question you're actually answering
- Who you're including/excluding
- What biases your cleaning introduces
- Which version tells the story you need

The technical work (SQL, Python, statistics) is the easy part. The hard part is knowing what the numbers mean.

## Technical Implementation

**Stack:**
- Python (pandas, matplotlib, numpy)
- SQL (SQLite for queries and filtering)
- Statistical analysis (percentiles, distributions)

**Approach:**
- Load CSV data into SQLite database
- Use SQL for complex filtering with multiple conditions
- Use Python for statistical calculations and visualization
- Compare results across three different methodologies

Each version is fully reproducible with documented cleaning rules and SQL queries.

## Files

- `version_a_raw.py` - Raw data analysis (no cleaning)
- `version_b_cleaned.py` - Moderate cleaning analysis
- `version_c_strict.py` - Conservative cleaning analysis
- `comparison.py` - Side-by-side comparison of all three
- `README.md` - This file

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas matplotlib numpy

# Run analyses
python version_a_raw.py
python version_b_cleaned.py
python version_c_strict.py
python comparison.py
```

## Requirements

- Python 3.8+
- pandas
- matplotlib
- numpy
- sqlite3 (built-in)

## Dataset

Reddit Tech Salary Survey 2018 - 4,500+ responses from tech workers reporting base salaries.

## What I Learned

1. **Outliers tell stories** - Don't remove them blindly. Sometimes they're errors. Sometimes they're CEOs.

2. **Mean vs Median matters** - In skewed salary data, median ($68K-$70K) is more meaningful than mean ($79K).

3. **Document your decisions** - Future you (or your manager) will ask "why did you exclude values above $110K?"

4. **Visualize early** - That raw data histogram immediately showed the problem. One bar at $27M told me everything.

5. **There is no "right" answer** - Only answers that fit your question and context.

---

**The bottom line:** Anyone can calculate an average. A data scientist knows which average to calculate.
