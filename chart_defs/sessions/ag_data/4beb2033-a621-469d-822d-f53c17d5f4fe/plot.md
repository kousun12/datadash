---
title: "Agricultural Commodity Type Trends (2010-Present)"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Type Trends (2010-Present)

This stacked area chart displays trends for agricultural commodity types, showing the total value of beginning stocks, production, and imports from 2010 onwards. The chart allows for easy comparison of trends across different commodity types over time.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
SELECT 
  "Commodity Type",
  "Marketing/calendar year" AS Year,
  SUM(CAST("Value text" AS FLOAT)) AS TotalValue
FROM ds.ag_data
WHERE "Marketing/calendar year" >= '2010/11'
  AND Attribute IN ('Beginning stocks', 'Production', 'Imports')
GROUP BY "Commodity Type", "Marketing/calendar year"
ORDER BY "Commodity Type", "Marketing/calendar year"
`
```


```js
function plotChart(data, {width} = {}) {
  const height = 500;
  const margin = {top: 20, right: 30, bottom: 40, left: 60};

  return Plot.plot({
    width,
    height,
    margin,
    x: {
      label: "Year",
      tickFormat: d => d.slice(0, 4)
    },
    y: {
      label: "Total Value",
      grid: true,
      transform: d => d / 1e9,
      tickFormat: d => d.toFixed(1) + "B"
    },
    color: {
      legend: true,
      scheme: "category10"
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: d => d.Year,
        y: d => d.TotalValue,
        z: d => d["Commodity Type"],
        fill: d => d["Commodity Type"],
        title: d => `${d["Commodity Type"]}\nYear: ${d.Year}\nValue: ${d.TotalValue.toLocaleString()}`
      })),
      Plot.ruleY([0])
    ],
    style: {
      fontSize: "12px"
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