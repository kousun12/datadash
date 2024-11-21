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

  const width = options.width || 640;
  const height = options.width ? options.width * 0.8 : 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 30;
  const marginLeft = 40;

  const candlestickChart = Plot.plot({
    width,
    height: height * 0.7,
    marginTop,
    marginRight,
    marginBottom: 0,
    marginLeft,
    style: {
      backgroundColor: "#f5f5f5",
    },
    x: {
      type: "band",
      label: null,
      tickFormat: d => safeFormatDate(parseDate(d)),
    },
    y: {
      grid: true,
      label: "Price ($)",
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
    ],
  });

  const volumeChart = Plot.plot({
    width,
    height: height * 0.3,
    marginTop: 0,
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
      label: "Volume",
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(data, {
        x: d => d.date,
        y: d => d.volume,
        fill: "lightblue",
        tip: true,
        title: d => `Date: ${safeFormatDate(safeParseDate(d.date))}\nVolume: ${d.volume.toLocaleString()}`,
      }),
    ],
  });

  return Plot.plot({
    width,
    height,
    style: {
      display: "flex",
      flexDirection: "column",
    },
    marks: [
      Plot.frame({fill: "transparent"}),
      candlestickChart,
      volumeChart,
    ],
  });
}
