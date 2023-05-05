So after thinking about this here is what I think I want to do

1. Every weekday I will pull from API's and get the latest data. The API's I am currently looking into are:
    Alpha Vantage's API for Commodities, Forex, and Econ indicators
        Will need latest 1000 days (to be safe)
    Market Data Docs' API for Indices quotes (or candle)
2. I will format from JSON into Dataframes then into csv (?) so I can send to DB - Snowflake I guess
3. In Snowflake I will package data as I need it:
    a. I will build (Materialized?) views for dashboard. 
    b. Also create moving averages calculations among others and store in the appropriate DB
    c. 
4. I will pull data from the database for the dashboard
    a. Unsure whether to build or use service for Dashboard


NOTE: 
    1 Need to test MD endpoints and parameters in Postman
    2 Need to get symbols for other major indices
    3 Need to test main.py