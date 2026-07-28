import pandas as pd

# Load the Kenya World Bank Excel file
# Change the path to where you saved the file on your laptop
df = pd.read_excel('Kenya_Financial_Data_CLEAN.xlsx')

# Explore the data
print(df.shape)
print(df.head())
print(df.columns.tolist())
# Extract GDP growth row
gdp = df[df['Indicator Name'] == 'GDP growth (annual %)']

# Convert to a simple series — years as index, values as data
gdp_series = gdp.iloc[0, 1:].astype(float)
gdp_series.index = gdp_series.index.astype(str)

print("\nKenya GDP Growth (2010-2024):")
print(gdp_series.round(2).to_string())

print(f"\nBest year: {gdp_series.idxmax()} ({gdp_series.max():.2f}%)")
print(f"Worst year: {gdp_series.idxmin()} ({gdp_series.min():.2f}%)")
print(f"Average growth: {gdp_series.mean():.2f}%")
# Extract NPL row — same as filtering in SQL
npl = df[df['Indicator Name'] == 'Bank nonperforming loans to total gross loans (%)']

# Take the numbers only, make them floats
npl_series = npl.iloc[0, 1:].astype(float)
npl_series.index = npl_series.index.astype(str)

# Print year by year
print("\nKenya NPL Ratio (2010-2024):")
print(npl_series.round(2).to_string())

# For NPL — lower is better, higher is worse
print(f"\nBest year (lowest NPL): {npl_series.idxmin()} ({npl_series.min():.2f}%)")
print(f"Worst year (highest NPL): {npl_series.idxmax()} ({npl_series.max():.2f}%)")
print(f"Average NPL: {npl_series.mean():.2f}%")

inf=df[df['Indicator Name']=='Inflation, consumer prices (annual %)']
inf_series=inf.iloc[0,1:].astype(float)
inf_series.index = inf_series.index.astype(str)
print("\nKenya INF Ratio (2010-2024):")
print(inf_series.round(2).to_string())
print(f"\nBest year (lowest INF): {inf_series.idxmin()} ({inf_series.min():.2f}%)")
print(f"Worst year (highest INF): {inf_series.idxmax()} ({inf_series.max():.2f}%)")
print(f"Average INF: {inf_series.mean():.2f}%")