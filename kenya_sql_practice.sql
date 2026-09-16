-- ============================================================
-- KENYA FINANCIAL DATABASE — SQL PRACTICE
-- Basics to Advanced — One concept per day
-- ============================================================

USE kenya_financial_db;

-- ============================================================
-- DAY 1 — BASIC SELECT
-- ============================================================
-- Concept: SELECT * means "get all columns"
-- WHERE filters rows

-- Q1: Show all indicators in the database
-- Hint: SELECT * FROM table_name
-- Write your query below:
select * from indicators;


-- Q2: Show all yearly values for the year 2020
-- Hint: SELECT * FROM table WHERE column = value
-- Write your query below:
select * from yearly_values
where year = 2020;


-- ============================================================
-- DAY 2 — FILTERING AND ORDERING
-- ============================================================
-- Concept: WHERE filters, ORDER BY sorts

-- Q3: Show all GDP values (indicator_id = 1) ordered by year ascending
-- Hint: WHERE indicator_id = 1, ORDER BY year ASC
-- Write your query below:
SELECT *
from yearly_values
where indicator_id = 1
order by year asc;
 
-- Q4: Show all NPL values (indicator_id = 2) ordered by value descending
-- Find which year had the highest NPL
-- Hint: ORDER BY value DESC LIMIT 1
-- Write your query below:
select * from yearly_values
where indicator_id= 2
order by value DESC
limit 1;


-- ============================================================
-- DAY 3 — AGGREGATION (SUM, AVG, MIN, MAX, COUNT)
-- ============================================================
-- Concept: Aggregate functions combine rows into single results

-- Q5: What is the average GDP growth across all years?
-- Hint: SELECT AVG(value) FROM yearly_values WHERE indicator_id = 1
-- Write your query below:
select avg(value) from yearly_values
where indicator_id=1;


-- Q6: What is the highest NPL ratio ever recorded?
-- Hint: SELECT MAX(value) FROM yearly_values WHERE indicator_id = 2
-- Write your query below:
select max(value)
from yearly_values
where indicator_id=2;


-- Q7: What is the lowest inflation rate ever recorded?
-- Hint: SELECT MIN(value) FROM yearly_values WHERE indicator_id = 3
-- Write your query below:
select min(value)
from yearly_values
where indicator_id= 3;


-- ============================================================
-- DAY 4 — GROUP BY
-- ============================================================
-- Concept: GROUP BY groups rows, then aggregate each group

-- Q8: Show average value for EACH indicator
-- Display: indicator_id, indicator_name, avg_value
-- Hint: SELECT i.indicator_id, i.indicator_name, AVG(yv.value) 
--       FROM indicators i JOIN yearly_values yv ON i.indicator_id = yv.indicator_id
--       GROUP BY i.indicator_id, i.indicator_name
-- Write your query below:
select i.indicator_id,i.indicator_name,avg(yv.value)
from indicators i 
join yearly_values yv on i.indicator_id = yv.indicator_id
group by i.indicator_id,i.indicator_name;


-- Q9: Show the count of years with data for each indicator
-- Display: indicator_name, number_of_years
-- Hint: COUNT(*) counts rows in each group
-- Write your query below:
select i.indicator_name,
       count(*)  as number_of_years
from indicators i 
join yearly_values yv on i.indicator_id = yv.indicator_id
group by i.indicator_name;


-- ============================================================
-- DAY 5 — JOIN (combining tables)
-- ============================================================
-- Concept: JOIN connects data from two tables using a foreign key

-- Q10: Show indicator_name alongside its values
-- Display: indicator_name, year, value
-- Order by indicator_name, then year
-- Hint: SELECT i.indicator_name, yv.year, yv.value
--       FROM indicators i JOIN yearly_values yv ON i.indicator_id = yv.indicator_id
--       ORDER BY i.indicator_name, yv.year
-- Write your query below:
select i.indicator_name,yv.year,yv.value 
from indicators i 
join yearly_values yv on i.indicator_id = yv.indicator_id
order by i.indicator_name,yv.year;


-- ============================================================
-- DAY 6 — FILTERING AGGREGATED DATA (HAVING)
-- ============================================================
-- Concept: WHERE filters before GROUP BY, HAVING filters after

