---
title: "NYC Taxi Trip Heatmap: Popular Routes"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# NYC Taxi Trip Heatmap: Popular Routes

This heatmap visualizes the frequency of taxi trips between different locations in New York City, highlighting the most common routes and busiest areas for taxi services.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH trip_counts AS (
  SELECT 
    PULocationID, 
    DOLocationID, 
    COUNT(*) as trip_count
  FROM ds.yellow_trips
  GROUP BY PULocationID, DOLocationID
)
SELECT * FROM trip_counts
ORDER BY trip_count DESC
LIMIT 10000`
```


```js
function plotChart(data, {width} = {}) {
  const height = width * 0.7;
  
  // Get the maximum values for PULocationID and DOLocationID
  const maxPULocationID = d3.max(data, d => d.PULocationID);
  const maxDOLocationID = d3.max(data, d => d.DOLocationID);
  
  return Plot.plot({
    width,
    height,
    color: {
      type: "log",
      scheme: "YlOrRd"
    },
    x: {
      label: "Pickup Location ID",
      domain: d3.range(1, maxPULocationID + 1)
    },
    y: {
      label: "Dropoff Location ID",
      domain: d3.range(1, maxDOLocationID + 1)
    },
    marks: [
      Plot.cell(data, {
        x: "PULocationID",
        y: "DOLocationID",
        fill: "trip_count",
        tip: true
      }),
      Plot.text(data, {
        x: "PULocationID",
        y: "DOLocationID",
        text: d => d.trip_count > 1000 ? d.trip_count.toString() : "",
        fill: "white"
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