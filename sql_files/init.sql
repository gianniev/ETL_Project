-- Ensure schema exists
CREATE SCHEMA IF NOT EXISTS gianni_ev93_coderhouse;

-- Create table in the specified schema
CREATE TABLE IF NOT EXISTS gianni_ev93_coderhouse.coinmarketcap (
    id SERIAL PRIMARY KEY,
    name VARCHAR(250),
    symbol VARCHAR(64),
    marketcap INT,
    price DECIMAL, 
    volume_24 DECIMAL
);


-- Query to check if data was loaded
select * from gianni_ev93_coderhouse.coinmarketcap