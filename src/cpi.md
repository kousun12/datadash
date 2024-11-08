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
  return Plot.plot({
    title: "Consumer Price Index (CPI) Historical Trend",
    width,
    y: {
      label: "CPI (1982-1984 = 100)",
      grid: true,
      tickFormat: d => d.toLocaleString()
    },
    x: {
      label: "Date →",
      grid: true,
      tickFormat: d3.timeFormat("%Y"),
      tickRotate: 45
    },
    
    marks: [
      Plot.gridY({ stroke: "#333", strokeOpacity: 0.5 }),
      Plot.gridX({ stroke: "#333", strokeOpacity: 0.5 }),
      Plot.areaY(data, {
        x: d => new Date(d.DATE),
        y: "CPIAUCSL",
        fill: "#00ff0020",
        stroke: "none",
      }),
      
      Plot.line(data, {
        x: d => new Date(d.DATE),
        y: "CPIAUCSL",
        stroke: "#00ff00",
        strokeWidth: 2
      }),
      
      // January dots using arrow data
      Plot.dot(data, {
        x: d => new Date(d.DATE),
        y: "CPIAUCSL",
        stroke: "#00ff00",
        fill: "#1a1a1a",
        strokeWidth: 1,
        r: 2,
        filter: d => new Date(d.DATE).getMonth() === 0,
        tip: true,
        title: d => `${d3.timeFormat("%B %Y")(new Date(d.DATE))}\nCPI: ${d.CPIAUCSL.toFixed(1)}`
      }),
      // mark the baseline years:
      Plot.rectY(data, { 
        x: new Date("1982-01-01"), x2: new Date("1984-01-01"), 
        fill: "#88888802", y: 0, y2: d3.max(data, d => d.CPIAUCSL) 
      }),
      Plot.ruleY([100], {stroke: "#888888", strokeDasharray: "5,5"}),
    ],
    
    caption: "Source: Federal Reserve Economic Data (FRED)"
  });
}// display(plotTimeline(data));
```


<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotTimeline(data, {width}))}
    </div>
</div>
