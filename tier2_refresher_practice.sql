-- ============================================================
-- SQL TIER 2 REFRESHER — Full Joins, Cross Join, Self Join,
-- Window Functions, Views, Constraints
-- Built against your existing World Bank Kenya schema:
--   indicators(indicator_id, indicator_name, category, description)
--   yearly_values(value_id, indicator_id, year, value)
-- Indicator IDs: 1=GDP growth, 2=NPL ratio, 3=Inflation,
--                4=Lending rate, 5=Deposit rate, 6=Interest spread
-- ============================================================


-- ============================================================
-- Q1: Full Join
-- Recap: FULL JOIN returns every row from both tables, matched
--   where possible, NULL where not. MySQL has no native FULL JOIN
--   — emulate it with LEFT JOIN UNION RIGHT JOIN.
-- Setup (run once): add an indicator with no yearly data yet,
--   so you have something for the join to actually demonstrate.
-- ============================================================

INSERT INTO indicators (indicator_name, category, description) VALUES
('Foreign direct investment (% of GDP)', 'Economic', 'FDI inflows as % of GDP');

-- Task: List every indicator alongside its yearly values, including
--   indicators with no yearly_values rows yet (like the one above).
-- Display: indicator_name, year, value
-- Hint:
--   SELECT i.indicator_name, yv.year, yv.value
--   FROM indicators i LEFT JOIN yearly_values yv ON i.indicator_id = yv.indicator_id
--   UNION
--   SELECT i.indicator_name, yv.year, yv.value
--   FROM indicators i RIGHT JOIN yearly_values yv ON i.indicator_id = yv.indicator_id;
-- Write your query below:



-- ============================================================
-- Q2: Cross Join
-- Recap: CROSS JOIN pairs every row of table A with every row of
--   table B (Cartesian product). Useful for generating a full grid
--   of combinations — e.g. every indicator × every year — so you
--   can spot which combos are missing actual data.
-- ============================================================

-- Task: Generate a row for every indicator paired with every
--   distinct year present in yearly_values.
-- Display: indicator_name, year
-- Hint:
--   SELECT i.indicator_name, y.year
--   FROM indicators i
--   CROSS JOIN (SELECT DISTINCT year FROM yearly_values) y;
-- Write your query below:



-- ============================================================
-- Q3: Self Join
-- Recap: A table joined to itself, aliased twice, to compare rows
--   within the same table. Here, joining yearly_values to itself
--   on `year` lets you line up two different indicators side by
--   side for the same year.
-- ============================================================

-- Task: For each year, show the NPL ratio (indicator_id = 2) next
--   to the Lending rate (indicator_id = 4) for that same year.
-- Display: year, npl_ratio, lending_rate
-- Hint:
--   SELECT npl.year, npl.value AS npl_ratio, lend.value AS lending_rate
--   FROM yearly_values npl
--   JOIN yearly_values lend
--     ON npl.year = lend.year
--    AND npl.indicator_id = 2
--    AND lend.indicator_id = 4;
-- Write your query below:



-- ============================================================
-- Q4: Window Functions
-- Recap: Window functions calculate across a set of related rows
--   WITHOUT collapsing them the way GROUP BY does.
--     ROW_NUMBER() — unique sequential number per row
--     RANK()       — same rank for ties, gaps after
--     DENSE_RANK() — same rank for ties, no gaps
--     LAG()/LEAD() — pull a value from the previous/next row
-- ============================================================

-- Task A: For NPL ratio (indicator_id = 2), show each year's value
--   next to the PREVIOUS year's value, and the year-over-year change.
-- Display: year, value, prev_value, change
-- Hint:
--   SELECT year, value,
--          LAG(value) OVER (ORDER BY year) AS prev_value,
--          value - LAG(value) OVER (ORDER BY year) AS change
--   FROM yearly_values
--   WHERE indicator_id = 2
--   ORDER BY year;
-- Write your query below:



-- Task B: Rank all years by GDP growth (indicator_id = 1),
--   highest growth first.
-- Display: year, value, rank
-- Hint:
--   SELECT year, value,
--          RANK() OVER (ORDER BY value DESC) AS rank
--   FROM yearly_values
--   WHERE indicator_id = 1;
-- Write your query below:



-- ============================================================
-- Q5: Views
-- Recap: A view is a saved, reusable SELECT that behaves like a
--   virtual table — good for hiding a repetitive join so you don't
--   rewrite it every time.
-- ============================================================

-- Task: Create a view called indicator_summary joining indicators
--   and yearly_values (indicator_name, category, year, value), then
--   query it for Financial-category indicators from 2020 onward.
-- Hint:
--   CREATE VIEW indicator_summary AS
--   SELECT i.indicator_name, i.category, yv.year, yv.value
--   FROM indicators i
--   JOIN yearly_values yv ON i.indicator_id = yv.indicator_id;
-- Write your CREATE VIEW + SELECT below:



-- ============================================================
-- Q6: Constraints
-- Recap: Constraints enforce data integrity at the table level.
--   NOT NULL, UNIQUE, CHECK, PRIMARY KEY, FOREIGN KEY.
--   Right now, yearly_values allows `value` to be NULL and allows
--   duplicate (indicator_id, year) pairs — nothing stops the same
--   indicator being logged twice for the same year.
-- ============================================================

-- Task: Write ALTER TABLE statements to:
--   (a) add a UNIQUE constraint on (indicator_id, year)
--   (b) make `value` NOT NULL
-- Hint:
--   ALTER TABLE yearly_values ADD CONSTRAINT uq_indicator_year UNIQUE (indicator_id, year);
--   ALTER TABLE yearly_values MODIFY value DECIMAL(10,2) NOT NULL;
-- Write your ALTER statements below:


