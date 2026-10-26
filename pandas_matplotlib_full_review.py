"""
PANDAS + MATPLOTLIB — FULL JOURNEY REVIEW
=========================================
Everything from the start: Python basics -> Pandas -> GroupBy/Pivot -> Merge -> Time series
-> Matplotlib -> Real-world projects -> Capstone.

HOW TO USE
- Put this file in the same folder as Kenya_Financial_Data_CLEAN.xlsx.
- In VS Code, click "Run Cell" above each `# %%` marker and do ONE exercise at a time.
- Run the SETUP cell first, every session.
- Each exercise has a TASK, sometimes a CHECK (a number you can verify against), and an INSIGHT question.
  Answer the INSIGHT in a comment under your code. Numbers without meaning are not analysis.
- No hints. Struggle for ~10 minutes, then ask.

LEVELS
  [CORE]     taught already
  [STRETCH]  new tool: look it up or ask me
  [ADVANCED] combines several ideas
  [REAL]     realistic banking / SACCO scenario

SYNTHETIC DATA: `loans`, `sacco`, `branch_info`, `provision_rates` and `messy` are made up for practice.
Kenya macro data (summary_df) is real World Bank data.
"""

# %% ============================ SETUP (run first) ============================
import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    df_clean = pd.read_excel('Kenya_Financial_Data_CLEAN.xlsx')
except FileNotFoundError:
    raise SystemExit("Kenya_Financial_Data_CLEAN.xlsx not found. Put it in the same folder as this file.")
df_clean = df_clean.iloc[:15, :16]


def classify_gdp(rate):
    if rate > 5:
        return "strong"
    elif 3 <= rate <= 5:
        return "moderate"
    else:
        return "weak"


def classify_npl(ratio):
    if ratio < 5:
        return "healthy"
    elif ratio <= 10:
        return "watch"
    else:
        return "critical"


def classify_inflation(rate):
    if rate < 5:
        return "low"
    elif 5 <= rate <= 10:
        return "moderate"
    else:
        return "high"


summary_data = []
for i, year in enumerate([int(c) for c in df_clean.columns[1:]]):
    row = {'year': year}
    g = float(df_clean[df_clean['Indicator Name'] == 'GDP growth (annual %)'].iloc[0, i + 1])
    n = float(df_clean[df_clean['Indicator Name'] == 'Bank nonperforming loans to total gross loans (%)'].iloc[0, i + 1])
    f = float(df_clean[df_clean['Indicator Name'] == 'Inflation, consumer prices (annual %)'].iloc[0, i + 1])
    row.update({'gdp': g, 'gdp_class': classify_gdp(g),
                'npl': n, 'npl_class': classify_npl(n),
                'inflation': f, 'inflation_class': classify_inflation(f)})
    summary_data.append(row)
summary_df = pd.DataFrame(summary_data)

# --- external datasets used in the merge exercises ---
unemployment_df = pd.DataFrame({
    'year': list(range(2015, 2025)),
    'unemployment_rate': [2.76, 2.76, 3.54, 4.28, 5.01, 5.61, 5.69, 5.57, 5.41, 5.49]})
cbk_df = pd.DataFrame({
    'year': list(range(2018, 2025)),
    'cbk_rate': [10.0, 9.0, 7.25, 7.0, 8.5, 10.0, 11.0]})
forecast_df = pd.DataFrame({'year': [2025, 2026], 'gdp_forecast': [4.5, 4.8], 'npl_forecast': [14.0, 14.5]})

