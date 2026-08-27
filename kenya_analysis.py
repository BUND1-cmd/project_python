analyst_name = "peter bundi"
bank_target = "equity bank"
internship_complete=True
loan_portfolio=10305000
npl_ratio= 13.59

print(f"Analyst:{analyst_name}")
print(f"Target_employer:{bank_target}")
print(f"Internship_complete:{internship_complete}")
print(f"loan_portfolio_kes:{loan_portfolio:,}")
print(f"Npl_ratio:{npl_ratio}%")




counties=["meru","nairobi","mombasa","nakuru","kisumu"]
print(counties[0])
print(counties[-1])
print(len(counties))

gdp_growth=[8.06, 5.12, 4.57, 3.80, 5.02, 4.97, 4.21, 3.84, 5.65, 5.11, -0.27, 7.59, 4.86, 5.72, 4.66]
print(max(gdp_growth))
print(min(gdp_growth))
print(len(gdp_growth))

branches=[
 {
    "branch_name":"westlands branch",
    "county":"nairobi county",
    "total_loans":"35",
    "portfolio_kes":23000000,
    "npl_ratio":(13.35)
 },
 {
     "branch_name":"nairobi cbd",
     "county":"nairobi county",
     "total-loans":"24",
     "portfolio_kes":34000000,
     "npl_ratio":34.45
 },
 {
     "branch_name":"mombasa",
     "county":"mombasa",
     "total_loans":"45",
     "portfolio_kes":56000000,
     "npl_ratio":23.34
 }
]
for branch in branches:
    print(f"{branch['branch_name']}:{branch['portfolio_kes']}")