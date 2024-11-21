---
title: "Hourly Heatmap of NYC Taxi Pickups by Location"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Hourly Heatmap of NYC Taxi Pickups by Location

This heatmap visualizes the distribution of taxi pickups across the top 20 most frequent pickup locations in New York City over a 24-hour period. The color intensity represents the number of trips, allowing viewers to identify peak hours and popular locations for taxi usage throughout the day.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH hourly_counts AS (
  SELECT 
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
    PULocationID,
    COUNT(*) AS trip_count
  FROM ds.yellow_trips
  GROUP BY 1, 2
),
top_locations AS (
  SELECT PULocationID
  FROM hourly_counts
  GROUP BY PULocationID
  ORDER BY SUM(trip_count) DESC
  LIMIT 20
)
SELECT 
  h.hour,
  h.PULocationID,
  h.trip_count
FROM hourly_counts h
JOIN top_locations t ON h.PULocationID = t.PULocationID
ORDER BY h.PULocationID, h.hour`
```


```js
function plotChart(data, {width} = {}) {
  const height = 500;
  const marginTop = 30;
  const marginRight = 30;
  const marginBottom = 40;
  const marginLeft = 60;

  // Convert Arrow table to array
  const dataArray = data.toArray();

  return Plot.plot({
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ":00",
      domain: d3.range(24)
    },
    y: {
      label: "Pickup Location ID",
      domain: d3.groupSort(dataArray, g => -d3.sum(g, d => d.trip_count), d => d.PULocationID)
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Number of Trips"
    },
    marks: [
      Plot.cell(dataArray, {
        x: d => d.hour,
        y: d => d.PULocationID,
        fill: d => d.trip_count,
        tip: true,
        title: d => `Location: ${d.PULocationID}\nHour: ${d.hour}:00\nTrips: ${d.trip_count}`
      })
    ]
  });
}

function displayError(message) {
    return html`<div style="color: red; text-align: center; padding: 20px;">Error: ${message}</div>`;
}

function plotOrError(data, options) {
    try {
        return plotChart(data, options);
    } catch (e) {
        return displayError(e.message);
    }
}
```


<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotOrError(data, {width}))}
    </div>
</div>

### Data

```js
display(Inputs.table(data));
```