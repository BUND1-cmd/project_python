import pandas as pd
import os
import matplotlib.pyplot as plt




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

def make_dashboard(df,out_path):
    os.makedirs(os.path.dirname(out_path)or'.',exist_ok=True)
    fig,axes=plt.subplots(2,2,figsize=(14,9))
    axes[0,0].plot(df['year'],df['gdp'],marker='o',linewidth=2,color='green')
    axes[0,0].set_title('gdp growth%')
    axes[0,0].grid(True,alpha=0.7)

    axes[0,1].bar(df['year'],df['npl'],color='red')
    axes[0,1].set_title('npl growth%')
    axes[0,1].grid(True,alpha=0.6)

    axes[1,0].hist(df['inflation'],bins=5,color='red',alpha=0.7,edgecolor='black')
    axes[1,0].set_title('inflation histogram')
    axes[1,0].grid(True,alpha=0.5)
    

    sc=axes[1,1].scatter(df['year'],df['health_score'],c=df['year'],cmap='viridis',s=60)
    fig.colorbar(sc,ax=axes[1,1],label='year')
    axes[1,1].set_title('heath score scatter point')
    axes[1,1].grid(True,alpha=0.6)

    for ax in [axes[0,0],axes[0,1],axes[1,1]]:
        ax.set_xticks(df['year'])
        ax.tick_params(axis='x',rotation=45)


    fig.savefig(out_path,dpi=300)
    plt.show()

def main():
    summary_df=load_data('Kenya_Financial_Data_CLEAN.xlsx')
    summary_df=add_features(summary_df)
    make_dashboard(summary_df,'charts/kenya_dashboard.png')

    first=summary_df.iloc[0]
    last=summary_df.iloc[-1]
    gap=summary_df['npl']-summary_df['gdp']
    worst=summary_df.loc[gap.idxmax()]
    recent=summary_df.tail(7)
    years_above_10 = (recent['npl'] > 10).sum()

    print("\nKey findings")
    print(f"1. Growth has not protected the banks: NPL rose from {first['npl']:.1f}% in {int(first['year'])} "
          f"to {last['npl']:.1f}% in {int(last['year'])}, while GDP averaged {summary_df['gdp'].mean():.1f}% a year.")
    print(f"2. COVID exposed the weakest point: in {int(worst['year'])} GDP contracted to {worst['gdp']:.1f}% "
          f"while NPL was already {worst['npl']:.1f}%, the widest gap of the period at {gap.max():.1f} points.")
    print(f"3. The NPL rise is structural: NPL stayed above 10% in {years_above_10} of the last {len(recent)} years.")
    print("\nReport saved to charts/kenya_dashboard.png")



if __name__=="__main__":
        main()