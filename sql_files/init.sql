-- Ensure schema exists
CREATE SCHEMA IF NOT EXISTS gianni_ev93_coderhouse;

-- Create table in the specified schema
CREATE TABLE IF NOT EXISTS gianni_ev93_coderhouse.coinmarketcap (
    id INTEGER IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(250),
    symbol VARCHAR(64),
    marketcap FLOAT,
    price DECIMAL(20, 10), 
    volume_24 VARCHAR(250),
    date TIMESTAMP
);


-- Query to check if data was loaded
select * from gianni_ev93_coderhouse.coinmarketcap
