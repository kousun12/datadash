---
title: "Simplified Agricultural Commodity Beginning Stocks Trends (1990-Present)"
toc: false
sidebar: false
header: false
footer: false
pager: false

---

# Simplified Agricultural Commodity Beginning Stocks Trends (1990-Present)

This basic chart displays the beginning stocks for agricultural commodities from 1990 onwards. It focuses on simplicity and robustness, providing a clear visualization of the data while handling potential inconsistencies.


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
// Simplified utility function to access data
function safeGetColumn(data, columnName) {
  if (Array.isArray(data)) {
    return data.map(row => row[columnName] ?? null);
  }
  return [];
}

function normalizeData(data) {
  const requiredColumns = ['year', 'value', 'commodity_type', 'unit'];
  const normalizedData = requiredColumns.reduce((acc, col) => {
    acc[col] = safeGetColumn(data, col);
    return acc;
  }, {});

  return normalizedData.year.map((year, i) => ({
    year,
    value: parseFloat(normalizedData.value[i]),
    commodity_type: normalizedData.commodity_type[i],
    unit: normalizedData.unit[i]
  }));
}

function validateDataPoint(d) {
  return !isNaN(d.value) && d.year && d.commodity_type && d.unit;
}

function plotChart(data, {width} = {}) {
  // Basic data validation
  if (!Array.isArray(data) || data.length === 0) {
    return displayError("No data available to display.");
  }

  // Normalize and validate data
  const normalizedData = normalizeData(data);
  const validData = normalizedData.filter(validateDataPoint);

  if (validData.length === 0) {
    return displayError("No valid data points after filtering. Please check your data source.");
  }

  // Log filtering results for debugging
  console.log(`Total data points: ${normalizedData.length}, Valid data points: ${validData.length}`);

  // Create a simple plot
  const plot = Plot.plot({
    width,
    height: 400,
    marginRight: 80,
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
        stroke: "commodity_type",
        strokeWidth: 2
      }),
      Plot.dot(validData, {
        x: "year",
        y: "value",
        fill: "commodity_type",
        title: d => `${d.commodity_type}\nYear: ${d.year}\nValue: ${d.value} ${d.unit}`
      })
    ]
  });

  return plot;
}

function displayError(message) {
  console.error(message); // Log error for debugging
  return html`
    <div style="color: red; text-align: center; padding: 20px; border: 1px solid red; border-radius: 5px;">
      <h3>Error</h3>
      <p>${message}</p>
      <p>Please check the data source and try again.</p>
    </div>
  `;
}

// Documentation
/**
 * plotChart - Creates a simple time series chart for agricultural commodity data
 * @param {Array} data - The input data as a standard JavaScript array
 * @param {Object} options - Chart options
 * @param {number} options.width - The width of the chart
 * @returns {Object} - A Plot object representing the chart or an error message
 * 
 * Expected data format:
 * - Each object should have properties 'year', 'value', 'commodity_type', and 'unit'
 * 
 * Example usage:
 * const chart = plotChart(data, {width: 800});
 * document.body.appendChild(chart);
 */

// Export functions for potential unit testing
if (typeof module !== 'undefined') {
  module.exports = {
    safeGetColumn,
    normalizeData,
    validateDataPoint,
    plotChart,
    displayError
  };
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