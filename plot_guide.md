Here's a comprehensive guide to Observable Plot:

## Basic Setup

Include Plot in your HTML page:
```html
<script src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6"></script>
```

Access Plot via the global `Plot` object:
```javascript
const chart = Plot.plot({
  marks: [
    Plot.dot(data, {x: "field1", y: "field2"})
  ]
});
document.body.appendChild(chart);
```

## Core Concepts

**Plot Structure**
- Every plot consists of marks (geometric shapes) layered on a canvas
- Plots are created using `Plot.plot()` with configuration options
- Data can be arrays of objects, arrays of arrays, or Map/Set objects[1]

**Basic Configuration Options**
```javascript
Plot.plot({
  marks: [],      // Array of mark layers
  width: 640,     // Width in pixels
  height: 400,    // Height in pixels
  margin: 40,     // Margin around plot
  grid: true,     // Show grid lines
  nice: true,     // Nice round axis values
  zero: true,     // Include zero in scale
  color: {},      // Color scheme options
  x: {},          // X-axis options
  y: {}           // Y-axis options
})
```

## Mark Types

**Basic Marks**
```javascript
// Points/Scatter
Plot.dot(data, {x: "field1", y: "field2", r: 5})

// Lines
Plot.line(data, {x: "field1", y: "field2"})

// Bars
Plot.barY(data, {x: "category", y: "value"})
Plot.barX(data, {y: "category", x: "value"})

// Area
Plot.area(data, {x: "field1", y: "field2"})

// Text
Plot.text(data, {x: "field1", y: "field2", text: "label"})
```

**Advanced Marks**
```javascript
// Heat maps
Plot.cell(data, {x: "field1", y: "field2", fill: "value"})

// Density
Plot.density(data, {x: "field1", y: "field2"})

// Box plots
Plot.boxY(data, {x: "category", y: "value"})

// Violin plots
Plot.violinY(data, {x: "category", y: "value"})
```

## Scales and Transforms

**Scale Types**
```javascript
{
  x: {
    type: "linear",    // Numeric scale
    domain: [0, 100],  // Input range
    range: [0, width]  // Output range
  },
  color: {
    type: "categorical",
    scheme: "spectral" // Color scheme name
  }
}
```

**Data Transforms**
```javascript
// Binning
Plot.rectY(data, {
  x: "value",
  y: "count",
  interval: "month",  // For dates
  bin: true           // For numbers
})

// Grouping
Plot.groupY({
  x: "mean",         // Aggregate function
  y: "category",
  stroke: "group"    // Group by field
})
```

## Styling and Customization

**Mark Properties**
```javascript
{
  stroke: "color",      // Line/border color
  fill: "color",        // Fill color
  opacity: 0.5,         // Opacity
  strokeWidth: 2,       // Line width
  r: 5,                 // Point radius
  curve: "natural",     // Line interpolation
  title: "tooltip"      // Tooltip text
}
```

**Axes and Labels**
```javascript
{
  x: {
    label: "X Axis",    // Axis label
    tickFormat: ",.0f", // Number format
    ticks: 5,          // Number of ticks
    grid: true         // Show gridlines
  },
  color: {
    legend: true       // Show color legend
  }
}
```

## Faceting and Composition

**Multiple Views**
```javascript
Plot.plot({
  grid: true,
  marks: [
    Plot.frame(),
    Plot.dot(data, {...}),
    Plot.line(data, {...})
  ]
})
```

**Faceting**
```javascript
Plot.plot({
  facet: {
    data: dataset,
    x: "category",    // Facet by column
    y: "group"        // Facet by row
  },
  marks: [
    Plot.dot(data, {...})
  ]
})
```

## Event Handling

```javascript
const chart = Plot.plot({...});

// Click events
chart.addEventListener("click", (event) => {
  const {value, index} = event.detail;
  console.log("Clicked:", value);
});

// Hover events
chart.addEventListener("pointermove", (event) => {
  const {value, index} = event.detail;
  console.log("Hover:", value);
});
```

## Common Patterns

