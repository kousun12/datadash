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
${await FileAttachment("plot.js").text()}
```


<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotChart(data, {width}))}
    </div>
</div>

```js
display(Inputs.table(data));
```
