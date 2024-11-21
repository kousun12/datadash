function plotChart(data, options = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  const width = options.width || 640;
  const height = options.width ? options.width * 0.8 : 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 30;
  const marginLeft = 40;

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
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    style: {
      backgroundColor: "#f5f5f5",
    },
    x: {
      type: "band",
      label: "Date",
      tickFormat: d => safeFormatDate(parseDate(d)),
    },
    y: {
      grid: true,
      label: "Price ($)",
      domain: [0, d3.max(data, d => d.high)],
    },
    y2: {
      label: "Volume",
      domain: [0, d3.max(data, d => d.volume)],
    },
    marks: [
      Plot.ruleY([0]),
      Plot.rect(data, {
        x: d => d.date,
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.close > d.open ? "green" : "red",
        tip: true,
        title: d => `Date: ${safeFormatDate(safeParseDate(d.date))}\nOpen: $${d.open.toFixed(2)}\nClose: $${d.close.toFixed(2)}\nHigh: $${d.high.toFixed(2)}\nLow: $${d.low.toFixed(2)}\nVolume: ${d.volume.toLocaleString()}`,
      }),
      Plot.ruleY(data, {
        x: d => d.date,
        y1: d => d.low,
        y2: d => d.high,
        stroke: d => d.close > d.open ? "green" : "red",
      }),
      Plot.barY(data, {
        x: d => d.date,
        y: d => d.volume,
        y2: 0,
        fill: "lightblue",
        opacity: 0.5,
      }),
    ],
  });
}
