---
title: "Hourly Taxi Pickup Heatmap for Top 20 Zones in NYC"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Hourly Taxi Pickup Heatmap for Top 20 Zones in NYC

This heatmap visualizes the number of taxi pickups across the top 20 most popular zones in New York City, broken down by hour of the day. The color intensity represents the pickup count, allowing viewers to identify peak hours and busy locations at a glance.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/yellow_trips.db")});
```

```js
const data = db.sql`
WITH hourly_pickups AS (
  SELECT 
    z.Zone,
    EXTRACT(HOUR FROM y.tpep_pickup_datetime) AS hour,
    COUNT(*) AS pickup_count
  FROM ds.yellow_trips y
  JOIN ds.zones z ON y.PULocationID = z.LocationID
  GROUP BY z.Zone, EXTRACT(HOUR FROM y.tpep_pickup_datetime)
),
top_zones AS (
  SELECT Zone
  FROM hourly_pickups
  GROUP BY Zone
  ORDER BY SUM(pickup_count) DESC
  LIMIT 20
)
SELECT hp.Zone, hp.hour, hp.pickup_count
FROM hourly_pickups hp
JOIN top_zones tz ON hp.Zone = tz.Zone
ORDER BY hp.Zone, hp.hour`
```


```js
function plotChart(data, {width} = {}) {
  const margin = {top: 40, right: 100, bottom: 60, left: 200};

  return Plot.plot({
    width,
    marginLeft: margin.left,
    marginRight: margin.right,
    marginTop: margin.top,
    marginBottom: margin.bottom,
    x: {
      label: "Hour of Day",
    },
    y: {
      label: null,
      domain: d3.groupSort(data, g => d3.sum(g, d => d.pickup_count), d => d.Zone)
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour,
        y: d => d.Zone,
        fill: d => d.pickup_count,
        tip: true,
        title: d => `${d.Zone}\nPickups: ${d.pickup_count.toLocaleString()}`
      }),
      Plot.text(data, Plot.groupY({x: "count"}, {
        y: d => d.Zone,
        text: d => d.Zone,
        dx: -10,
        dy: 0,
        fontSize: 9,
        textAnchor: "end"
      }))
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