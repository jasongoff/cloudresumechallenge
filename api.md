# Chunk 2: Building the API
To start with, I created and tested the API in a Development account, separate from the Production account hosting the website created in Chunk 1.

## Step 8 - The Database
I started off creating the database via the console to understand exactly what I wanted.

I created a table called `hit-counters` with a partition key of `counter-name (string)`.  

I chose to customise settings and change read/write capacity to On-Demand, to better control costs.

Then, in Explore Items, I added an Item to the Table, and also added a new attribute `counter-value`.  I then had a table:

|counter-name|counter-value|
|---|---|
|cloud-resume|0|

Page 83.

## Step 9 - The Lambda API

## Step 10 - The Python Code

## Step 13 - Source Control

