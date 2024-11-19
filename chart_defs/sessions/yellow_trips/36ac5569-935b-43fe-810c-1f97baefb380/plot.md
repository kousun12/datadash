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
LIMIT 100
`
```


```js
function plotChart(data, {width} = {}) {
  const height = width * 0.7;
  
  // Get unique location IDs
  const locationIDs = new Set();
  for (let i = 0; i < data.numRows; i++) {
    locationIDs.add(data.getChild('PULocationID').get(i));
    locationIDs.add(data.getChild('DOLocationID').get(i));
  }
  const sortedLocationIDs = Array.from(locationIDs).sort((a, b) => a - b);
  
  return Plot.plot({
    width,
    height,
    marginLeft: 60,
    marginBottom: 60,
    color: {
      type: "log",
      scheme: "YlOrRd",
      label: "Trip Count"
    },
    x: {
      label: "Pickup Location ID",
      tickFormat: d => d,
      domain: sortedLocationIDs,
      padding: 0.1
    },
    y: {
      label: "Dropoff Location ID",
      tickFormat: d => d,
      domain: sortedLocationIDs,
      padding: 0.1
    },
    marks: [
      Plot.cell(data, {
        x: d => d.PULocationID,
        y: d => d.DOLocationID,
        fill: d => d.trip_count,
        tip: true
      }),
      Plot.text(data, {
        x: d => d.PULocationID,
        y: d => d.DOLocationID,
        text: d => d.trip_count.toString(),
        fill: "white",
        fontSize: 8
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