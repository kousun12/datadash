function plotChart(data, options = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  // Parse date strings to Date objects
  const parseDate = d3.utcParse("%Y-%m-%d");

  // Helper function to safely parse dates
  const safeParseDate = (dateString) => {
    if (!dateString) return null;
    return parseDate(dateString);
  };

  // Helper function to safely format dates
  const safeFormatDate = (date) => {
    if (!date) return "N/A";
    return d3.utcFormat("%b %Y")(date);
  };

  return Plot.plot({
    width: options.width || 640,
    height: options.width ? options.width * 0.6 : 400,
    y: {
      grid: true,
      label: "Price ($)"
    },
    x: {
      type: "band",
      label: "Date"
    },
    marks: [
      Plot.ruleY([0]),
      Plot.rect(data, {
        x: d => d.date,
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.open > d.close ? "red" : "green",
        tip: true,
        title: d => {
          const date = safeParseDate(d.date);
          return `Date: ${safeFormatDate(date)}\nOpen: $${d.open.toFixed(2)}\nClose: $${d.close.toFixed(2)}\nHigh: $${d.high.toFixed(2)}\nLow: $${d.low.toFixed(2)}\nVolume: ${d.volume.toLocaleString()}`;
        }
      }),
      Plot.ruleY(data, {
        x: d => d.date,
        y1: d => d.low,
        y2: d => d.high,
        stroke: d => d.open > d.close ? "red" : "green"
      }),
      Plot.rectY(data, {
        x: d => d.date,
        y: d => d.volume,
        fill: "lightblue",
        fillOpacity: 0.5,
      }),
      Plot.axisX({
        label: "Date",
        tickFormat: d => safeFormatDate(parseDate(d))
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
      y: d => d.volume ? "Volume" : "Price"
    },
    fy: {
      axis: null
    }
  });
}
