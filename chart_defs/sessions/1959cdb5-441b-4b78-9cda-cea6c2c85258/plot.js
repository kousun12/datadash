function plotChart(data, {width} = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  const height = 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 30;
  const marginLeft = 40;

  const volumeHeight = 100;
  const priceHeight = height - volumeHeight - marginTop - marginBottom;

  // Parse date strings to Date objects
  const parseDate = d3.utcParse("%Y-%m-%d");

  return Plot.plot({
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    y: {
      grid: true,
      label: "Price ($)"
    },
    x: {
      type: "utc",
      label: "Date"
    },
    marks: [
      Plot.ruleY([0]),
      Plot.rect(data, {
        x: d => parseDate(d.date),
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.open > d.close ? "red" : "green",
        tip: true,
        title: d => {
          const date = parseDate(d.date);
          return `Date: ${date.toLocaleDateString()}\nOpen: $${d.open.toFixed(2)}\nClose: $${d.close.toFixed(2)}\nHigh: $${d.high.toFixed(2)}\nLow: $${d.low.toFixed(2)}\nVolume: ${d.volume.toLocaleString()}`;
        }
      }),
      Plot.ruleY(data, {
        x: d => parseDate(d.date),
        y1: d => d.low,
        y2: d => d.high,
        stroke: d => d.open > d.close ? "red" : "green"
      }),
      Plot.rectY(data, {
        x: d => parseDate(d.date),
        y: d => d.volume,
        fill: "lightblue",
        fillOpacity: 0.5,
      }),
      Plot.axisX({
        label: "Date",
        tickFormat: "%b %Y"
      }),
      Plot.axisY({
        label: "Price ($)",
        tickFormat: ".0f"
      }),
      Plot.axisY({
        label: "Volume",
        tickFormat: "~s",
        ticks: 3,
        y: d => d.volume,
      })
    ],
    facet: {
      data: data,
      y: d => d.volume ? "Volume" : "Price",
      marginTop: 30
    },
    fy: {
      axis: null
    }
  });
}
