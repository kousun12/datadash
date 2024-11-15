---
title: US Agricultural Commodity Trends: Top 5 Crops and Livestock/Dairy
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# US Agricultural Commodity Trends: Top 5 Crops and Livestock/Dairy


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH ranked_commodities AS (
  SELECT 
    Commodity,
    "Commodity Type",
    SUM("Value text") as total_value,
    ROW_NUMBER() OVER (PARTITION BY "Commodity Type" ORDER BY SUM("Value text") DESC) as rank
  FROM ds.ag_data
  WHERE Attribute = 'Beginning stocks'
  GROUP BY Commodity, "Commodity Type"
),
top_commodities AS (
  SELECT Commodity, "Commodity Type"
  FROM ranked_commodities
  WHERE rank <= 5
)
SELECT 
  ad."Marketing/calendar year" as year,
  ad.Commodity,
  ad."Commodity Type",
  ad."Value text" as value
FROM ds.ag_data ad
JOIN top_commodities tc ON ad.Commodity = tc.Commodity AND ad."Commodity Type" = tc."Commodity Type"
WHERE ad.Attribute = 'Beginning stocks'
ORDER BY ad."Marketing/calendar year", ad."Commodity Type", ad.Commodity`
```


```js
function plotChart(data, {width} = {}) {
  const commodityTypes = ["Crops", "Livestock/Dairy"];
  
  return Plot.plot({
    width,
    height: 600,
    grid: true,
    x: {
      label: "Year",
      tickFormat: d => d.slice(0, 4)
    },
    y: {
      label: "Value",
      tickFormat: "~s"
    },
    color: {
      legend: true
    },
    facet: {
      data: commodityTypes,
      y: d => d,
      marginRight: 80
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "year",
        y: "value",
        z: "Commodity",
        fill: "Commodity",
        stroke: "Commodity",
        title: d => `${d.Commodity}: ${d.value.toLocaleString()}`,
        curve: "basis",
        fy: "Commodity Type"
      })),
      Plot.ruleY([0])
    ]
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

