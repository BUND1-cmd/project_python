"""
MATPLOTLIB PRACTICE — Kenya Financial Data
==========================================
28 exercises | Beginner -> Advanced -> Real-world -> Capstone



LEVELS
  [CORE]     things you already learned
  [STRETCH]  new tools: look up the function or ask me
  [ADVANCED] combines several ideas
  [REAL]     realistic banking / SACCO scenario
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# DATA (Kenya, World Bank 2010-2024) — do not edit
# ============================================================
years = list(range(2010, 2025))
gdp = [8.058474, 5.121106, 4.568680, 3.797848, 5.020111, 4.967721, 4.213517, 3.837958,
       5.647946, 5.114159, -0.272766, 7.590489, 4.859981, 5.719992, 4.660196]
npl = [5.132644, 4.421192, 4.590960, 5.043583, 5.455120, 5.988764, 8.585968, 9.949128,
       12.026729, 9.749355, 11.878576, 10.886463, 10.753110, 12.335551, 13.572976]
inflation = [3.961389, 14.022491, 9.377770, 5.717494, 6.878155, 6.582154, 6.297250, 8.005650,
             4.689806, 5.239638, 5.405162, 6.107936, 7.659863, 7.671396, 4.489789]
df = pd.DataFrame({'year': years, 'gdp': gdp, 'npl': npl, 'inflation': inflation})

# ============================================================
# PRACTICE DATASETS (SYNTHETIC — made up for practice, not real bank data)
# ============================================================
branches = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret']
loan_book = [420, 310, 180, 205, 150]            # KES millions outstanding
npl_by_branch = [6.1, 9.8, 12.4, 8.2, 14.9]      # NPL ratio %
ageing = {'Current': 61, '1-30 days': 12, '31-90 days': 9, '91-180 days': 6, '180+ days': 7}  # number of loans

rng = np.random.default_rng(7)
months = pd.date_range('2023-01-01', periods=24, freq='MS')
sacco_deposits = (50 + np.cumsum(rng.normal(1.2, 2.0, 24))).round(1)   # KES millions, monthly


# ############################################################
# PART A — LINE CHARTS
# ############################################################

# %%
# A1 [CORE] First chart
# TASK: Line chart of NPL 2010-2024. Markers on every point, title, axis labels,
#       faint gridlines, legend.
# INSIGHT: In one sentence, what is the NPL story?
# YOUR CODE:



# %%
# A2 [CORE] Three lines, one chart
# TASK: Plot GDP, NPL and inflation on the same axes. Give each its own colour,
#       line style and marker. Put the legend in the upper left.
# INSIGHT: Which line is hardest to read on a shared axis, and why?
# YOUR CODE:



# %%
# A3 [CORE] Axis control
# TASK: Redo A1 so that (a) every single year shows on the x-axis, rotated 45 degrees,
#       (b) the y-axis runs from 0 to 15.
# INSIGHT: How does starting the y-axis at 0 change how dramatic the chart looks?
# YOUR CODE:



# %%
# A4 [STRETCH] Reference lines
# TASK: On the NPL chart add a dashed horizontal line at 10% labelled "Critical threshold"
#       and a vertical line at 2020 labelled "COVID-19".
# INSIGHT: How many years sit above the threshold?
# CHECK: your count should be 6
# YOUR CODE:



# %%
# A5 [STRETCH] Annotations
# TASK: On the GDP chart, use an arrow annotation to mark the worst year and the best year,
#       with the value written in the label.
# INSIGHT: Why do annotations make a chart more useful for a manager?
# YOUR CODE:



# %%
# A6 [STRETCH] Shading
# TASK: On the GDP chart shade the COVID year (2020) with a vertical band, and shade the
#       region below zero growth in red.
# INSIGHT: What does shading add that a line alone does not?
# YOUR CODE:



# ############################################################
# PART B — BAR CHARTS
# ############################################################

# %%
# B1 [CORE] Conditional colours
# TASK: Bar chart of NPL by year. Colour each bar red if NPL > 10, orange if 5-10, green if < 5.
#       (Build the colour list with a loop or list comprehension.)
# INSIGHT: What does the colour pattern tell you at a glance?
# YOUR CODE:



# %%
# B2 [CORE] Horizontal bars, sorted
# TASK: Horizontal bar chart of loan_book by branch, sorted from largest to smallest
#       (largest at the top).
# INSIGHT: Which branch carries the most exposure?
# YOUR CODE:



# %%
# B3 [ADVANCED] Grouped bars
# TASK: For 2020-2024 only, draw GDP, NPL and inflation as three side-by-side bars per year.
#       You will need to shift each group of bars on the x-axis yourself.
# INSIGHT: In which year is the gap between NPL and GDP widest?
# YOUR CODE:



# %%
# B4 [ADVANCED] Stacked bars
# TASK: For each branch, split loan_book into performing and non-performing amounts using
#       npl_by_branch. Draw them stacked (performing at the bottom, non-performing on top).
# INSIGHT: Which branch has the largest NON-PERFORMING amount in KES, and is it the same
#          branch that has the highest NPL ratio?
# YOUR CODE:



# %%
# B5 [STRETCH] Value labels
# TASK: Take your B1 chart and print the NPL value above every bar (1 decimal place).
# INSIGHT: When do value labels help, and when do they clutter?
# YOUR CODE:



# ############################################################
# PART C — SUBPLOTS & DASHBOARDS
# ############################################################

# %%
# C1 [CORE] 1 x 3 panel
# TASK: Three charts side by side: GDP, NPL, inflation. Share the x-axis. Each has its own title.
# INSIGHT: What do you see when the three are lined up that you did not see separately?
# YOUR CODE:



# %%
# C2 [CORE] 2 x 2 dashboard with a main title
# TASK: GDP line (top-left), NPL bars (top-right), inflation line (bottom-left),
#       NPL minus GDP gap bars (bottom-right). Add one overall title for the whole figure.
# INSIGHT: Write the headline a newspaper would run on this dashboard.
# YOUR CODE:



# %%
# C3 [STRETCH] Twin axes
# TASK: One chart with NPL on the left y-axis and GDP on the right y-axis (different scales),
#       each axis label coloured to match its line.
# INSIGHT: Why can twin axes mislead readers? When are they justified?
# YOUR CODE:



# %%
# C4 [ADVANCED] Reusable chart function
# TASK: Write a function  plot_indicator(ax, x, y, title, color, threshold=None)  that draws a
#       line chart on a given axis and, if a threshold is given, adds a dashed line for it.
#       Then use it three times in a 1 x 3 figure.
# INSIGHT: What is the benefit of putting chart code in a function?
# YOUR CODE:



# ############################################################
# PART D — DISTRIBUTIONS & RELATIONSHIPS  (all STRETCH)
# ############################################################

# %%
# D1 Histogram
# TASK: Histogram of inflation with 5 bins and a vertical line at the mean.
# INSIGHT: Is inflation symmetric, or skewed by one extreme year? Which year?
# YOUR CODE:



# %%
# D2 Scatter with a colour scale
# TASK: Scatter of GDP (x) vs NPL (y). Colour each point by year using a colour bar,
#       and label the 2020 point.
# INSIGHT: Do the later years (darker/lighter colours) cluster in a particular corner?
# YOUR CODE:



# %%
# D3 Trend line and correlation
# TASK: Add a straight best-fit line to D2 and show the correlation coefficient in the title.
# INSIGHT: Is the relationship between GDP and NPL strong, weak or negligible?
#          What does that say about "growth fixes bad loans"?
# YOUR CODE:



# %%
# D4 Box plot
# TASK: Box plots of GDP, NPL and inflation side by side.
# INSIGHT: Which indicator is the most spread out? Which has outliers?
# YOUR CODE:



# %%
# D5 Donut / pie
# TASK: Donut chart of loan_book share by branch with percentage labels.
# INSIGHT: Why do many analysts prefer bar charts over pie charts for this?
# YOUR CODE:



# ############################################################
# PART E — POLISH & EXPORT
# ############################################################

# %%
# E1 [STRETCH] Styles
# TASK: Draw the same NPL line chart three times using three different plt.style options
#       (try 'ggplot', 'fivethirtyeight', 'bmh'). Reset to default afterwards.
# INSIGHT: Which style would you use in a board presentation and why?
# YOUR CODE:



# %%
# E2 [STRETCH] Save to file
# TASK: Create a folder called charts (if it does not exist) and save your C2 dashboard there
#       as a 300-dpi PNG with tight margins. Open the file and confirm it is not cropped.
# INSIGHT: Why do you save with a higher dpi than the screen default?
# YOUR CODE:



# %%
# E3 [ADVANCED] Colour by category
# TASK: Using only the data above, build a dict mapping an NPL class to a colour
#       (healthy < 5 -> green, watch 5-10 -> orange, critical > 10 -> red), then draw
#       a scatter of year vs NPL with each point coloured by its class and a legend that
#       lists the three classes.
# INSIGHT: From which year does the chart stay mostly red?
# YOUR CODE:



# ############################################################
# PART F — REAL-WORLD SCENARIOS
# ############################################################

# %%
# F1 [REAL] SACCO deposit growth
# TASK: Using months and sacco_deposits, plot monthly deposits, a 3-month rolling average,
#       and annotate the best month. Format the x-axis as "Jan-23" style dates.
# INSIGHT: Is the SACCO growing steadily, or is the growth coming in bursts?
# YOUR CODE:



# %%
# F2 [REAL] Branch risk bubble chart
# TASK: Scatter loan_book (x) vs npl_by_branch (y). Make each bubble's size proportional to
#       loan_book and write the branch name next to each bubble. Add a dashed line at 10% NPL.
# INSIGHT: If the credit committee can review only ONE branch this month, which one and why?
#          (Think about both size and risk.)
# YOUR CODE:



# %%
# F3 [REAL] Loan ageing report
# TASK: Bar chart of the ageing dict. Colours should go from green (current) to dark red (180+).
#       Put both the count and the percentage of total loans above each bar.
# INSIGHT: What share of the book is more than 90 days overdue? (This is the PAR90 idea.)
# CHECK: 13 of 95 loans, about 13.7%
# YOUR CODE:



# %%
# F4 [REAL] Macro stress view
# TASK: One chart with inflation as bars and NPL as a line on top. Highlight in red every year
#       where BOTH inflation > 6 and NPL > 10.
# INSIGHT: How many such "double stress" years exist, and are they recent or early?
# CHECK: 3 years
# YOUR CODE:



# ############################################################
# PART G — CAPSTONE
# ############################################################

# %%
# G1 [ADVANCED] The Board Pack
# TASK: Build ONE figure designed for a bank board (use a grid layout so panels can differ in size):
#       - Top, full width: NPL line with the 10% threshold, COVID marker and peak annotation.
#       - Middle left: GDP vs NPL scatter with trend line.
#       - Middle right: year-on-year NPL change bars (red for rise, green for fall).
#       - Bottom, full width: a "KPI strip" (text only, no chart) showing
#           latest NPL | change since 2011 | number of critical years | average inflation.
#       Add a title and a source note ("Source: World Bank"). Save it as charts/board_pack.png at 300 dpi.
# INSIGHT: Write three sentences a CEO could read aloud from this page.
# CHECK: latest NPL 13.57 | change since 2011 about +9.15 | critical years 6 | avg inflation about 6.81
# YOUR CODE:



# %%
print("""
SELF-REVIEW (answer honestly)
1. Which exercises did I solve without looking anything up?
2. Which function names do I still forget? (write them down, then re-type them from memory)
3. Which chart type fits: trend over time? comparison of categories? relationship between two variables?
4. Which chart would I show a non-technical manager, and which is only for me?
""")
