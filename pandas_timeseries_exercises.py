"""
PANDAS TIME SERIES & WINDOW FUNCTIONS EXERCISES
Week 4 Consolidation — 15 Questions
Level: Intermediate to Advanced (Rolling, Expanding, Ranking, Diff)

Instructions:
- Write the code for each exercise
- Run the entire file
- For each exercise, print results clearly with labels
- Answer the questions that follow each exercise
"""

import pandas as pd

# ============================================================
# SETUP: Load your Kenya data
# ============================================================
df_clean = pd.read_excel('Kenya_Financial_Data_CLEAN.xlsx')
df_clean = df_clean.iloc[:15, :16]

def classify_gdp(gdp_rate):
    if gdp_rate > 5:
        return "strong"
    elif 3 <= gdp_rate <= 5:
        return "moderate"
    else:
        return "weak"

def classify_npl(npl_ratio):
    if npl_ratio < 5:
        return "healthy"
    elif npl_ratio <= 10:
        return "watch"
    else:
        return "critical"

def classify_inflation(inflation_rate):
    if inflation_rate < 5:
        return "low"
    elif 5 <= inflation_rate <= 10:
        return "moderate"
    else:
        return "high"

summary_data = []
years = [int(col) for col in df_clean.columns[1:]]

for i, year in enumerate(years):
    row = {'year': year}
    gdp_row = df_clean[df_clean['Indicator Name'] == 'GDP growth (annual %)']
    gdp_values = float(gdp_row.iloc[0, i+1])
    row['gdp'] = gdp_values
    row['gdp_class'] = classify_gdp(gdp_values)
    
    npl_row = df_clean[df_clean['Indicator Name'] == 'Bank nonperforming loans to total gross loans (%)']
    npl_values = float(npl_row.iloc[0, i+1])
    row['npl'] = npl_values
    row['npl_class'] = classify_npl(npl_values)
    
    inflation_row = df_clean[df_clean['Indicator Name'] == 'Inflation, consumer prices (annual %)']
    inflation_values = float(inflation_row.iloc[0, i+1])
    row['inflation'] = inflation_values
    row['inflation_class'] = classify_inflation(inflation_values)
    
    summary_data.append(row)

summary_df = pd.DataFrame(summary_data)

# ============================================================
# WEEK 4: TIME SERIES & WINDOW FUNCTIONS
# ============================================================

# ============================================================
# EXERCISE 1: Rolling Average (3-year window)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 1: 3-Year Rolling Average for NPL")
print("="*60)

# TODO: Calculate 3-year rolling average of NPL
# Display: year, npl, rolling_3yr_npl
# Write your code here:
npl_series=summary_df.set_index('year')['npl']
npl_rolling= npl_series.rolling(window=3,min_periods=1).mean()
expected_npl=pd.DataFrame({
    'npl':npl_series,
    'average':npl_rolling
})
print(f"{expected_npl}")


# ============================================================
# EXERCISE 2: Multiple Rolling Windows
# ============================================================
print("\n" + "="*60)
print("EXERCISE 2: Compare 2-year, 4-year, 6-year Rolling Averages")
print("="*60)

# TODO: Calculate rolling averages with 3 different window sizes for GDP
# Display: year, gdp, rolling_2yr, rolling_4yr, rolling_6yr
# Write your code here:
gdp_series= summary_df.set_index('year')['gdp']
gdp_r_2= gdp_series.rolling(window=2,min_periods=1).mean()
gdp_r_4= gdp_series.rolling(window=4,min_periods=1).mean()
gdp_r_6= gdp_series.rolling(window=6,min_periods=1).mean()
exp_gdp=pd.DataFrame({
    'gdp':gdp_series,
    '2-avg':gdp_r_2,
    '4_avg':gdp_r_4,
    '6-avg':gdp_r_6
})
print(f"{exp_gdp}")


# ============================================================
# EXERCISE 3: Rolling Sum (Cumulative within window)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 3: 4-Year Rolling Sum of Inflation")
print("="*60)

# TODO: Calculate 4-year rolling sum of inflation
# Display: year, inflation, rolling_4yr_sum
# What does the rolling sum tell you about cumulative price pressure?
# Write your code here:
inflation_series = summary_df.set_index('year')['inflation']
inf_4 = inflation_series.rolling(window=4,min_periods=1).sum()
exp_inf= pd.DataFrame({
    'inflation':inflation_series,
    'rolling sum':inf_4
})
print(exp_inf)



# ============================================================
# EXERCISE 4: Expanding Windows
# ============================================================
print("\n" + "="*60)
print("EXERCISE 4: Expanding Max and Min for NPL")
print("="*60)

# TODO: Calculate expanding max (worst NPL so far) and expanding min (best NPL so far)
# Display: year, npl, worst_npl_so_far, best_npl_so_far
# Write your code here:



# ============================================================
# EXERCISE 5: Cumulative Sum (Total burden over time)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 5: Cumulative NPL Burden Over 15 Years")
print("="*60)

# TODO: Calculate expanding sum of NPL to show cumulative burden
# Display: year, npl, cumulative_npl_burden
# What is the total NPL burden by 2024?
# Write your code here:



# ============================================================
# EXERCISE 6: Year-over-Year Changes (Diff)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 6: Year-over-Year Changes in All Indicators")
print("="*60)

# TODO: Calculate diff() for GDP, NPL, and Inflation
# Display: year, gdp, gdp_change, npl, npl_change, inflation, inflation_change
# Which indicator had the most volatile year-over-year changes?
# Write your code here:



# ============================================================
# EXERCISE 7: Ranking Values
# ============================================================
print("\n" + "="*60)
print("EXERCISE 7: Rank Years by Economic Performance")
print("="*60)

# TODO: Rank years by:
# - NPL (ascending=False, so 1 = worst)
# - GDP (ascending=True, so 1 = best)
# - Inflation (ascending=True, so 1 = best/lowest inflation)
# Display: year, npl, npl_rank, gdp, gdp_rank, inflation, inflation_rank
# Write your code here:



# ============================================================
# EXERCISE 8: Find Extremes Using Diff
# ============================================================
print("\n" + "="*60)
print("EXERCISE 8: Biggest Year-over-Year Swings")
print("="*60)

# TODO: Calculate year-over-year changes, then find:
# - Year with biggest GDP improvement
# - Year with biggest GDP decline
# - Year with biggest NPL increase
# - Year with biggest NPL decrease
# Write your code here:



# ============================================================
# WEEK 2-3 REVIEW: GROUPBY & AGGREGATIONS
# ============================================================

# ============================================================
# EXERCISE 9: GroupBy Multiple Columns Review
# ============================================================
print("\n" + "="*60)
print("EXERCISE 9: REVIEW - GroupBy GDP and NPL Classes")
print("="*60)

# TODO: Group by both gdp_class and npl_class
# Calculate: count, avg inflation, min/max npl for each combination
# Write your code here:



# ============================================================
# EXERCISE 10: Pivot Table Review
# ============================================================
print("\n" + "="*60)
print("EXERCISE 10: REVIEW - Pivot Table by GDP/NPL")
print("="*60)

# TODO: Create pivot table with:
# - Rows: gdp_class
# - Columns: npl_class
# - Values: average inflation
# Use aggfunc='mean'
# Write your code here:



# ============================================================
# WEEK 3 REVIEW: MERGING & JOINING
# ============================================================

# ============================================================
# EXERCISE 11: Merge Review - Multiple Join Types
# ============================================================
print("\n" + "="*60)
print("EXERCISE 11: REVIEW - All 4 Join Types")
print("="*60)

# Create external dataset
unemployment_data = {
    'year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'unemployment_rate': [2.76, 2.76, 3.54, 4.28, 5.01, 5.61, 5.69, 5.57, 5.41, 5.49]
}
unemployment_df = pd.DataFrame(unemployment_data)

# TODO: Do all 4 merges (inner, left, right, outer) and print row count for each
# Write your code here:
inner_merge = summary_df.merge(
    unemployment_df,
    on='year',
    how='inner'
)
print(f"{inner_merge}")


# ============================================================
# EXERCISE 12: Merge Then Aggregate Review
# ============================================================
print("\n" + "="*60)
print("EXERCISE 12: REVIEW - Merge Then GroupBy")
print("="*60)

# TODO: Merge summary_df with unemployment_df (left join)
# Then groupby gdp_class and calculate:
# - count of years
# - average npl
# - average unemployment_rate
# Write your code here:



# ============================================================
# EXERCISE 13: Complex Chain - Merge, Filter, GroupBy
# ============================================================
print("\n" + "="*60)
print("EXERCISE 13: REVIEW - Multi-Step Analysis")
print("="*60)

# TODO: 
# 1. Merge summary_df with unemployment_df (left)
# 2. Filter to only years with unemployment data (not NaN)
# 3. GroupBy npl_class
# 4. Calculate: count, avg gdp, avg unemployment
# Write your code here:



# ============================================================
# EXERCISE 14: Rolling Window + Classification
# ============================================================
print("\n" + "="*60)
print("EXERCISE 14: Advanced - Rolling Average Classification")
print("="*60)

# TODO: Calculate 3-year rolling average of NPL
# Create classification: if rolling_npl < 8 = "improving", else "deteriorating"
# Display: year, npl, rolling_3yr_npl, classification
# Write your code here:



# ============================================================
# EXERCISE 15: Complete Analysis Report
# ============================================================
print("\n" + "="*60)
print("EXERCISE 15: Final Project - Kenya Financial Health Summary")
print("="*60)

# TODO: Create a comprehensive summary showing:
# - Rolling 3-year average GDP
# - Rolling 3-year average NPL
# - Year-over-year changes
# - Rank by economic health (combine GDP rank + inverse NPL rank)
# - Display: year, gdp, gdp_3yr_rolling, npl, npl_3yr_rolling, gdp_change, npl_change, combined_rank
# Write your code here:



# ============================================================
# REFLECTION QUESTIONS
# ============================================================
print("\n" + "="*60)
print("REFLECTION QUESTIONS FOR THIS WEEK")
print("="*60)
print("""
TIME SERIES CONCEPTS:
1. What's the difference between rolling() and expanding()?
2. When would you use rank() vs diff()?
3. How do NaN values appear in rolling calculations vs expanding?
4. Why is year-over-year change important for analysis?

INTEGRATION WITH PREVIOUS WEEKS:
5. How would you combine rolling averages with groupby?
6. How would you merge data then apply rolling windows?
7. When would you rank data within each group (groupby + rank)?
8. How do you identify data quality issues after merging?

REAL-WORLD APPLICATION:
9. What story does Kenya's rolling NPL average tell?
10. Which technique (rolling, ranking, or diff) best reveals the banking crisis?
""")