-- Q11: Show indicators where average value is above 5
-- Display: indicator_name, avg_value
-- Hint: HAVING AVG(yv.value) > 5
-- Write your query below:
select i.indicator_name,avg(yv.value) as average value
from indicators i
join yearly_values yv on i.indicator_id = yv.indicator_id
group by i.indicator_name
having avg(yv.value)>5;


-- Q12: Show years where we have data for ALL 6 indicators
-- Display: year, count_of_indicators
-- Hint: HAVING COUNT(DISTINCT indicator_id) = 6
-- Write your query below:
select yv.year,count(distinct indicator_id)
from yearly_values yv
group by yv.year
having count(distinct indicator_id) = 6;

-- ============================================================
-- DAY 7 — SUBQUERIES (queries inside queries)
-- ============================================================
-- Concept: A subquery returns a result that another query uses

-- Q13: Find the year with the highest GDP growth
-- Display: year, gdp_value
-- Hint: WHERE value = (SELECT MAX(value) FROM yearly_values WHERE indicator_id = 1)
-- Write your query below:
select value as gdp_value,year from yearly_values
where indicator_id =1 AND
 value = (
    select max(value) from yearly_values
    where indicator_id = 1
);


-- Q14: Show all years where NPL was above the average NPL
-- Display: year, npl_value
-- Hint: WHERE indicator_id = 2 AND value > (SELECT AVG(value) FROM yearly_values WHERE indicator_id = 2)
-- Write your query below:
select value as npl_value,year
from yearly_values
where indicator_id= 2 AND
 value > (
    select avg(value) from yearly_values
    where indicator_id = 2
 );



-- ============================================================
-- DAY 8 — CASE WHEN (conditional logic)
-- ============================================================
-- Concept: CASE WHEN classifies values into categories

-- Q15: Classify each year's NPL ratio as Healthy, Watch, or Critical
-- Display: year, npl_value, classification
-- Rules: < 5% = Healthy, 5-10% = Watch, > 10% = Critical
-- Hint: CASE WHEN yv.value < 5 THEN 'Healthy' WHEN yv.value <= 10 THEN 'Watch' ELSE 'Critical' END
-- Write your query below:



-- Q16: Show GDP values with classification as Good (>5%), Medium (3-5%), or Weak (<3%)
-- Display: year, gdp_value, classification
-- Write your query below:



-- ============================================================
-- DAY 9 — WINDOW FUNCTIONS (ranking, running totals)
-- ============================================================
-- Concept: Window functions calculate across rows without collapsing them

-- Q17: Rank years by GDP growth (highest to lowest)
-- Display: year, gdp_value, rank
-- Hint: SELECT yv.year, yv.value, RANK() OVER (ORDER BY yv.value DESC) as rank
--       FROM yearly_values yv WHERE yv.indicator_id = 1
-- Write your query below:



-- Q18: Show NPL values with running total (cumulative sum across years)
-- Display: year, npl_value, cumulative_npl
-- Hint: SUM(yv.value) OVER (ORDER BY yv.year) as cumulative_total
-- Write your query below:



-- ============================================================
-- DAY 10 — CAPSTONE: Complex multi-step query
-- ============================================================
-- Concept: Combine everything — JOINs, GROUP BY, HAVING, CASE WHEN, ORDER BY

-- Q19: COMPLETE FINANCIAL SUMMARY
-- For each year, show:
-- - year
-- - gdp_growth (with classification: Strong >5%, Moderate 3-5%, Weak <3%)
-- - npl_ratio (with classification: Healthy <5%, Watch 5-10%, Critical >10%)
-- - interest_spread
-- - lending_rate
-- Order by year descending
-- Hint: Use 5 separate JOINs to get all 5 indicators, then CASE WHEN for classifications
-- Write your query below:



-- ============================================================
-- END OF PRACTICE
-- After completing all 19 queries, you will have mastered:
-- SELECT, WHERE, ORDER BY, Aggregation, GROUP BY, JOIN, HAVING
-- Subqueries, CASE WHEN, Window Functions, and Complex Queries
-- ============================================================
