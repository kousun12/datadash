---
title: "New York City Taxi Trip Heatmap"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# New York City Taxi Trip Heatmap

Visualizes the density of taxi trips across different times of day and days of the week, revealing patterns in urban transportation demand.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH trip_counts AS (
  SELECT 
    EXTRACT(DOW FROM tpep_pickup_datetime) AS day_of_week,
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour_of_day,
    COUNT(*) AS trip_count
  FROM ds.yellow_trips
  GROUP BY 1, 2
)
SELECT 
  day_of_week,
  hour_of_day,
  trip_count
FROM trip_counts
ORDER BY day_of_week, hour_of_day`
```


```js
function plotChart(data, {width} = {}) {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const hours = Array.from({length: 24}, (_, i) => i);

  return Plot.plot({
    width,
    height: Math.min(400, width * 0.7),
    color: {
      type: "linear",
      scheme: "YlOrRd",
      legend: true,
      label: "Number of trips"
    },
    x: {
      label: "Hour of day",
      tickFormat: d => d.toString().padStart(2, '0') + ':00'
    },
    y: {
      label: "Day of week",
      domain: days
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour_of_day,
        y: d => days[d.day_of_week],
        fill: d => d.trip_count,
        tip: true
      })
    ],
    marginLeft: 60,
    marginBottom: 50,
    style: {
      fontSize: 12
    }
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