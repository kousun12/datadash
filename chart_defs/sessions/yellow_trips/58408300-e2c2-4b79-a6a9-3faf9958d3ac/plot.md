---
title: "Taxi Pickup Heatmap: Weekly Patterns in NYC"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Taxi Pickup Heatmap: Weekly Patterns in NYC

This heatmap visualizes the density of taxi pickups in New York City across different hours of the day and days of the week, revealing patterns in urban transportation demand.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH hourly_pickups AS (
  SELECT 
    EXTRACT(DOW FROM tpep_pickup_datetime) AS day_of_week,
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour_of_day,
    COUNT(*) AS pickup_count
  FROM ds.yellow_trips
  GROUP BY 1, 2
)
SELECT 
  day_of_week,
  hour_of_day,
  pickup_count
FROM hourly_pickups
ORDER BY day_of_week, hour_of_day`
```


```js
function plotChart(data, {width} = {}) {
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  
  return Plot.plot({
    width,
    height: 400,
    marginLeft: 60,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ":00"
    },
    y: {
      label: "Day of Week",
      domain: days
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Number of Pickups"
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour_of_day,
        y: d => days[d.day_of_week],
        fill: d => d.pickup_count,
        tip: true
      })
    ],
    facet: {
      data: data,
      y: d => days[d.day_of_week]
    },
    fy: {
      axis: "left"
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