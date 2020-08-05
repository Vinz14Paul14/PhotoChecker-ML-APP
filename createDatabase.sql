
-- You need manually create schema FinalProject in PgAdmin;
-- comment lines must starts with "--" and ends with semicolon, otherwise you will get an error;

-- historical price data downloaded from finance.yahoo.com;
drop table if exists price;
CREATE TABLE price (
    ticker VARCHAR(20),
    date date,
    open float,
    high float,
    low float,
    close float,
    adj_close float,
    volume bigint,
    PRIMARY KEY (ticker, date)
);