# --- SYNTHETIC loan book (80 loans) ---
rng = np.random.default_rng(42)
n_loans = 80
loans = pd.DataFrame({
    'loan_id': [f'L{1000 + i}' for i in range(n_loans)],
    'branch': rng.choice(['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'], n_loans),
    'product': rng.choice(['Personal', 'SME', 'Mortgage', 'Agri'], n_loans, p=[0.35, 0.30, 0.15, 0.20]),
    'principal': rng.integers(50_000, 5_000_000, n_loans),
    'interest_rate': rng.uniform(11, 20, n_loans).round(1),
    'days_overdue': rng.choice([0, 0, 0, 0, 15, 45, 95, 150, 220], n_loans),
    'repaid_pct': rng.uniform(0.1, 1.0, n_loans).round(2),
    'disbursed': pd.to_datetime('2023-01-01') + pd.to_timedelta(rng.integers(0, 640, n_loans), unit='D'),
})
branch_info = pd.DataFrame({
    'branch': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'],
    'region': ['Nairobi', 'Coast', 'Western', 'Rift Valley', 'Rift Valley'],
    'staff': [42, 28, 17, 19, 15]})
provision_rates = pd.MultiIndex.from_product(
    [['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret'], ['Personal', 'SME', 'Mortgage', 'Agri']],
    names=['branch', 'product']).to_frame(index=False)
provision_rates['base_rate'] = rng.uniform(0.01, 0.05, len(provision_rates)).round(3)

# --- SYNTHETIC SACCO monthly deposits (KES millions) ---
sacco = pd.DataFrame({
    'month': pd.date_range('2023-01-01', periods=24, freq='MS'),
    'deposits': (50 + np.cumsum(rng.normal(1.2, 2.0, 24))).round(1)})

# --- SYNTHETIC messy data for the cleaning exercises ---
messy = loans.head(12).copy()
messy['branch'] = [' nairobi', 'MOMBASA ', 'Kisumu', 'nakuru', 'Eldoret ', ' NAIROBI',
                   'mombasa', 'Kisumu ', 'NAKURU', 'eldoret', 'Nairobi', 'Mombasa']
messy.loc[2, 'principal'] = -250000
messy.loc[5, 'repaid_pct'] = np.nan
messy = pd.concat([messy, messy.iloc[[3]]], ignore_index=True)   # one duplicated row


def ex(code, title):
    print("\n" + "=" * 70)
    print(f"EXERCISE {code}: {title}")
    print("=" * 70)


print("Setup complete. summary_df:", summary_df.shape, "| loans:", loans.shape, "| sacco:", sacco.shape)


# ##########################################################################
# PART 1 — PYTHON FOUNDATIONS  (variables, lists, dicts, functions, loops)
# ##########################################################################

# %%
ex("1.1", "[CORE] Variables and f-strings")
# TASK: A loan of KES 1,250,000 at 14.5% for 3 years (simple interest). Store each in a variable.
#       Print one sentence: "Loan of KES 1,250,000 at 14.5% earns KES X interest over 3 years; total repayment KES Y."
#       Numbers need thousands separators and 2 decimals.
# CHECK: interest = 543,750.00 | total = 1,793,750.00
# YOUR CODE:



# %%
ex("1.2", "[CORE] Lists")
# TASK: amounts = [120000, 450000, 80000, 910000, 275000, 640000]
#       Print: how many loans, total, average, largest, smallest, and how many are ABOVE the average.
# CHECK: total 2,475,000 | average 412,500 | above average = 3
# YOUR CODE:



# %%
ex("1.3", "[CORE] Dictionaries and loops")
# TASK: Build a list of 6 loan dictionaries (name, principal, repaid, risk) using real-sounding Kenyan names
#       and businesses. Loop with .items() over ONE dictionary to print its keys/values, then loop over the
#       list and print only loans where risk == "high".
# INSIGHT: Why is a list of dictionaries a natural fit for a table?
# YOUR CODE:



# %%
ex("1.4", "[CORE] Functions with decisions")
# TASK: Write classify_age(months) -> "new" (<6), "mature" (6-17), "old" (18+).
#       Write classify_risk(repaid_pct, age) -> "recovered" if repaid >= 100,
#       "loss" if age is "old" and repaid < 50, "high risk" if age is "new" and repaid < 30,
#       otherwise "medium risk". Test each branch with at least 2 inputs.
# YOUR CODE:



