---
title: "Hourly Taxi Pickup Heatmap for Top 20 Zones in NYC"
toc: false
sidebar: false
header: false
footer: false
pager: false

---
```js
import {Editor} from "/components/Editor.js";
```

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
  const margin = {top: 40, right: 200, bottom: 60, left: 200};

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
      scheme: "YlGn",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour,
        y: d => d.Zone,
        fill: d => d.pickup_count,
        tip: true,
        title: d => `${d.Zone}\nHour: ${d.hour}:00\nPickups: ${d.pickup_count.toLocaleString()}`
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

```js
function getJSView() {
  const plotCodeString = "function plotChart(data, {width} = {}) {\n  const margin = {top: 40, right: 200, bottom: 60, left: 200};\n\n  return Plot.plot({\n    width,\n    marginLeft: margin.left,\n    marginRight: margin.right,\n    marginTop: margin.top,\n    marginBottom: margin.bottom,\n    x: {\n      label: \"Hour of Day\",\n    },\n    y: {\n      label: null,\n      domain: d3.groupSort(data, g => d3.sum(g, d => d.pickup_count), d => d.Zone)\n    },\n    color: {\n      type: \"linear\",\n      scheme: \"YlGn\",\n      label: \"Pickup Count\",\n      legend: true\n    },\n    marks: [\n      Plot.cell(data, {\n        x: d => d.hour,\n        y: d => d.Zone,\n        fill: d => d.pickup_count,\n        tip: true,\n        title: d => `${d.Zone}\\nHour: ${d.hour}:00\\nPickups: ${d.pickup_count.toLocaleString()}`\n      }),\n      Plot.text(data, Plot.groupY({x: \"count\"}, {\n        y: d => d.Zone,\n        text: d => d.Zone,\n        dx: -10,\n        dy: 0,\n        fontSize: 9,\n        textAnchor: \"end\"\n      }))\n    ]\n  });\n}\n";
  const e = Editor({value: plotCodeString, lang: "javascript"});
  return e;
}
function getSQLView() {
    const sqlString = `WITH hourly_pickups AS (
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
ORDER BY hp.Zone, hp.hour`;
    const e = Editor({value: sqlString, lang: "sql"});
    return e;
}
```

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotOrError(data, {width}))}
    </div>
</div>

### Raw Code

The following shows the `Plot` code as well as the `sql` used to drive the above visualizations.

<div class="grid grid-cols-2">
    <div class="card">
        ${getJSView()}
    </div>
    <div class="card">
        ${getSQLView()}
    </div>
</div>

### Data

This is the raw data resulting from the SQL query.

```js
display(Inputs.table(data));
```