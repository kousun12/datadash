---
title: "Heatmap of Taxi Pickups in New York City by Zone"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Heatmap of Taxi Pickups in New York City by Zone

This visualization shows the frequency of taxi pickups across different zones in New York City. Each cell represents a unique taxi zone, with color intensity indicating the number of pickups. Darker colors represent higher pickup frequencies, providing insight into the most popular pickup areas. Hover over cells to see the zone name, location ID, and exact pickup count.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH pickup_counts AS (
  SELECT PULocationID, COUNT(*) as pickup_count
  FROM ds.yellow_trips
  GROUP BY PULocationID
)
SELECT 
  y.PULocationID,
  COALESCE(p.pickup_count, 0) as pickup_count,
  COALESCE(z.Zone, 'Unknown') as zone_name
FROM ds.yellow_trips y
LEFT JOIN pickup_counts p ON y.PULocationID = p.PULocationID
LEFT JOIN taxi_zone_lookup z ON y.PULocationID = z.LocationID
GROUP BY y.PULocationID, p.pickup_count, z.Zone
ORDER BY pickup_count DESC
`
```


```js
function plotChart(data, {width} = {}) {
  const height = width * 0.6;
  const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.pickup_count)]);

  return Plot.plot({
    width,
    height,
    style: {
      fontFamily: "sans-serif",
      background: "#f0f0f0"
    },
    color: {
      type: "sequential",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.PULocationID % 10,
        y: d => Math.floor(d.PULocationID / 10),
        fill: d => d.pickup_count,
        title: d => `Zone: ${d.zone_name}\nLocation ID: ${d.PULocationID}\nPickups: ${d.pickup_count.toLocaleString()}`,
      })
    ],
    x: {
      label: "Location ID (mod 10)",
      nice: true
    },
    y: {
      label: "Location ID (div 10)",
      nice: true
    },
    marginTop: 40,
    marginRight: 40,
    marginBottom: 40,
    marginLeft: 40,
    caption: "Heatmap of Taxi Pickups by Zone"
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