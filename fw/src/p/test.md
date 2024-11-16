---
title: "Agricultural Commodity Beginning Stocks Trends (1990-Present)"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Agricultural Commodity Beginning Stocks Trends (1990-Present)

This interactive chart displays the beginning stocks for various agricultural commodities from 1990 onwards, allowing comparison between crops and livestock/dairy products across different units of measurement. The visualization includes robust error handling to manage potential data inconsistencies, including scenarios with no valid data points after filtering, and provides a reliable user experience, supporting both Apache Arrow Tables and standard JavaScript arrays.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/us_ag.db")});
```

```js
const data = db.sql`
WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    "Commodity Type" AS commodity_type,
    Commodity,
    Attribute,
    Unit,
    "Value text" AS value
  FROM ds.ag_data
  WHERE Attribute = 'Beginning stocks'
    AND "Marketing/calendar year" >= '1990/91'
)
SELECT *
FROM filtered_data
ORDER BY year, commodity_type, Commodity`
```


```js
// Utility function to safely access data
function safeGetColumn(data, columnName) {
  if (data.getColumn && typeof data.getColumn === 'function') {
    return data.getColumn(columnName)?.toArray() ?? [];
  } else if (Array.isArray(data)) {
    return data.map(row => row[columnName] ?? null);
  }
  return [];
}

function normalizeData(data) {
  const requiredColumns = ['year', 'value', 'commodity', 'commodity_type', 'unit'];
  const normalizedData = requiredColumns.reduce((acc, col) => {
    acc[col] = safeGetColumn(data, col);
    return acc;
  }, {});

  return normalizedData.year.map((year, i) => ({
    year,
    value: parseFloat(normalizedData.value[i]),
    commodity: normalizedData.commodity[i],
    commodity_type: normalizedData.commodity_type[i],
    unit: normalizedData.unit[i]
  }));
}

function validateDataPoint(d) {
  return !isNaN(d.value) && d.year && d.commodity && d.commodity_type && d.unit;
}

function plotChart(data, {width} = {}) {
  // Data validation
  if (!data || (Array.isArray(data) && data.length === 0)) {
    return displayError("No data available to display.");
  }

  // Normalize and validate data
  const normalizedData = normalizeData(data);
  const validData = normalizedData.filter(validateDataPoint);

  if (validData.length === 0) {
    return displayError("No valid data points after filtering. Please check your data source and filtering criteria.");
  }

  // Log filtering results for debugging
  console.log(`Total data points: ${normalizedData.length}, Valid data points: ${validData.length}`);

  // Create the plot with progressive enhancement
  const plot = Plot.plot({
    width,
    height: 500,
    marginRight: 120,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
    },
    y: {
      label: "Value",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(validData, {
        x: "year",
        y: "value",
        stroke: "commodity",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(validData, {
        x: "year",
        y: "value",
        stroke: "commodity",
        fill: "commodity_type"
      })
    ],
    facet: {
      data: validData,
      y: "unit"
    },
    fy: {
      label: "Unit"
    }
  });

  // Add advanced features if data quality permits
  if (validData.length > 1) {
    plot.marks.push(
      Plot.text(validData, Plot.selectLast({
        x: "year",
        y: "value",
        text: d => d.commodity,
        dx: 3,
        dy: -3,
        anchor: "start",
        fontSize: 10
      })),
      Plot.tip(validData, Plot.pointerX({
        x: "year",
        y: "value",
        title: d => `${d.commodity} (${d.commodity_type})\nYear: ${d.year}\nValue: ${d.value} ${d.unit}`
      }))
    );
  } else {
    // Add a single point annotation for minimal data
    plot.marks.push(
      Plot.text(validData, {
        x: "year",
        y: "value",
        text: d => `${d.commodity}: ${d.value} ${d.unit}`,
        dy: -10,
        fontSize: 12
      })
    );
  }

  return plot;
}

// Debugging function
function debugData(data) {
  console.log("Data sample:", data.slice(0, 5));
  console.log("Data columns:", Object.keys(data[0]));
  console.log("Data types:", Object.fromEntries(
    Object.entries(data[0]).map(([key, value]) => [key, typeof value])
  ));
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

```js
display(Inputs.table(data));
```