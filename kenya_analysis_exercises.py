import pandas as pd

df_clean = pd.read_excel('Kenya_Financial_Data_CLEAN.xlsx')
df_clean = df_clean.iloc[:15,:16]

def classify_npl(npl_ratio):
    if npl_ratio < 5:
        return "healthy"
    elif npl_ratio <= 10 :
        return "watch"
    else :
        return "critical"

def classify_gdp(gdp_rate):
    if gdp_rate > 5:
        return "strong"
    elif 3<= gdp_rate <=5 :
        return "moderate"
    else:
        return "weak"

def classify_inflation(inflation_rate):
    if inflation_rate < 5 :
        return "low"
    elif 5<= inflation_rate <=10:
        return "moderate"
    else:
        return "high"
summary_data = []
years = [int(col) for col in df_clean.columns[1:]]
for i,year in enumerate (years):
    row = {'year':year}
    gdp_row = df_clean[df_clean['Indicator Name']== 'GDP growth (annual %)']
    gdp_values = float(gdp_row.iloc[0,i+1])
    row ['gdp'] = gdp_values
    row ['gdp_class'] = classify_gdp(gdp_values)
    npl_row = df_clean[df_clean['Indicator Name']== 'Bank nonperforming loans to total gross loans (%)']
    npl_values = float(npl_row.iloc[0,i+1])
    row['npl'] = npl_values
    row['npl_class'] = classify_npl(npl_values)
    inflation_row = df_clean[df_clean['Indicator Name']=='Inflation, consumer prices (annual %)']
    inflation_values = float(inflation_row.iloc[0,i+1])
    row ['inflation'] = inflation_values
    row['inflation_class'] = classify_inflation(inflation_values)


    summary_data.append(row)
summary_df = pd.DataFrame(summary_data)
print(summary_df)

print(summary_df)

# ============================================================
# EXERCISE 1: GroupBy GDP class
# ============================================================
print("\n=== EXERCISE 1: GroupBy GDP Class ===")
# Calculate: count, avg NPL, avg inflation, min/max GDP
# Write your code here:
print(summary_df.groupby('gdp_class')[['npl','inflation','gdp']].agg({
    'npl':['mean','count'],
    'inflation':'mean',
    'gdp':['min','max']
    }).round(2))
# ============================================================
# EXERCISE 2: GroupBy NPL class
# ============================================================
print("\n=== EXERCISE 2: GroupBy NPL Class ===")
# Calculate: count, avg GDP, avg inflation
# Write your code here:
print(summary_df.groupby('npl_class')[['gdp','inflation']].agg({
    'gdp':['mean','count'],
    'inflation':'mean'}).round(2))


# ============================================================
# EXERCISE 3: Pivot table - GDP rows, NPL columns, count values
# ============================================================
print("\n=== EXERCISE 3: Pivot - Count by GDP/NPL ===")
# Write your code here:
pivot_table = summary_df.pivot_table(
    values = 'year',
    index = 'gdp_class',
    columns = 'npl_class',
    aggfunc= 'count'
).round(2)
print(pivot_table)


# ============================================================
# EXERCISE 4: Pivot table - Year rows, GDP columns, NPL values
# ============================================================
print("\n=== EXERCISE 4: Pivot - NPL by Year/GDP ===")
# Write your code here:
pivot_table= summary_df.pivot_table(
    values = 'npl',
    index = 'year',
    columns = 'gdp_class'
).round(2)
print(pivot_table)


# ============================================================
# EXERCISE 5: Filter + Classify + Calculate
# ============================================================
print("\n=== EXERCISE 5: Strong GDP Years Analysis ===")
# Filter to only Strong GDP years
# Calculate: average NPL, average inflation, count of years
# Write your code here:
strong_years=summary_df[summary_df['gdp_class']=='strong']
print(strong_years[['npl','inflation']].agg({
    'npl':['mean','count'],
    'inflation':'mean'
}).round(2))


# ============================================================
# EXERCISE 6: Multiple conditions filtering
# ============================================================
print("\n=== EXERCISE 6: Strong GDP + Watch/Critical NPL ===")
# Filter where GDP class = Strong AND NPL class is either Watch or Critical
# Show: year, gdp, npl, inflation
# Write your code here:
filtered = summary_df[(summary_df['gdp_class']=='strong')&
                      (summary_df['npl_class'].isin(['watch','critical']))]
print(filtered[['year','gdp','npl','inflation']])



# ============================================================
# EXERCISE 7: Sorting + Top results
# ============================================================
print("\n=== EXERCISE 7: Top 5 Highest NPL Years ===")
# Sort by NPL descending, show first 5 rows
# Display: year, npl, npl_class, gdp, gdp_class
# Write your code here:
sorted = summary_df.sort_values('npl',ascending=False)
print(sorted[['year','npl','npl_class','gdp','gdp_class']].head(5))


# ============================================================
# EXERCISE 8: Calculate new column
# ============================================================
print("\n=== EXERCISE 8: NPL-GDP Gap ===")
# Create new column: npl_gdp_gap = npl - gdp
# Show: year, gdp, npl, npl_gdp_gap
# Sort by npl_gdp_gap descending
# Write your code here:
summary_df['npl_gdp_gap']= summary_df['npl']- summary_df['gdp']
sorted = summary_df.sort_values('npl_gdp_gap',ascending= False)
print(sorted[['year','gdp','npl','npl_gdp_gap']].head())



# ============================================================
# EXERCISE 9: Apply function to create classification
# ============================================================
print("\n=== EXERCISE 9: Economic Health Classification ===")
# Create a function that classifies overall economic health:
# - "Excellent" if Strong GDP AND Healthy NPL
# - "Good" if Strong GDP AND Watch NPL
# - "Concerning" if Strong GDP AND Critical NPL
# - "Weak" if Moderate/Weak GDP AND Critical NPL
# - "Fair" for everything else
# Apply to summary_df and show results
# Write your code here:
def classify_economic_health(row):
    gdp =row['gdp_class']
    npl = row['npl_class']
    if gdp =='strong' and npl == 'healthy':
        return 'excellent'
    elif gdp == 'strong' and npl=='watch':
        return "good"
    elif gdp == 'strong' and npl == 'critical':
        return 'concerning'
    elif gdp in['moderate','weak'] and npl== 'critical':
        return 'weak'
    else:
        return 'fair'
summary_df['economic_health']=summary_df.apply(classify_economic_health,axis=1)
print(summary_df[['year','gdp_class','npl_class','economic_health']])



# ============================================================
# EXERCISE 10: Summary statistics across entire dataset
# ============================================================
print("\n=== EXERCISE 10: Overall Kenya Financial Summary ===")
# Calculate across ALL years:
# - Total years analyzed
# - Average GDP, NPL, Inflation (with min/max for each)
# - Count of years by GDP class
# - Count of years by NPL class
# - Worst year (highest NPL)
# - Best year (lowest NPL)
# Write your code here: