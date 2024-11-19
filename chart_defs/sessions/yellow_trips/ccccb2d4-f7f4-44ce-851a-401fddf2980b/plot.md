---
title: "Hourly Taxi Pickup Patterns in New York City"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Hourly Taxi Pickup Patterns in New York City

This chart visualizes the density of taxi pickups across different locations in New York City over 24 hours, revealing popular areas and temporal trends in taxi usage throughout the day.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH hourly_pickups AS (
  SELECT 
    PULocationID,
    date_trunc('hour', tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS pickup_count
  FROM ds.yellow_trips
  GROUP BY PULocationID, pickup_hour
)
SELECT 
  hp.PULocationID,
  hp.pickup_hour,
  hp.pickup_count
FROM hourly_pickups hp
ORDER BY hp.pickup_hour, hp.pickup_count DESC`
```


```js
function plotChart(data, {width} = {}) {
  const height = width * 0.6;
  const margin = {top: 20, right: 30, bottom: 40, left: 40};

  // Get unique hours for the slider
  const hours = Array.from(new Set(data.getChild('pickup_hour').toArray().map(d => d.getHours()))).sort((a, b) => a - b);

  // Create a color scale
  const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data.getChild('pickup_count').toArray())]);

  // Create the plot
  return Plot.plot({
    width,
    height,
    margin,
    style: {
      fontFamily: "sans-serif",
      background: "#f0f0f0"
    },
    x: {
      label: "PULocationID",
      nice: true
    },
    y: {
      label: "Pickup Count",
      nice: true
    },
    color: {
      type: "sequential",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.dot(data, {
        x: "PULocationID",
        y: "pickup_count",
        r: d => Math.sqrt(d.pickup_count) / 2,
        fill: d => colorScale(d.pickup_count),
        title: d => `Location ID: ${d.PULocationID}\nPickups: ${d.pickup_count}`,
        opacity: 0.7
      })
    ],
    facet: {
      data: data,
      x: d => d.pickup_hour.getHours(),
      label: "Hour of Day"
    },
    fx: {
      domain: hours,
      label: "Hour"
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