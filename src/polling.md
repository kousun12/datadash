---
theme: dashboard
title: Polling 2024
toc: false
---


```js
// First, properly parse the dates and numbers
const polling_data = await FileAttachment("./data/polling.csv")
  .csv()
  .then(data => data.map(d => ({
    modeldate: d3.timeParse("%m/%d/%y")(d.modeldate), // Properly parse MM/DD/YY format
    trump: d.trump ? +d.trump : null,
    harris: d.harris ? +d.harris : null,
    trump_poll: d.trump_poll ? +d.trump_poll : null,
    harris_poll: d.harris_poll ? +d.harris_poll : null,
    rfk: d.rfk ? +d.rfk : null,
    rfk_poll: d.rfk_poll ? +d.rfk_poll : null
  })));

// Create the main polling trend visualization
const pollTrends = Plot.plot({
  style: { backgroundColor: "#1a1a1a", color: "white", fontSize: 12 },
  color: { legend: true },
  height: 600,
  width: 960,
  margin: 50,
  
  marks: [
    Plot.gridY({ stroke: "#333", strokeOpacity: 0.5 }),
    Plot.gridX({ stroke: "#333", strokeOpacity: 0.5 }),
    
    // Add area for uncertainty/spread
    Plot.areaY(polling_data.filter(d => d.trump), {
      x: "modeldate",
      y1: d => d.trump - 2,
      y2: d => d.trump + 2,
      fill: "#ff000020",
      stroke: "none"
    }),
    Plot.areaY(polling_data.filter(d => d.harris), {
      x: "modeldate",
      y1: d => d.harris - 2,
      y2: d => d.harris + 2,
      fill: "#0000ff20",
      stroke: "none"
    }),
    // Add points for actual polls
    // Trump polls
    Plot.dot(polling_data.filter(d => d.trump_poll), {
      x: "modeldate",
      y: "trump_poll",
      stroke: "red",
      fill: "#1a1a1a",  // Match background color
      strokeWidth: 2,
      r: 4,  // Slightly larger radius
      opacity: 0.2,
      tip: true,
      title: d => `Trump: ${d.trump_poll}%\n${d3.timeFormat("%B %d")(d.modeldate)}`
    }),

    // Harris polls
    Plot.dot(polling_data.filter(d => d.harris_poll), {
      x: "modeldate",
      y: "harris_poll",
      stroke: "blue",
      fill: "#1a1a1a",  // Match background color
      strokeWidth: 2,
      r: 4,  // Slightly larger radius
      opacity: 0.2,
      tip: true,
      title: d => `Harris: ${d.harris_poll}%\n${d3.timeFormat("%B %d")(d.modeldate)}`
    }),

    // Add main trend lines
    Plot.line(polling_data.filter(d => d.trump), {
      x: "modeldate",
      y: "trump",
      stroke: "red",
      strokeWidth: 2
    }),
    Plot.line(polling_data.filter(d => d.harris), {
      x: "modeldate",
      y: "harris",
      stroke: "blue",
      strokeWidth: 2
    }),

    Plot.areaY(polling_data.filter(d => !isNaN(d.rfk) && Number(d.rfk) > 0), {
      x: "modeldate",
      y1: d => Number(d.rfk) - 1,
      y2: d => Number(d.rfk) + 1,
      fill: "#ffff0020",
      stroke: "none"
    }),
    Plot.line(polling_data.filter(d => !isNaN(d.rfk)), {
      x: "modeldate",
      y: "rfk",
      stroke: "#ffff00",
      strokeWidth: 2
    }),
    // Vertical line for debate
    Plot.ruleX([new Date("2024-09-30")], {
      stroke: "white",
      strokeWidth: 1,
      strokeDasharray: "5,9",
      opacity: 0.5
    }),
    Plot.textX([new Date("2024-09-30")], {
      y: 4,
      text: ["Harris-Trump Debate"],
      fill: "white",
      stroke: "none",
      dx: 5
    })

  ],
  x: {
    label: "Date →",
    tickFormat: d3.timeFormat("%b %d"),
    ticks: "weeks",
    tickRotate: 45,
    grid: true
  },
  y: {
    label: "↑ Support (%)",
    domain: [4, 55],
    grid: true
  },
  
  title: "2024 Presidential Election Polling",
  subtitle: "Trump vs Harris National Polling Trends",
  caption: "Lines show polling averages with ±2% uncertainty bands. Points show individual polls."
});

// Display the chart
display(pollTrends);
```


##### Raw Data

```js
display(Inputs.table(polling_data));
```

```text
```