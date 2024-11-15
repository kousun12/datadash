---
title: "Agricultural Commodity Beginning Stocks Trends (1990-Present)"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Beginning Stocks Trends (1990-Present)

This interactive chart displays the beginning stocks for various agricultural commodities from 1990 onwards, allowing comparison between crops and livestock/dairy products across different units of measurement.


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
  WHERE Attribute = 'Beginning stocks'
    AND "Marketing/calendar year" >= '1990/91'
)
SELECT *
FROM filtered_data
ORDER BY year, commodity_type, Commodity`
```


```js
function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    marginRight: 80,
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
        fill: "commodity_type"
      }),
      Plot.text(data, Plot.selectLast({
        x: "year",
        y: "value",
        text: d => d.commodity,
        dx: 3,
        dy: -3,
        anchor: "start",
        fontSize: 10
      })),
      Plot.tip(data, Plot.pointerX({
        x: "year",
        y: "value",
        title: d => `${d.commodity} (${d.commodity_type})\nYear: ${d.year}\nValue: ${d.value} ${d.unit}`
      }))
    ],
    facet: {
      data: data,
      y: "unit"
    },
    fy: {
      label: "Unit"
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