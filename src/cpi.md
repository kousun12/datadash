---
theme: dashboard
title: CPI Over time
toc: false
---

# CPI Over time


```js
const db = DuckDBClient.of({base: FileAttachment("./data/cpi.parquet")});
```

```js
const data = db.sql`SELECT * FROM base`;
```


```js
function plotTimeline(data, {width} = {}) {
  console.log("DATA", data);
  return Plot.plot({
    title: "CPI over the years",
    width,
    height: 300,
    y: {label: "CPI (1982-1984=100)", grid: true},
    x: {label: "Date", grid: true, tickFormat: d3.timeFormat("%m-%Y")},
    color: {legend: true},
    marks: [
      Plot.line(data, { x: r => r.DATE, y: r => r.CPIAUCSL}) 
    ]
  });
}
display(Inputs.table(data));
display(plotTimeline(data));
```


```text
<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotTimeline(data, {width}))}
    </div>
</div>
```
