---
title: "U.S. Agricultural Crop Beginning Stocks Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# U.S. Agricultural Crop Beginning Stocks Over Time

This stacked area chart displays the beginning stocks of various crops in million bushels across different marketing years, allowing for easy comparison of crop quantities and trends over time.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH crop_stocks AS (
  SELECT 
    "Marketing/calendar year" as year,
    Commodity,
    "Value text" as value
  FROM ds.ag_data
  WHERE "Commodity Type" = 'Crops'
    AND Attribute = 'Beginning stocks'
    AND Unit = 'Million bushels'
)
SELECT *
FROM crop_stocks
ORDER BY year, Commodity`
```


```js
function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    y: {grid: true, label: "Beginning stocks (Million bushels)"},
    x: {label: "Marketing Year"},
    color: {legend: true},
    marks: [
      Plot.areaY(data, {
        x: "year",
        y: "value",
        fill: "Commodity",
        stroke: "Commodity",
        tip: true,
        title: d => `${d.Commodity}\nYear: ${d.year}\nValue: ${d.value.toFixed(2)} Million bushels`
      }),
      Plot.ruleY([0])
    ],
    style: {
      fontSize: 12
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