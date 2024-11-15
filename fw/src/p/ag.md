---
title: Agriculture
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# CPI Over time


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
// data is an arrow object
const data = db.sql`
WITH ranked_commodities AS (
  SELECT Commodity, COUNT(*) as count
  FROM ds.ag_data
  WHERE "Commodity Type" = 'Crops'
    AND Attribute = 'Beginning stocks'
  GROUP BY Commodity
  ORDER BY count DESC
  LIMIT 5
)
SELECT ad."Marketing/calendar year" as year, ad.Commodity, ad."Value text" as value
FROM ds.ag_data ad
JOIN ranked_commodities rc ON ad.Commodity = rc.Commodity
WHERE ad."Commodity Type" = 'Crops'
  AND ad.Attribute = 'Beginning stocks'
ORDER BY ad."Marketing/calendar year", ad.Commodity`;
```


```js
display(Inputs.table(data));
```

```js
function plot(data, {width} = {}) {
  const yearColumn = data.getChild('year');
  const lastYear = yearColumn.get(yearColumn.length - 1);
  return Plot.plot({
  width,
  x: { label: "Year", tickFormat: d => d.slice(0, 4) },
  y: { label: "Beginning stocks (Million bushels)", grid: true },
  color: { legend: true },
  marks: [
    Plot.line(data, {
      x: "year",
      y: "value",
      stroke: "Commodity",
      strokeWidth: 2
    }),
    Plot.dot(data, {
      x: "year",
      y: "value",
      stroke: "Commodity",
    }),
    Plot.text(data, {
      x: "year",
      y: "value",
      text: "Commodity",
      dx: 4,
      dy: -10,
      filter: (d) => d.year === lastYear
    })
  ],
  title: "Beginning Stocks for Top 5 Crops (1998-2023)"
  });
}
```


<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plot(data, {width}))}
    </div>
</div>