# %%
ex("1.5", "[ADVANCED] Portfolio analyzer function")
# TASK: Write summarise_portfolio(loans_list) that RETURNS a dictionary with: total_principal,
#       total_repaid, recovery_rate (%), counts per risk class, and the name of the worst-performing loan
#       (lowest repaid %). Run it on two different lists to prove it is reusable.
# NOTE: this finishes the "find the worst performing loan" exercise from Module 1.
# YOUR CODE:



# ##########################################################################
# PART 2 — PANDAS BASICS  (load, inspect, select, clean, types)
# ##########################################################################

# %%
ex("2.1", "[CORE] Inspect a DataFrame")
# TASK: For `loans`: shape, dtypes, first 5 rows, last 3 rows, and describe() of principal and interest_rate.
# INSIGHT: Which column would you expect to be skewed, and how can you tell from describe()?
# YOUR CODE:



# %%
ex("2.2", "[CORE] Selecting: column, iloc, loc")
# TASK: (a) the principal column as a Series; (b) principal and branch as a DataFrame;
#       (c) the 3rd row using iloc; (d) rows 10-14 and only 'loan_id','principal' using loc;
#       (e) every loan with loan_id 'L1005' using a boolean filter.
# INSIGHT: In your own words: when do you use iloc and when loc?
# YOUR CODE:



# %%
ex("2.3", "[CORE] Missing data")
# TASK: Copy `messy`. Count the nulls per column, then fill the missing repaid_pct with the MEDIAN
#       (not zero). Explain in a comment why median is safer than mean here.
# YOUR CODE:



# %%
ex("2.4", "[CORE] Rename, drop, sort")
# TASK: On a copy of loans: rename 'principal' to 'principal_kes', drop 'interest_rate',
#       sort by principal_kes descending, show the top 5.
# YOUR CODE:



# %%
ex("2.5", "[STRETCH] Dates")
# TASK: Using the .dt accessor on loans['disbursed'], add columns: disb_year, disb_month, disb_quarter.
#       Then count how many loans were disbursed in each quarter (in chronological order).
# INSIGHT: Which quarter had the most disbursements?
# YOUR CODE:



# %%
ex("2.6", "[ADVANCED] Rebuild summary_df from scratch")
# TASK: WITHOUT looking at the setup code, rebuild a DataFrame called rebuilt from df_clean that has
#       year, gdp, npl, inflation. Then prove it matches summary_df[['year','gdp','npl','inflation']]
#       using a comparison method (not eyeballing).
# YOUR CODE:



# %%
ex("2.7", "[STRETCH] Reshape: wide -> long -> wide")
# TASK: df_clean is WIDE (one column per year). Use melt to make it LONG (columns: indicator, year, value),
#       then pivot it back so each row is a year and each column is an indicator.
#       Keep only the 3 indicators used in summary_df.
# INSIGHT: Why is long format preferred by Power BI and by groupby?
# YOUR CODE:



# ##########################################################################
# PART 3 — FILTERING, NEW COLUMNS, apply, map
# ##########################################################################

# %%
ex("3.1", "[CORE] Boolean filters")
# TASK: From summary_df: (a) years with gdp_class 'strong' AND npl_class in ['watch','critical'];
#       (b) years where inflation is between 6 and 9; (c) years where NPL is above its own average.
# CHECK: (a) 6 rows | (c) 8 rows
# YOUR CODE:



# %%
ex("3.2", "[STRETCH] query() and np.where")
# TASK: (a) redo 3.1(a) using .query(). (b) Add a column 'stress' using np.where: "stressed" if
#       npl > 10 and inflation > 6, else "ok". Count each.
# CHECK: stressed = 3
# YOUR CODE:



