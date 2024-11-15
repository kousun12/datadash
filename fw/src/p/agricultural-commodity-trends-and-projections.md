---
title: "Agricultural Commodity Trends and Projections"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Trends and Projections

Interactive visualization of U.S. agricultural data showing trends in crop and livestock commodities over time, including production, stocks, and other key attributes.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    "Commodity Type" AS commodity_type,
    Commodity,
    Attribute,
    Unit,
    "Value text" AS value
  FROM ds.ag_data
  WHERE "Value text" IS NOT NULL
)
SELECT * FROM filtered_data
ORDER BY year, commodity_type, Commodity, Attribute`
```


```js
function plotChart(data, {width} = {}) {
  // NB data is an Apache Arrow table
  return Plot.plot({
    width,
    height: 500,
    marginRight: 120,
    x: {
      type: "time",
      label: "Year",
      tickFormat: "%Y"
    },
    y: {
      label: "Value",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(data, {
        x: "year",
        y: "value",
        stroke: d => `${d.Commodity} - ${d.Attribute}`,
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.text(data, Plot.selectLast({
        x: "year",
        y: "value",
        z: d => `${d.Commodity} - ${d.Attribute}`,
        text: d => `${d.Commodity} - ${d.Attribute}`,
        dx: 3,
        alignLeft: true
      })),
      Plot.tip(data, Plot.pointerX({
        x: "year",
        y: "value",
        title: d => `${d.Commodity} - ${d.Attribute}\nYear: ${d.year}\nValue: ${d.value} ${d.Unit}`
      }))
    ],
    facet: {
      data,
      y: "commodity_type"
    },
    fy: {
      label: "Commodity Type"
    }
  });
}
```


<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotChart(data, {width}))}
    </div>
</div>

```js
display(Inputs.table(data));
```