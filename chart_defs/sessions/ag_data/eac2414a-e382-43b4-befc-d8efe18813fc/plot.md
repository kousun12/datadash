---
title: "Crop Beginning Stocks Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Crop Beginning Stocks Over Time

This chart displays the beginning stocks for various crops in million bushels across different marketing years, allowing for easy comparison of trends between commodities.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    Commodity,
    "Commodity Type",
    Attribute,
    Unit,
    "Value text" AS value
  FROM ds.ag_data
  WHERE "Commodity Type" = 'Crops'
    AND Attribute = 'Beginning stocks'
    AND Unit = 'Million bushels'
)
SELECT * FROM filtered_data
ORDER BY year, Commodity`
```


```js
function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    marginRight: 100,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
    },
    y: {
      label: "Value (Million bushels)",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(data, {
        x: "year",
        y: "value",
        stroke: "Commodity",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(data, {
        x: "year",
        y: "value",
        stroke: "Commodity",
        fill: "white",
        title: d => `${d.Commodity}\nYear: ${d.year}\nValue: ${d.value}`
      }),
      Plot.ruleY([0])
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

```js
display(Inputs.table(data));
```