# %%
ex("3.3", "[CORE] apply() across rows")
# TASK: Write classify_health(row) using gdp_class and npl_class:
#       strong+healthy -> excellent, strong+watch -> good, strong+critical -> concerning,
#       moderate/weak + critical -> weak, else fair. Apply with axis=1 and count the results.
# CHECK: concerning = 3, weak = 3
# YOUR CODE:



# %%
ex("3.4", "[STRETCH] map()")
# TASK: Use map with a dictionary to turn npl_class into a score (healthy=1, watch=2, critical=3), and
#       gdp_class into (strong=1, moderate=2, weak=3). Add a 'risk_score' = sum of the two. Show the 5 riskiest years.
# INSIGHT: What are the weaknesses of a simple additive score?
# YOUR CODE:



# %%
ex("3.5", "[STRETCH] nlargest / nsmallest")
# TASK: Find the 3 years with the highest NPL and the 3 years with the lowest GDP, each in ONE line of pandas.
# YOUR CODE:



# ##########################################################################
# PART 4 — GROUPBY, PIVOT, TRANSFORM
# ##########################################################################

# %%
ex("4.1", "[CORE] GroupBy with agg dictionary")
# TASK: Group summary_df by gdp_class: count of years, mean and max NPL, mean inflation, min/max GDP.
# CHECK: strong -> 7 years, mean NPL 8.57
# YOUR CODE:



# %%
ex("4.2", "[STRETCH] Named aggregation")
# TASK: Same as 4.1 but with clean column names using named aggregation:
#       .agg(years=('year','count'), avg_npl=('npl','mean'), ...). Round to 2 d.p.
# INSIGHT: Why are named columns better when you export to Excel or Power BI?
# YOUR CODE:



# %%
ex("4.3", "[CORE] Multi-column groupby and pivot_table")
# TASK: (a) Group by [gdp_class, npl_class] and give the count and mean inflation.
#       (b) Make a pivot_table: rows gdp_class, columns npl_class, values = year, aggfunc='count'.
#       (c) Add row/column totals (look up margins).
# CHECK: the grand total must be 15
# YOUR CODE:



# %%
ex("4.4", "[STRETCH] transform()")
# TASK: Add a column npl_vs_class_avg = each year's NPL minus the average NPL of ITS gdp_class
#       (use groupby + transform so the result keeps the original 15 rows).
# INSIGHT: Which year is the most above its own group's average? Why does that matter?
# YOUR CODE:



# %%
ex("4.5", "[STRETCH] value_counts with percentages")
# TASK: Percentage of years in each npl_class and in each inflation_class (as %, 1 decimal).
# CHECK: critical = 40.0%
# YOUR CODE:



# %%
ex("4.6", "[REAL] Loan book by branch and product")
# TASK: From `loans`: (a) pivot of TOTAL principal (KES millions, 1 d.p.) by branch x product,
#       fill empty cells with 0. (b) The share of the total book each branch holds (%).
#       (c) The single branch+product cell with the largest exposure.
# INSIGHT: What concentration risk would a risk manager flag?
# YOUR CODE:



# %%
ex("4.7", "[ADVANCED] Rank within groups")
# TASK: In `loans`, rank every loan by principal WITHIN its branch (1 = biggest in that branch).
#       Show the top-2 loans of every branch in one table.
# INSIGHT: Why is "top 2 per branch" a common real-world report?
# YOUR CODE:



# ##########################################################################
# PART 5 — MERGING AND JOINING
# ##########################################################################

# %%
ex("5.1", "[CORE] The four join types")
# TASK: Merge summary_df with unemployment_df on year using inner, left, right and outer.
#       Print the row count of each. Then, for the left join, list the years with missing unemployment.
# CHECK: inner 10 | left 15 | right 10 | outer 15
# INSIGHT: Which join would you use to build a model that needs complete rows only?
# YOUR CODE:



