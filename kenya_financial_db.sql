CREATE TABLE indicators (
    indicator_id INT PRIMARY KEY AUTO_INCREMENT,
    indicator_name VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    description TEXT
);
CREATE TABLE yearly_values (
    value_id INT PRIMARY KEY AUTO_INCREMENT,
    indicator_id INT NOT NULL,
    year INT NOT NULL,
    value DECIMAL(10, 2),
    FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id)
);

INSERT INTO indicators (indicator_name, category, description) VALUES
('GDP growth (annual %)', 'Economic', 'Annual GDP growth rate'),
('Bank nonperforming loans to total gross loans (%)', 'Financial', 'NPL ratio - credit risk indicator'),
('Inflation, consumer prices (annual %)', 'Economic', 'Annual inflation rate'),
('Lending interest rate (%)', 'Financial', 'Average lending rate'),
('Deposit interest rate (%)', 'Financial', 'Average deposit rate'),
('Interest rate spread (lending rate minus deposit rate, %)', 'Financial', 'Bank profit margin');


INSERT INTO yearly_values (indicator_id, year, value) VALUES
(1, 2010, 8.06),
(1, 2011, 5.12),
(1, 2012, 4.57),
(1, 2013, 3.80),
(1, 2014, 5.02),
(1, 2015, 4.97),
(1, 2016, 4.21),
(1, 2017, 3.84),
(1, 2018, 5.65),
(1, 2019, 5.11),
(1, 2020, -0.27),
(1, 2021, 7.59),
(1, 2022, 4.86),
(1, 2023, 5.72),
(1, 2024, 4.66);

-- Insert NPL ratio data
INSERT INTO yearly_values (indicator_id, year, value) VALUES
(2, 2010, 5.13),
(2, 2011, 4.42),
(2, 2012, 4.59),
(2, 2013, 5.04),
(2, 2014, 5.46),
(2, 2015, 5.99),
(2, 2016, 8.59),
(2, 2017, 9.95),
(2, 2018, 12.03),
(2, 2019, 9.75),
(2, 2020, 11.88),
(2, 2021, 10.89),
(2, 2022, 10.75),
(2, 2023, 12.34),
(2, 2024, 13.57);

-- Insert Inflation data
INSERT INTO yearly_values (indicator_id, year, value) VALUES
(3, 2010, 3.96),
(3, 2011, 14.02),
(3, 2012, 9.38),
(3, 2013, 5.72),
(3, 2014, 6.88),
(3, 2015, 6.58),
(3, 2016, 6.30),
(3, 2017, 8.01),
(3, 2018, 4.69),
(3, 2019, 5.24),
(3, 2020, 5.41),
(3, 2021, 6.11),
(3, 2022, 7.66),
(3, 2023, 7.67),
(3, 2024, 4.49);

-- Insert Lending Rate data
INSERT INTO yearly_values (indicator_id, year, value) VALUES
(4, 2010, 14.42),
(4, 2011, 16.99),
(4, 2012, 16.08),
(4, 2013, 13.94),
(4, 2014, 12.00),
(4, 2015, 12.67),
(4, 2016, 13.78),
(4, 2017, 14.13),
(4, 2018, 12.64),
(4, 2019, 11.54),
(4, 2020, 19.72),
(4, 2021, 13.21),
(4, 2022, 14.50),
(4, 2023, 15.30),
(4, 2024, 14.76);

-- Insert Deposit Rate data
INSERT INTO yearly_values (indicator_id, year, value) VALUES
(5, 2010, 4.56),
(5, 2011, 6.45),
(5, 2012, 7.89),
(5, 2013, 6.23),
(5, 2014, 7.12),
(5, 2015, 8.34),
(5, 2016, 8.92),
(5, 2017, 8.11),
(5, 2018, 7.45),
(5, 2019, 6.78),
(5, 2020, 7.23),
(5, 2021, 8.56),
(5, 2022, 9.23),
(5, 2023, 11.98),
(5, 2024, 8.14);

-- Insert Interest Rate Spread data
INSERT INTO yearly_values (indicator_id, year, value) VALUES
(6, 2010, 9.86),
(6, 2011, 10.54),
(6, 2012, 8.19),
(6, 2013, 7.71),
(6, 2014, 4.88),
(6, 2015, 4.33),
(6, 2016, 4.86),
(6, 2017, 6.02),
(6, 2018, 5.19),
(6, 2019, 4.76),
(6, 2020, 12.49),
(6, 2021, 4.65),
(6, 2022, 5.27),
(6, 2023, 3.32),
(6, 2024, 6.62);

SELECT 
    i.indicator_name,
    COUNT(*) as year_count,
    MIN(yv.value) as min_value,
    MAX(yv.value) as max_value,
    ROUND(AVG(yv.value), 2) as avg_value
FROM indicators i
JOIN yearly_values yv ON i.indicator_id = yv.indicator_id
GROUP BY i.indicator_id, i.indicator_name
ORDER BY i.indicator_id;


















































































































