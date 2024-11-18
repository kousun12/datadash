---
title: "Agricultural Commodity Trends: Top 5 Products (2010-Present)"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Trends: Top 5 Products (2010-Present)

This stacked area chart displays trends for the top 5 agricultural commodities, showing beginning stocks, production, and imports from 2010 onwards. The chart is faceted by commodity type and individual commodities, allowing for easy comparison of trends across different products and categories.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH ranked_commodities AS (
  SELECT Commodity, COUNT(*) as count,
         ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) as rank
  FROM ds.ag_data
  GROUP BY Commodity
),
top_commodities AS (
  SELECT Commodity
  FROM ranked_commodities
  WHERE rank <= 5
)
SELECT ad."Commodity Type", ad.Commodity, ad.Attribute, ad."Marketing/calendar year" as Year, ad."Value text" as Value
FROM ds.ag_data ad
JOIN top_commodities tc ON ad.Commodity = tc.Commodity
WHERE ad.Attribute IN ('Beginning stocks', 'Production', 'Imports')
  AND ad."Marketing/calendar year" >= '2010/11'
ORDER BY ad."Commodity Type", ad.Commodity, ad."Marketing/calendar year", ad.Attribute`
```


```js
function plotChart(data, {width} = {}) {
  const height = 800;
  const margin = {top: 40, right: 120, bottom: 40, left: 60};

  return Plot.plot({
    width,
    height,
    margin,
    x: {
      label: "Year",
      tickFormat: d => d.slice(0, 4)
    },
    y: {
      label: "Value",
      grid: true,
      transform: d => d / 1e6,
      tickFormat: d => d.toFixed(0) + "M"
    },
    color: {
      legend: true,
      scheme: "category10"
    },
    facet: {
      data,
      x: "Commodity Type",
      y: "Commodity",
      marginRight: 120
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "Year",
        y: d => +d.Value,
        fill: "Attribute",
        title: d => `${d.Commodity}\n${d.Attribute}\nYear: ${d.Year}\nValue: ${(+d.Value).toLocaleString()}`
      })),
      Plot.ruleY([0])
    ],
    style: {
      fontSize: "12px"
    }
  });
}


function displayError(message) {
    return html`<div style="color: red; text-align: center; padding: 20px;">Error: ${message}</div>`;
}

function plotOrError(data, options) {
    try {
        return plotChart(data, options);
    } catch (e) {
        return displayError(e.message);
    }
}
```


<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotOrError(data, {width}))}
    </div>
</div>

### Data

```js
display(Inputs.table(data));
```