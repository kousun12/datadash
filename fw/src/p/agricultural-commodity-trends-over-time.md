---
title: "Agricultural Commodity Trends Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Trends Over Time

This chart displays historical and projected values for various agricultural commodities, separated into crops and livestock/dairy categories. It allows for comparison of trends across different commodities and years, providing insights into production, stocks, and market dynamics in the agricultural sector.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
SELECT 
  "Marketing/calendar year" as year,
  Commodity,
  Attribute,
  Unit,
  "Value text" as value,
  "Commodity Type" as commodity_type
FROM ds.ag_data
ORDER BY "Marketing/calendar year"`
```


```js
function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    marginRight: 40,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
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
        stroke: "commodity",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(data, {
        x: "year",
        y: "value",
        stroke: "commodity",
        fill: "white",
        title: d => `${d.commodity}: ${d.attribute}\nValue: ${d.value} ${d.unit}\nYear: ${d.year}`
      }),
      Plot.text(data, Plot.selectLast({
        x: "year",
        y: "value",
        text: d => d.commodity,
        dx: 3,
        anchor: "start"
      }))
    ],
    facet: {
      data,
      y: "commodity_type"
    },
    fy: {
      domain: ["Crops", "Livestock/Dairy"]
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