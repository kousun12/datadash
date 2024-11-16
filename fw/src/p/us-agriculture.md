---
title: "Crop Beginning Stocks Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Crop Beginning Stocks Over Time

This interactive chart aims to display the beginning stocks for various crops in million bushels across different marketing years. It should allow for easy comparison of trends between commodities. However, there is currently an issue with the stacking functionality, resulting in an 'unknown offset: zero' error. This needs to be resolved for accurate data representation. When fixed, users will be able to hover over areas to see detailed information for each year and commodity. The x-axis labels are rotated and spaced for improved readability.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    Commodity,
    "Commodity Type",
    Attribute,
    Unit,
    "Value text" AS value
  FROM ds.ag_data
  WHERE "Commodity Type" = 'Crops'
    AND Attribute = 'Beginning stocks'
    AND Unit = 'Million bushels'
)
SELECT * FROM filtered_data
ORDER BY year, Commodity`
```


```js
function plotChart(data, {width} = {}) {
  // Convert value to number
  data = data.map(d => ({...d, value: +d.value}));

  return Plot.plot({
    width,
    height: 600,
    marginBottom: 80,
    marginRight: 120,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45,
      labelOffset: 50
    },
    y: {
      label: "Value (Million bushels)",
      grid: true
    },
    color: {
      legend: true,
      scheme: "tableau10"
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "year",
        y: "value",
        z: "Commodity",
        fill: "Commodity",
        stroke: "white",
        strokeWidth: 1,
        curve: "natural"
      })),
      Plot.ruleY([0]),
      Plot.tip(data, Plot.pointerX({
        x: "year",
        y: "value",
        z: "Commodity",
        title: (d) => `${d.Commodity}\nYear: ${d.year}\nValue: ${d.value.toLocaleString()} million bushels`,
        fill: "Commodity",
        fillOpacity: 0.8
      }))
    ],
    tooltip: {
      hidden: false
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