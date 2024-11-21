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

This line chart visualizes the number of taxi pickups across the top 10 most popular zones in New York City, broken down by hour of the day. Each line represents a different zone, allowing viewers to compare pickup patterns and identify peak hours across different locations.


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
  LIMIT 10
)
SELECT hp.Zone, hp.hour, hp.pickup_count
FROM hourly_pickups hp
JOIN top_zones tz ON hp.Zone = tz.Zone
ORDER BY hp.Zone, hp.hour
`
```


```js
function plotChart(data, {width} = {}) {
  const margin = {top: 20, right: 200, bottom: 40, left: 60};

  return Plot.plot({
    width,
    height: 500,
    marginTop: margin.top,
    marginRight: margin.right,
    marginBottom: margin.bottom,
    marginLeft: margin.left,
    x: {
      label: "Hour of Day",
      domain: [0, 23],
      tickFormat: d => d.toString().padStart(2, '0') + ':00'
    },
    y: {
      label: "Pickup Count",
      grid: true
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
        r: 3
      }),
      Plot.ruleY([0]),
      Plot.text(data, Plot.selectLast({
        x: "hour",
        y: "pickup_count",
        z: "Zone",
        text: "Zone",
        textAnchor: "start",
        dx: 5
      }))
    ],
    color: {
      scheme: "tableau10"
    },
    tip: {
      format: {
        x: x => `Hour: ${x.toString().padStart(2, '0')}:00`,
        y: y => `Pickups: ${y.toLocaleString()}`
      }
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
  const plotCodeString = "function plotChart(data, {width} = {}) {\n  const margin = {top: 20, right: 200, bottom: 40, left: 60};\n\n  return Plot.plot({\n    width,\n    height: 500,\n    marginTop: margin.top,\n    marginRight: margin.right,\n    marginBottom: margin.bottom,\n    marginLeft: margin.left,\n    x: {\n      label: \"Hour of Day\",\n      domain: [0, 23],\n      tickFormat: d => d.toString().padStart(2, '0') + ':00'\n    },\n    y: {\n      label: \"Pickup Count\",\n      grid: true\n    },\n    color: {\n      legend: true\n    },\n    marks: [\n      Plot.line(data, {\n        x: \"hour\",\n        y: \"pickup_count\",\n        stroke: \"Zone\",\n        strokeWidth: 2,\n        curve: \"monotone-x\"\n      }),\n      Plot.dot(data, {\n        x: \"hour\",\n        y: \"pickup_count\",\n        stroke: \"Zone\",\n        fill: \"white\",\n        r: 3\n      }),\n      Plot.ruleY([0]),\n      Plot.text(data, Plot.selectLast({\n        x: \"hour\",\n        y: \"pickup_count\",\n        z: \"Zone\",\n        text: \"Zone\",\n        textAnchor: \"start\",\n        dx: 5\n      }))\n    ],\n    color: {\n      scheme: \"tableau10\"\n    },\n    tip: {\n      format: {\n        x: x => `Hour: ${x.toString().padStart(2, '0')}:00`,\n        y: y => `Pickups: ${y.toLocaleString()}`\n      }\n    }\n  });\n}\n";
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
  LIMIT 10
)
SELECT hp.Zone, hp.hour, hp.pickup_count
FROM hourly_pickups hp
JOIN top_zones tz ON hp.Zone = tz.Zone
ORDER BY hp.Zone, hp.hour
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