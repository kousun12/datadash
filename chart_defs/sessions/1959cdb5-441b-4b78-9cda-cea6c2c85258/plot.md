---
title: "MMM Stock Price and Volume Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---
```js
import {Editor} from "/components/Editor.js";
```

# MMM Stock Price and Volume Over Time

Candlestick chart showing daily price movements and trading volume for 3M Company (MMM) stock, with green candles indicating price increases and red candles indicating decreases.


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
function plotChart(data, {width} = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  const height = 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 30;
  const marginLeft = 40;

  const volumeHeight = 100;
  const priceHeight = height - volumeHeight - marginTop - marginBottom;

  // Parse date strings to Date objects
  const parseDate = d3.utcParse("%Y-%m-%d");

  // Helper function to safely parse dates
  const safeParseDate = (dateString) => {
    if (!dateString) return null;
    return parseDate(dateString);
  };

  // Helper function to safely format dates
  const safeFormatDate = (date) => {
    if (!date) return "N/A";
    return d3.utcFormat("%b %Y")(date);
  };

  return Plot.plot({
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    y: {
      grid: true,
      label: "Price ($)"
    },
    x: {
      type: "band",
      label: "Date"
    },
    marks: [
      Plot.ruleY([0]),
      Plot.rect(data, {
        x: d => d.date,
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.open > d.close ? "red" : "green",
        tip: true,
        title: d => {
          const date = safeParseDate(d.date);
          return `Date: ${safeFormatDate(date)}\nOpen: $${d.open.toFixed(2)}\nClose: $${d.close.toFixed(2)}\nHigh: $${d.high.toFixed(2)}\nLow: $${d.low.toFixed(2)}\nVolume: ${d.volume.toLocaleString()}`;
        }
      }),
      Plot.ruleY(data, {
        x: d => d.date,
        y1: d => d.low,
        y2: d => d.high,
        stroke: d => d.open > d.close ? "red" : "green"
      }),
      Plot.rectY(data, {
        x: d => d.date,
        y: d => d.volume,
        fill: "lightblue",
        fillOpacity: 0.5,
      }),
      Plot.axisX({
        label: "Date",
        tickFormat: d => safeFormatDate(parseDate(d))
      }),
      Plot.axisY({
        label: "Price ($)",
        tickFormat: ".0f"
      }),
      Plot.axisY({
        label: "Volume",
        tickFormat: "~s",
        ticks: 3,
        y: d => d.volume,
      })
    ],
    facet: {
      data: data,
      y: d => d.volume ? "Volume" : "Price",
      marginTop: 30
    },
    fy: {
      axis: null
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
  const plotCodeString = "function plotChart(data, {width} = {}) {\n  if (!data || data.numRows === 0) {\n    return displayError(\"No data available to plot.\");\n  }\n\n  const height = 500;\n  const marginTop = 20;\n  const marginRight = 30;\n  const marginBottom = 30;\n  const marginLeft = 40;\n\n  const volumeHeight = 100;\n  const priceHeight = height - volumeHeight - marginTop - marginBottom;\n\n  // Parse date strings to Date objects\n  const parseDate = d3.utcParse(\"%Y-%m-%d\");\n\n  // Helper function to safely parse dates\n  const safeParseDate = (dateString) => {\n    if (!dateString) return null;\n    return parseDate(dateString);\n  };\n\n  // Helper function to safely format dates\n  const safeFormatDate = (date) => {\n    if (!date) return \"N/A\";\n    return d3.utcFormat(\"%b %Y\")(date);\n  };\n\n  return Plot.plot({\n    width,\n    height,\n    marginTop,\n    marginRight,\n    marginBottom,\n    marginLeft,\n    y: {\n      grid: true,\n      label: \"Price ($)\"\n    },\n    x: {\n      type: \"band\",\n      label: \"Date\"\n    },\n    marks: [\n      Plot.ruleY([0]),\n      Plot.rect(data, {\n        x: d => d.date,\n        y1: d => Math.min(d.open, d.close),\n        y2: d => Math.max(d.open, d.close),\n        fill: d => d.open > d.close ? \"red\" : \"green\",\n        tip: true,\n        title: d => {\n          const date = safeParseDate(d.date);\n          return `Date: ${safeFormatDate(date)}\\nOpen: $${d.open.toFixed(2)}\\nClose: $${d.close.toFixed(2)}\\nHigh: $${d.high.toFixed(2)}\\nLow: $${d.low.toFixed(2)}\\nVolume: ${d.volume.toLocaleString()}`;\n        }\n      }),\n      Plot.ruleY(data, {\n        x: d => d.date,\n        y1: d => d.low,\n        y2: d => d.high,\n        stroke: d => d.open > d.close ? \"red\" : \"green\"\n      }),\n      Plot.rectY(data, {\n        x: d => d.date,\n        y: d => d.volume,\n        fill: \"lightblue\",\n        fillOpacity: 0.5,\n      }),\n      Plot.axisX({\n        label: \"Date\",\n        tickFormat: d => safeFormatDate(parseDate(d))\n      }),\n      Plot.axisY({\n        label: \"Price ($)\",\n        tickFormat: \".0f\"\n      }),\n      Plot.axisY({\n        label: \"Volume\",\n        tickFormat: \"~s\",\n        ticks: 3,\n        y: d => d.volume,\n      })\n    ],\n    facet: {\n      data: data,\n      y: d => d.volume ? \"Volume\" : \"Price\",\n      marginTop: 30\n    },\n    fy: {\n      axis: null\n    }\n  });\n}\n";
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