# %%
ex("5.2", "[CORE] Chain merges")
# TASK: Build master = summary_df + unemployment_df + cbk_df (left joins). Columns to show:
#       year, gdp, npl, unemployment_rate, cbk_rate. Which columns have the most NaN?
# YOUR CODE:



# %%
ex("5.3", "[REAL] Merge on one key, then two keys")
# TASK: (a) Merge loans with branch_info on branch to bring in region and staff.
#       (b) Merge the result with provision_rates on BOTH branch and product.
#       (c) Confirm you still have 80 rows.
# YOUR CODE:



# %%
ex("5.4", "[STRETCH] Audit a merge with indicator=True")
# TASK: Outer-merge summary_df with forecast_df using indicator=True. Count how many rows are
#       'left_only', 'right_only' and 'both'.
# CHECK: left_only 15, right_only 2, both 0
# YOUR CODE:



# %%
ex("5.5", "[ADVANCED] The duplicate-key trap")
# TASK: Create unemployment_dup = unemployment_df plus one extra copy of the 2020 row.
#       Left-merge summary_df with it. How many rows do you get and why? Then fix it two ways:
#       (a) drop_duplicates before merging, (b) use the validate= argument so pandas raises an error.
# INSIGHT: How could this silently inflate a bank's total loan exposure in a real report?
# YOUR CODE:



# %%
ex("5.6", "[STRETCH] concat")
# TASK: Stack forecast rows under summary_df using pd.concat so the result has 17 rows.
#       How is this different from the merge in 5.4?
# YOUR CODE:



# ##########################################################################
# PART 6 — TIME SERIES AND WINDOW FUNCTIONS
# ##########################################################################

# %%
ex("6.1", "[CORE] Rolling and expanding")
# TASK: Index summary_df by year. Compute: 3-year and 5-year rolling mean of GDP,
#       expanding max and cumulative sum of NPL. Show all in one DataFrame.
# CHECK: rolling-3 GDP in 2012 = 5.92 | cumulative NPL by 2024 = 130.37
# YOUR CODE:



# %%
ex("6.2", "[STRETCH] Rolling volatility")
# TASK: 4-year rolling standard deviation of inflation. In which year did inflation volatility peak?
# INSIGHT: Why do banks care about volatility, not just the level?
# YOUR CODE:



# %%
ex("6.3", "[CORE] diff, pct_change, rank")
# TASK: For NPL: year-on-year change, percentage change, and rank (1 = worst).
#       Which year had the biggest rise? The biggest fall?
# CHECK: biggest rise 2016 (+2.60) | biggest fall 2019 (-2.28)
# YOUR CODE:



# %%
ex("6.4", "[ADVANCED] Longest streak")
# TASK: Find the longest run of consecutive years in which NPL ROSE, and print the start and end year.
#       (Hint of approach only: think diff() > 0 and a running counter that resets.)
# INSIGHT: Does a streak signal a structural problem or a cycle?
# YOUR CODE:



# %%
ex("6.5", "[STRETCH] shift() — does today's GDP predict tomorrow's NPL?")
# TASK: Create gdp_lag1 (last year's GDP). Compute the correlation between gdp_lag1 and NPL, and between
#       same-year GDP and NPL. Compare.
# INSIGHT: If correlation is weak, what else might drive NPL in Kenya? Name three factors.
# YOUR CODE:



# %%
ex("6.6", "[REAL] SACCO deposits: monthly to quarterly")
# TASK: Using `sacco` (set month as the index): (a) month-on-month growth %, (b) 3-month rolling average,
#       (c) quarterly average using resample, (d) the quarter with the highest average deposits.
# INSIGHT: Would a SACCO manager prefer monthly or quarterly numbers for budgeting? Why?
# YOUR CODE:



# ##########################################################################
# PART 7 — PANDAS + MATPLOTLIB TOGETHER
# ##########################################################################

