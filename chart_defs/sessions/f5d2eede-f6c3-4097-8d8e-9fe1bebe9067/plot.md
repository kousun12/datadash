---
title: "Hourly Taxi Pickup Line Chart for Top 10 Zones in NYC"
toc: false
sidebar: false
header: false
footer: false
pager: false

---
```js
import {Editor} from "/components/Editor.js";
```

# Hourly Taxi Pickup Line Chart for Top 10 Zones in NYC

This line chart visualizes the number of taxi pickups across the top 10 most popular zones in New York City, broken down by hour of the day. Each line represents a different zone, allowing viewers to easily compare patterns and trends across different locations and times.


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
  SELECT Zone, SUM(pickup_count) as total_pickups
  FROM hourly_pickups
  GROUP BY Zone
  ORDER BY total_pickups DESC
  LIMIT 10
)
SELECT hp.Zone, hp.hour, hp.pickup_count, tz.total_pickups
FROM hourly_pickups hp
JOIN top_zones tz ON hp.Zone = tz.Zone
ORDER BY tz.total_pickups DESC, hp.hour
`
```


```js
function plotChart(data, {width} = {}) {
  const margin = {top: 40, right: 160, bottom: 60, left: 60};

  return Plot.plot({
    width,
    height: 600,
    marginTop: margin.top,
    marginRight: margin.right,
    marginBottom: margin.bottom,
    marginLeft: margin.left,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ':00'
    },
    y: {
      label: "Pickup Count",
      axis: "left"
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(data, {
        x: "hour",
        y: "pickup_count",
        stroke: "Zone",
        strokeWidth: 2,
        curve: "monotone-x"
      }),
      Plot.dot(data, {
        x: "hour",
        y: "pickup_count",
        stroke: "Zone",
        fill: "white",
        title: d => `Zone: ${d.Zone}\nHour: ${d.hour.toString().padStart(2, '0')}:00\nPickups: ${d.pickup_count.toLocaleString()}\nTotal Pickups: ${d.total_pickups.toLocaleString()}`,
      }),
      Plot.text(data, Plot.selectLast({
        x: d => 24,
        y: "pickup_count",
        text: "Zone",
        dx: 6,
        fontSize: 10,
        textAnchor: "start"
      }))
    ],
    tip: true,
    color: {
      legend: true,
      scheme: "tableau10"
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

```js
function getJSView() {
  const plotCodeString = "function plotChart(data, {width} = {}) {\n  const margin = {top: 40, right: 160, bottom: 60, left: 60};\n\n  return Plot.plot({\n    width,\n    height: 600,\n    marginTop: margin.top,\n    marginRight: margin.right,\n    marginBottom: margin.bottom,\n    marginLeft: margin.left,\n    x: {\n      label: \"Hour of Day\",\n      tickFormat: d => d.toString().padStart(2, '0') + ':00'\n    },\n    y: {\n      label: \"Pickup Count\",\n      axis: \"left\"\n    },\n    color: {\n      legend: true\n    },\n    marks: [\n      Plot.line(data, {\n        x: \"hour\",\n        y: \"pickup_count\",\n        stroke: \"Zone\",\n        strokeWidth: 2,\n        curve: \"monotone-x\"\n      }),\n      Plot.dot(data, {\n        x: \"hour\",\n        y: \"pickup_count\",\n        stroke: \"Zone\",\n        fill: \"white\",\n        title: d => `Zone: ${d.Zone}\\nHour: ${d.hour.toString().padStart(2, '0')}:00\\nPickups: ${d.pickup_count.toLocaleString()}\\nTotal Pickups: ${d.total_pickups.toLocaleString()}`,\n      }),\n      Plot.text(data, Plot.selectLast({\n        x: d => 24,\n        y: \"pickup_count\",\n        text: \"Zone\",\n        dx: 6,\n        fontSize: 10,\n        textAnchor: \"start\"\n      }))\n    ],\n    tip: true,\n    color: {\n      legend: true,\n      scheme: \"tableau10\"\n    }\n  });\n}\n";
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
  SELECT Zone, SUM(pickup_count) as total_pickups
  FROM hourly_pickups
  GROUP BY Zone
  ORDER BY total_pickups DESC
  LIMIT 10
)
SELECT hp.Zone, hp.hour, hp.pickup_count, tz.total_pickups
FROM hourly_pickups hp
JOIN top_zones tz ON hp.Zone = tz.Zone
ORDER BY tz.total_pickups DESC, hp.hour
`;
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