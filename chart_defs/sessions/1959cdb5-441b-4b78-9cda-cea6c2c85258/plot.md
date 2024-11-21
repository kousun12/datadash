---
title: "MMM Stock Price Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---
```js
import {Editor} from "/components/Editor.js";
```

# MMM Stock Price Over Time

OHLC (Open, High, Low, Close) chart showing daily price movements for 3M Company (MMM) stock, with green lines indicating price increases and red lines indicating decreases.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/dji.db")});
```

```js
const data = db.sql`
SELECT 
    strftime(date, '%Y-%m-%d') AS date,
    open, 
    high, 
    low, 
    close, 
    volume
FROM ds.dji_data
WHERE ticker = 'MMM'
ORDER BY date
`
```


```js
function plotChart(data, options = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  const width = options.width || 960;
  const parseDate = d3.utcParse("%Y-%m-%d");

  const color = d => d.close > d.open ? "#4daf4a" : "#e41a1c";

  return Plot.plot({
    width,
    inset: 6,
    grid: true,
    style: {
      backgroundColor: "#f5f5f5",
    },
    x: {
      type: "utc",
      label: "Date",
      tickFormat: d3.utcFormat("%b %Y"),
    },
    y: {
      label: "↑ MMM stock price ($)",
    },
    color,
    marks: [
      Plot.ruleX(data, {
        x: d => parseDate(d.date),
        y1: "low",
        y2: "high",
        stroke: color,
      }),
      Plot.ruleX(data, {
        x: d => parseDate(d.date),
        y1: "open",
        y2: "close",
        stroke: color,
        strokeWidth: 4,
        strokeLinecap: "round",
      }),
    ],
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
  const plotCodeString = "function plotChart(data, options = {}) {\n  if (!data || data.numRows === 0) {\n    return displayError(\"No data available to plot.\");\n  }\n\n  const width = options.width || 960;\n  const parseDate = d3.utcParse(\"%Y-%m-%d\");\n\n  const color = d => d.close > d.open ? \"#4daf4a\" : \"#e41a1c\";\n\n  return Plot.plot({\n    width,\n    inset: 6,\n    grid: true,\n    style: {\n      backgroundColor: \"#f5f5f5\",\n    },\n    x: {\n      type: \"utc\",\n      label: \"Date\",\n      tickFormat: d3.utcFormat(\"%b %Y\"),\n    },\n    y: {\n      label: \"\u2191 MMM stock price ($)\",\n    },\n    color,\n    marks: [\n      Plot.ruleX(data, {\n        x: d => parseDate(d.date),\n        y1: \"low\",\n        y2: \"high\",\n        stroke: color,\n      }),\n      Plot.ruleX(data, {\n        x: d => parseDate(d.date),\n        y1: \"open\",\n        y2: \"close\",\n        stroke: color,\n        strokeWidth: 4,\n        strokeLinecap: \"round\",\n      }),\n    ],\n  });\n}\n";
  const e = Editor({value: plotCodeString, lang: "javascript"});
  return e;
}
function getSQLView() {
    const sqlString = `SELECT 
    strftime(date, '%Y-%m-%d') AS date,
    open, 
    high, 
    low, 
    close, 
    volume
FROM ds.dji_data
WHERE ticker = 'MMM'
ORDER BY date
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