-- Run these in your SQL client (host: localhost, port: 5433, db: stocks, user/password: airflow)

-- 1. Did the data arrive?
SELECT symbol, COUNT(*) AS days, MIN(trade_date) AS first_day, MAX(trade_date) AS last_day
FROM daily_prices
GROUP BY symbol;

-- 2. Latest 5 days for one stock
SELECT * FROM daily_prices
WHERE symbol = 'AAPL'
ORDER BY trade_date DESC
LIMIT 5;

-- 3. Best and worst single-day moves
SELECT symbol, trade_date, daily_return_pct
FROM daily_prices
ORDER BY daily_return_pct DESC
LIMIT 5;

SELECT symbol, trade_date, daily_return_pct
FROM daily_prices
ORDER BY daily_return_pct ASC
LIMIT 5;

-- 4. Average daily return per stock
SELECT symbol, ROUND(AVG(daily_return_pct)::numeric, 3) AS avg_daily_return_pct
FROM daily_prices
GROUP BY symbol
ORDER BY avg_daily_return_pct DESC;
