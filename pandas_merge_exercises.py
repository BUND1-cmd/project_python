"""
PANDAS MERGING & JOINING EXERCISES
Week 3 Consolidation — 10 Questions
Level: Intermediate (Merging & Joining)

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

# Recreate summary_df (your main dataset)
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
# EXERCISE 1: Basic Left Join
# ============================================================
print("\n" + "="*60)
print("EXERCISE 1: Basic Left Join")
print("="*60)

# Create external dataset: unemployment rates (partial years)
unemployment_data = {
    'year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'unemployment_rate': [2.76, 2.76, 3.54, 4.28, 5.01, 5.61, 5.69, 5.57, 5.41, 5.49]
}
unemployment_df = pd.DataFrame(unemployment_data)

# TODO: Merge summary_df with unemployment_df using LEFT join
# Expected: all 15 years from summary_df, unemployment data where available
# Write your code here:



# ============================================================
# EXERCISE 2: Inner Join (Only Overlapping Years)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 2: Inner Join - Only Years with Complete Data")
print("="*60)

# TODO: Merge using INNER join
# Expected: only years 2015-2024 (where both have data)
# Write your code here:



# ============================================================
# EXERCISE 3: Right Join
# ============================================================
print("\n" + "="*60)
print("EXERCISE 3: Right Join - All Unemployment Years")
print("="*60)

# TODO: Merge using RIGHT join
# Expected: all 10 unemployment years, GDP data where available
# Write your code here:



# ============================================================
# EXERCISE 4: Outer Join (Complete Picture)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 4: Outer Join - All Data from Both")
print("="*60)

# TODO: Merge using OUTER join
# Expected: 15 rows (all years from both tables)
# Write your code here:



# ============================================================
# EXERCISE 5: Merging Two External Datasets
# ============================================================
print("\n" + "="*60)
print("EXERCISE 5: Chain Multiple Merges")
print("="*60)

# Create second external dataset: interest rates (different years)
interest_rates = {
    'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'cbk_rate': [10.0, 9.0, 7.25, 7.0, 8.5, 10.0, 11.0]
}
interest_df = pd.DataFrame(interest_rates)

# TODO: Merge unemployment_df with interest_df on year
# Then merge the result with summary_df
# Expected: all years from summary_df with unemployment and interest rates where available
# Write your code here:



# ============================================================
# EXERCISE 6: Merge and Filter
# ============================================================
print("\n" + "="*60)
print("EXERCISE 6: Merge Then Filter")
print("="*60)

# TODO: Merge summary_df with unemployment_df (left join)
# Then filter to show only years where unemployment > 5%
# Display: year, gdp, npl, unemployment_rate
# Write your code here:



# ============================================================
# EXERCISE 7: Merge and Calculate New Column
# ============================================================
print("\n" + "="*60)
print("EXERCISE 7: Merge Then Create Derived Column")
print("="*60)

# TODO: Merge summary_df with unemployment_df (left join)
# Create new column: economic_stress = npl + unemployment_rate
# Sort by economic_stress descending
# Display top 5 rows with year, npl, unemployment_rate, economic_stress
# Write your code here:



# ============================================================
# EXERCISE 8: Check for Data Mismatches After Merge
# ============================================================
print("\n" + "="*60)
print("EXERCISE 8: Identify Data Gaps")
print("="*60)

# TODO: Merge summary_df with unemployment_df (left join)
# Find rows where unemployment_rate is NaN
# Display: year, gdp, unemployment_rate (for years missing unemployment data)
# Write your code here:



# ============================================================
# EXERCISE 9: Compare Join Types on Same Data
# ============================================================
print("\n" + "="*60)
print("EXERCISE 9: Join Type Comparison")
print("="*60)

# TODO: Do all 4 join types with unemployment_df and print row count for each
# inner_count = ?
# left_count = ?
# right_count = ?
# outer_count = ?
# Write your code here:



# ============================================================
# EXERCISE 10: Real-World Scenario - Adding Forecast Data
# ============================================================
print("\n" + "="*60)
print("EXERCISE 10: Combining Actuals with Forecast")
print("="*60)

# Create forecast data for 2025-2026
forecast_data = {
    'year': [2025, 2026],
    'gdp_forecast': [4.5, 4.8],
    'npl_forecast': [14.0, 14.5],
    'unemployment_forecast': [5.4, 5.3]
}
forecast_df = pd.DataFrame(forecast_data)

# TODO: Merge summary_df with unemployment_df (left)
# Then merge that result with forecast_df (outer)
# Display last 5 rows showing: year, gdp, gdp_forecast, unemployment_rate, unemployment_forecast
# Write your code here:



# ============================================================
# SUMMARY QUESTIONS
# ============================================================
print("\n" + "="*60)
print("REFLECTION QUESTIONS")
print("="*60)
print("""
1. When would you use INNER join vs LEFT join?
2. What happens to row count with each join type?
3. How do NaN values appear after a left join?
4. When merging multiple datasets, what order matters?
5. How can you identify data gaps after merging?
""")
