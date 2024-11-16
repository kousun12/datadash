---
title: "Stacked Crop Beginning Stocks Over Time"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Stacked Crop Beginning Stocks Over Time

This interactive stacked area chart displays the cumulative beginning stocks for various crops in million bushels across different marketing years. It allows for easy comparison of trends between commodities and shows the total stocks for all commodities combined. Hover over areas to see detailed information for each year and commodity. The x-axis labels are rotated and spaced for improved readability.


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
  return Plot.plot({
    width,
    height: 600, // Increased height to accommodate rotated labels
    marginBottom: 80, // Increased bottom margin for x-axis labels
    marginRight: 120, // Increased right margin for legend
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45,
      labelOffset: 50 // Increased offset to prevent overlap with rotated labels
    },
    y: {
      label: "Value (Million bushels)",
      grid: true
    },
    color: {
      legend: true,
      scheme: "tableau10" // Use a color scheme that works well for multiple categories
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "year",
        y: "value",
        fill: "Commodity",
        stroke: "white",
        strokeWidth: 1,
        curve: "natural"
      })),
      Plot.tip(data, Plot.pointerX({
        x: "year",
        y: "value",
        title: (d) => `${d.Commodity}\nYear: ${d.year}\nValue: ${d.value.toLocaleString()} million bushels`,
        fill: "Commodity",
        fillOpacity: 0.8
      }))
    ],
    tooltip: {
      hidden: false,
      position: "fixed"
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