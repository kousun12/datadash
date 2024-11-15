---
title: "Agricultural Commodity Beginning Stocks Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Beginning Stocks Over Time


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH yearly_data AS (
  SELECT
    "Marketing/calendar year" AS year,
    "Commodity Type" AS commodity_type,
    Commodity,
    Attribute,
    Unit,
    AVG("Value text") AS value
  FROM ds.ag_data
  WHERE Attribute = 'Beginning stocks'
  GROUP BY year, commodity_type, Commodity, Attribute, Unit
)
SELECT *
FROM yearly_data
ORDER BY year, commodity_type, Commodity`
```


```js
function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    y: {grid: true, label: "Value"},
    x: {label: "Year"},
    color: {legend: true},
    marks: [
      Plot.areaY(data, {
        x: "year",
        y: "value",
        z: "Commodity",
        fill: "Commodity",
        stroke: "Commodity",
        title: d => `${d.Commodity}\nType: ${d.commodity_type}\nValue: ${d.value.toFixed(2)} ${d.Unit}`,
        curve: "basis"
      }),
      Plot.ruleY([0])
    ],
    facet: {
      data: data,
      y: "commodity_type",
      marginRight: 80
    },
    fy: {
      axis: "right"
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