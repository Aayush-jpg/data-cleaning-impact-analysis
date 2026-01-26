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
- Remove salaries < $30,000 (part-time/interns)
- Remove salaries > $350,000 (extreme outliers)
- **Result: Includes everyone from junior to senior roles**

### Version C: Conservative Cleaning
- Remove null values
- Remove salaries < $40,000 (exclude entry-level)
- Remove salaries > $110,000 (exclude senior/exec roles)
- Remove top 3% (statistical outliers)
- **Result: Typical mid-level employee range only**

## The Results

| Version | Average | Median | Data Points | Removed |
|---------|---------|--------|-------------|---------|
| **Raw (A)** | $27,572,945 | N/A | 4,500 | 0% |
| **Moderate (B)** | $79,310 | $70,175 | 3,850 | 14% |
| **Conservative (C)** | $78,944 | $68,000 | 3,200 | 29% |

### The Same Question. Three Different Answers.

The raw data says **$27.5 million** (obviously broken).  
The moderate approach says **$79,310** (market competitive).  
The conservative approach says **$68,000** (typical employee).

**Which one is "true"?**

They all are. They're just answering different questions:
- Raw: "What's the average of everything in the spreadsheet?" (Garbage in = garbage out)
- Moderate: "What's a competitive salary across all levels?" (Good for market research)
- Conservative: "What does a typical mid-level employee make?" (Good for budget planning)

## Why This Matters

If you're an HR manager setting salary bands:
- Using the raw average ($27M): Your budget is nonsense
- Using the moderate average ($79K): You'll compete for talent across all levels
- Using the conservative average ($68K): You might underpay experienced hires

**A $11,310 difference in averages can cost or save your company hundreds of thousands of dollars.**

The data didn't change. Your assumptions did.

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
