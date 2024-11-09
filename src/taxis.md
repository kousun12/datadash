---
theme: dashboard
title: NYC Taxi Data Exploration
toc: false
---

# NYC Taxi Data Exploration with DuckDB, Parquet, and Observable

In this notebook, we'll load NYC Taxi data from Parquet files using DuckDB, and perform basic data exploration and visualization using Observable's built-in features.

---

## Initialize DuckDB

Let’s set up and initialize DuckDB within Observable’s environment. We are loading the DuckDBClient library here.

```js
import * as duckdb from "npm:@duckdb/duckdb-wasm";
import duckdbWasm from "npm:@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm";
import duckdbWorker from "npm:@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js";

const DUCKDB_CONFIG = {
  mainModule: duckdbWasm,
  mainWorker: duckdbWorker,
};

const db = await (async () => {
  const worker = await duckdb.createWorker(DUCKDB_CONFIG);
  const logger = new duckdb.ConsoleLogger();
  const db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate();
  return db;
})();
```

## Load NYC Taxi Parquet Data

Next, we’ll connect to the NYC TLC Taxi Parquet dataset, which you can host if you don't have direct access yet:

```js
taxi_data = {
  const conn = await db.connect();
  try {
    await conn.query(`
      CREATE TABLE taxi_data AS 
      SELECT * 
      FROM read_parquet('https://media.substrate.run/yellow_tripdata_2024-01.parquet')
    `);
    return await conn.query(`SELECT * FROM taxi_data LIMIT 10`);
  } finally {
    await conn.close();
  }
}
```

⚠️ **Note**: If you don't have a ready-to-use URL for NYC taxi data stored as a parquet, you’d need to upload the data to an accessible link or adjust this notebook with your own setup.

## Preview Loaded Data

Let’s run a query to inspect the first few rows of the dataset.

```js
data = await db.query(`SELECT * FROM taxi_data LIMIT 10`);
data
```

The table should display some fields like:
- `pickup_datetime`
- `dropoff_datetime`
- `trip_distance`
- `fare_amount`
- `tip_amount`

Try running and inspecting the schema to ensure the data appears correctly.

## Basic Summary Statistics

Let’s start by summarizing the data. We can use DuckDB to compute some aggregate statistics over the data, such as the number of trips, average fare, and average trip distance.

```js
summary = await db.query(`SELECT 
    COUNT(*) AS num_trips, 
    AVG(trip_distance) AS avg_distance, 
    AVG(fare_amount) AS avg_fare, 
    AVG(tip_amount) AS avg_tip 
FROM taxi_data`);

summary
```

## Visualizing Trip Distance Distribution

Now, we’ll use `Plot` from Observable to visualize the distribution of trip distances. You may want to filter or limit datasets for performance, especially with large datasets.

```js
import { Plot } from define1;

trip_distances = await db.query(`SELECT trip_distance FROM taxi_data WHERE trip_distance < 20 LIMIT 10000`);

Plot.plot({
  marks: [
    Plot.barY(trip_distances, Plot.binX({y: "count"}, {x: "trip_distance", thresholds: 20}))
  ],
  x: {
    label: "Trip Distance (miles)"
  },
  y: {
    label: "Number of Trips"
  }
})
```

### Interactive: Time Series of Taxi Demand

Let's visualize how taxi demand evolves over time by plotting a time series of the number of trips per day:

```js
time_series = await db.query(`
  SELECT 
    CAST(pickup_datetime AS DATE) AS date, 
    COUNT(*) AS num_trips 
  FROM taxi_data 
  GROUP BY CAST(pickup_datetime AS DATE) 
  ORDER BY date
`);

Plot.plot({
  marks: [
    Plot.line(time_series, {x: "date", y: "num_trips"})
  ],
  x: {
    label: "Date"
  },
  y: {
    label: "Number of Trips"
  }
})
```
