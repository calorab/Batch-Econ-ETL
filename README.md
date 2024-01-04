# Economics Batch ETL Project (Version 1.0)

## Tech: Python | Pandas | SQLite | Numpy | Requests | OS/CSV/TIME/DOTENV

This project was originally written as a way to not only practice building a data pipeline locally, but also to learn SQLite and charting libraries in a data project. For charting I used __Dash__ and __Plotly__ libraries.

The pipeline first builds the database locally using SQLite and get's the economics data from a few API's. From there calculations are made for charting and inserted into the database tables or views. Lastly the data is consumed and charted in the browser. A _.env_ file contains the API keys and other security info.

## Project Roadmap (01/04/2024)

My plan moving forward is to package this project into something that can be downloaded and used by anyone locally. Below is a non-inclusive (and unordered) list for what needs to be completed and was updated on the date listed above:

- Form these files into an executable CLI program
- Include prompts for naming the database, tables and views a well as API keys
- Include a teardown file for removing the database at user prompt
- Include -help resources and other misc files 
- Removing of unecessary files currently included