**Responsive Charts**
```javascript
function resize() {
  const container = document.querySelector("#chart");
  const chart = Plot.plot({
    width: container.clientWidth,
    height: container.clientHeight,
    marks: [...]
  });
  container.replaceChildren(chart);
}

window.addEventListener("resize", resize);
```

**Dynamic Updates**
```javascript
function updateChart(newData) {
  const chart = Plot.plot({
    marks: [
      Plot.dot(newData, {...})
    ]
  });
  document.querySelector("#chart").replaceChildren(chart);
}
```

## Transforms

**Data Transforms**
```javascript
// Binning data
Plot.rectY(data, {
  x: "value",
  y: "count",
  interval: "month",
  bin: true
}).plot()

// Grouping data
Plot.groupY(data, {
  x: "mean",
  y: "category",
  fill: "group"
}).plot()

// Stacking
Plot.stackY(data, {
  x: "date",
  y: "value",
  fill: "category"
}).plot()
```

## Facets

**Creating Multi-panel Plots**
```javascript
Plot.plot({
  facet: {
    data: dataset,
    x: "category",    // Horizontal faceting
    y: "group",       // Vertical faceting
    marginRight: 80   // Spacing between facets
  },
  marks: [
    Plot.dot(data, {
      x: "value1",
      y: "value2",
      fx: "category", // Facet x coordinate
      fy: "group"     // Facet y coordinate
    })
  ]
})
```

## Intervals

**Time Intervals**
```javascript
Plot.plot({
  x: {
    interval: "day",      // day, week, month, year
    round: true,         // Round to interval boundaries
    label: "Date"
  },
  marks: [
    Plot.barY(data, {
      x: "date",
      y: "value",
      interval: "month"
    })
  ]
})
```

## Formats

**Number and Date Formatting**
```javascript
Plot.plot({
  x: {
    tickFormat: ".0f",    // Fixed-point notation
    label: "Value"
  },
  y: {
    tickFormat: "$.2f",   // Currency format
    label: "Price"
  },
  color: {
    tickFormat: ".0%"     // Percentage format
  },
  marks: [/* ... */]
})
```

**Common Format Strings**
```javascript
{
  ".0f"     // Integer
  ".2f"     // 2 decimal places
  "$.2f"    // Currency with 2 decimals
  ".0%"     // Percentage
  ",d"      // Thousands separator
  "s"       // SI prefix
}
```

## Markers

**Adding Reference Lines and Annotations**
```javascript
Plot.plot({
  marks: [
    // Base visualization
    Plot.line(data, {x: "date", y: "value"}),
    
    // Reference line
    Plot.ruleY([0]),
    
    // Annotation
    Plot.text([{
      x: date,
      y: value,
      text: "Important event",
      dy: -10
    }]),
    
    // Frame
    Plot.frame()
  ]
})
```

**Marker Types**
```javascript
// Horizontal rule
Plot.ruleX([value])

// Vertical rule
Plot.ruleY([value])

// Rectangle
Plot.rect(data, {
  x1: "start",
  x2: "end",
  y1: "bottom",
  y2: "top"
})

// Arrow
Plot.arrow(data, {
  x1: "start",
  y1: "start",
  x2: "end",
  y2: "end"
})
```

## Interactions

**Adding Tooltips**
```javascript
Plot.plot({
  marks: [
    Plot.dot(data, {
      x: "value1",
      y: "value2",
      title: (d) => `${d.label}: ${d.value}`,
      tip: true
    })
  ]
})
```

**Crosshair**
```javascript
Plot.plot({
  marks: [
    Plot.dot(data, {x: "x", y: "y"}),
    Plot.crosshair(data, {x: "x", y: "y"})
  ]
})
```

NB: `data` is an Apache Arrow object, not a standard JavaScript array:
No direct indexing (e.g., data[0] doesn't work)
Use Arrow-specific methods for data access (e.g., getColumn(), get())
Columnar structure: optimized for column-wise operations
May support lazy evaluation
Can't use standard array methods (map, filter, etc.) directly
Potentially more memory-efficient for large datasets
May require conversion (toArray()) for some operations, but at a performance cost
Consider Arrow-specific or SQL operations for best performance