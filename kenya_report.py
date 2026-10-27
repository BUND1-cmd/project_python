import pandas as pd




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


def load_data(path):
    df_raw =pd.read_excel(path)
    df_raw= df_raw.iloc[:15,:16]
    years =[int(col) for col in df_raw.columns[1:]]

    for i,year in enumerate(years):
        row={'year':year}

        gdp_row=df_raw[df_raw['Indicator Name']=='GDP growth (annual %)']
        gdp_value=float(gdp_row.iloc[0,i+1])
        row['gdp']=gdp_value
        row['gdp_class']=classify_gdp(gdp_value)
        
        npl_row=df_raw[df_raw["Indicator Name"]=='Bank nonperforming loans to total gross loans (%)']
        npl_value=float(npl_row.iloc[0,i+1])
        row['npl']=npl_value
        row['npl_class']=classify_npl(npl_value)
        
        inflation_row=df_raw[df_raw['Indicator Name']=='Inflation, consumer prices (annual %)']
        inflation_value=float(inflation_row.iloc[0,i+1])
        row['inflation']=inflation_value
        row['inflation_class']=classify_inflation(inflation_value)



        summary_data.append(row)


    summary_df =pd.DataFrame(summary_data)
    return summary_df

def add_features(df):
    df=df.copy()
    df['rolling_3yr_npl']=df['npl'].rolling(window=3,min_periods=1).mean()
    df['rolling_3yr_gdp']=df['gdp'].rolling(window=3,min_periods=1).mean()
    df['rolling_3yr_inflation']=df['inflation'].rolling(window=3,min_periods=1).mean()
    df['npl_expanding']=df['npl'].expanding().sum()
    df['gdp_expanding']=df['gdp'].expanding().sum()
    df['inflation_expanding']=df['inflation'].expanding().sum()
    df['npl_change']=df['npl'].diff()
    df['gdp_change']=df['gdp'].diff()
    df['inflation_change']=df['inflation'].diff()
    df['gdp_rank']=df['gdp'].rank(ascending=True)
    df['npl_rank']=df['npl'].rank(ascending=False)
    df['health_score']=df['gdp_rank']+df['npl_rank']
    
    return df




if __name__=="__main__":
        summary_df=load_data('Kenya_Financial_Data_CLEAN.xlsx')
        summary_df=add_features(summary_df)
        print(summary_df[['year','npl','rolling_3yr_npl','gdp','rolling_3yr_gdp','inflation','rolling_3yr_inflation',
                          'npl_expanding','gdp_expanding','inflation_expanding',
                          'gdp_change','npl_change','inflation_change',
                          'gdp_rank',
                          'npl_rank',
                          'health_score']].to_string())

    