# %%
ex("7.1", "[CORE] DataFrame.plot() vs plt.subplots()")
# TASK: Draw the 3 indicators as lines using (a) summary_df.set_index('year')[[...]].plot()
#       and (b) the plt.subplots object-oriented way. Which gives you more control, and why?
# YOUR CODE:



# %%
ex("7.2", "[CORE] GroupBy result -> bar chart")
# TASK: Bar chart of average NPL by gdp_class, with the value on top of each bar and a title that
#       states the finding (not just the topic).
# YOUR CODE:



# %%
ex("7.3", "[ADVANCED] Heatmap from a pivot table")
# TASK: Take the branch x product pivot from 4.6 and draw it as a heatmap (imshow) with the
#       numbers printed in each cell, axis labels from the pivot, and a colour bar.
# INSIGHT: Which cell is hottest, and what would you ask the branch manager?
# YOUR CODE:



# %%
ex("7.4", "[CORE] Raw vs rolling vs expanding")
# TASK: One chart: raw GDP, 3-year rolling GDP (dashed), and the long-run average as a flat line.
# INSIGHT: Is GDP trending down, or just noisy?
# YOUR CODE:



# %%
ex("7.5", "[ADVANCED] Merged data on twin axes")
# TASK: Using your merge from 5.1: GDP (left axis) and unemployment (right axis) for 2015-2024
#       on one chart. Handle the missing years properly (no crashes, no fake zeros).
# INSIGHT: What happened to unemployment in 2020 and did it recover?
# YOUR CODE:



# %%
ex("7.6", "[STRETCH] Bars coloured by sign")
# TASK: Bar chart of year-on-year NPL change: red when NPL rose, green when it fell. Add a zero line.
# INSIGHT: How many years did NPL rise vs fall?
# CHECK: rose 10 times, fell 4 times
# YOUR CODE:



# %%
ex("7.7", "[ADVANCED] Scatter with regression and class colours")
# TASK: GDP vs NPL scatter. Colour points by npl_class (green/orange/red), draw a best-fit line with
#       np.polyfit, show the correlation in the title, and label the 2020 point.
# INSIGHT: State the finding in one sentence a non-technical person understands.
# YOUR CODE:



# %%
ex("7.8", "[STRETCH] Stacked bars from a pivot")
# TASK: Use the pivot from 4.3 (gdp_class x npl_class counts) and draw a stacked bar chart:
#       one bar per gdp_class, stacked by npl_class.
# INSIGHT: In which GDP class does "critical" dominate?
# YOUR CODE:



# %%
ex("7.9", "[REAL] Branch NPL league table")
# TASK: From `loans`, define a loan as non-performing if days_overdue > 90. For each branch compute
#       NPL ratio = non-performing principal / total principal (%). Draw a horizontal bar chart sorted
#       worst-first, red if above 10%, a dashed line at 10%, and the value labelled on each bar.
# INSIGHT: Which branch should the credit committee visit first?
# YOUR CODE:



# %%
ex("7.10", "[ADVANCED] 2 x 2 dashboard from summary_df")
# TASK: Top-left GDP line with rolling mean, top-right NPL bars coloured by class, bottom-left inflation
#       with a 6% reference line, bottom-right the combined health score. Overall title + saved as PNG
#       (300 dpi) inside a folder called charts.
# YOUR CODE:



# ##########################################################################
# PART 8 — REAL-WORLD PROJECTS
# ##########################################################################

# %%
ex("8.1", "[REAL] IFRS 9-style provisioning")
# TASK: Using `loans` merged with provision_rates (see 5.3):
#       Stage 1 = days_overdue <= 30  -> loss rate 1%
#       Stage 2 = 31-90 days          -> loss rate 10%
#       Stage 3 = > 90 days           -> loss rate 50%
#       (a) add a 'stage' column, (b) expected loss = principal x stage loss rate,
#       (c) a table by branch with: total principal, total expected loss, coverage ratio (%),
#       (d) a bar chart of coverage by branch.
#       Also compute PAR30 and PAR90 for the whole book (principal overdue > 30 / > 90 days, as % of total).
# INSIGHT: Which branch is under-provisioned relative to its risk?
# YOUR CODE:



