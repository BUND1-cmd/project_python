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

if __name__=="__main__":
        summary_df=load_data('Kenya_Financial_Data_CLEAN.xlsx')
        print(summary_df)

    