# %%
ex("8.2", "[REAL] SACCO early-warning on deposits")
# TASK: Flag every month where deposits FELL versus the previous month AND are below their 3-month rolling average.
#       Plot deposits, the rolling average, and mark the flagged months with red dots.
# INSIGHT: How would a SACCO treasurer use this signal?
# YOUR CODE:



# %%
ex("8.3", "[REAL] Kenya macro early-warning system")
# TASK: Rule: a year is RED if (3-yr rolling NPL has risen two years in a row) AND (inflation > 6).
#       Build the flag, list the red years, and draw NPL with red markers on flagged years.
# INSIGHT: Would this rule have warned you before the 2016 jump? What would you improve?
# YOUR CODE:



# %%
ex("8.4", "[REAL] Cleaning pipeline")
# TASK: The `messy` DataFrame has bad branch names (spaces/case), a negative principal, a missing
#       repaid_pct and a duplicated row. Write ONE function clean_loans(df) that returns a clean copy:
#       strip and title-case branch, drop duplicates, drop non-positive principal, fill missing
#       repaid_pct with the median. Chain the steps. Print before/after row counts.
# CHECK: 13 rows before -> 11 rows after
# INSIGHT: Why must cleaning be a function and not manual edits in Excel?
# YOUR CODE:



# %%
ex("8.5", "[REAL] Export for Power BI and Excel")
# TASK: Create a folder 'exports'. Save (a) summary_df with all your extra columns as CSV (no index),
#       (b) an Excel workbook with 3 sheets: 'Macro' (master from 5.2), 'Branch' (table from 8.1),
#       'SACCO' (sacco with growth columns). Re-open the Excel file with pandas to confirm each sheet.
# INSIGHT: Which format would you hand to Power BI, and which to a manager who only has Excel?
# YOUR CODE:



# ##########################################################################
# PART 9 — CAPSTONE
# ##########################################################################

# %%
ex("9.1", "[ADVANCED] Pandas vs SQL: the same questions twice")
# TASK: Load summary_df into an in-memory SQLite database (sqlite3 + to_sql). For EACH question below,
#       answer with SQL via pd.read_sql, then with pandas, and confirm the answers match:
#       (a) the year with the highest GDP
#       (b) years where NPL is above the average NPL
#       (c) average NPL per gdp_class, highest first
#       (d) count of years per npl_class
# INSIGHT: Which was faster to write for you, SQL or pandas? When would you pick each one at work?
# YOUR CODE:



# %%
ex("9.2", "[ADVANCED] Reusable report script")
# TASK: Turn your work into a small program:
#       - function load_data(path) -> summary_df
#       - function add_features(df) -> adds rolling, diff, health score, flags
#       - function make_dashboard(df, out_path) -> saves a 6-panel PNG
#       - function main() -> runs everything, prints a 5-line text summary with f-strings
#       - guarded by  if __name__ == "__main__":
#       Put it in its own file kenya_report.py, run it from the terminal, and push it to GitHub with a README.
# INSIGHT: What would a hiring manager learn about you from this repo?
# YOUR CODE: (write in kenya_report.py)



# %%
print("""
SELF-REVIEW — be honest
1. Which parts of Python basics do I still hesitate on?
2. Which pandas tools can I use WITHOUT looking up the syntax? (groupby, merge, rolling, apply ...)
3. For each of: trend / comparison / relationship / distribution — which chart do I choose and why?
4. Which 3 exercises were hardest? Re-do them from a blank cell tomorrow, then again in a week.
5. What is the story my analysis tells about Kenya's banks, in 3 sentences, for a non-technical reader?
""")
