function plotChart(data, options = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  const width = options.width || 960;
  const parseDate = d3.utcParse("%Y-%m-%d");

  const color = d => d.close > d.open ? "#4daf4a" : "#e41a1c";

  return Plot.plot({
    width,
    inset: 6,
    grid: true,
    style: {
      backgroundColor: "#f5f5f5",
    },
    x: {
      type: "utc",
      label: "Date",
      tickFormat: d3.utcFormat("%b %Y"),
    },
    y: {
      label: "↑ MMM stock price ($)",
    },
    color,
    marks: [
      Plot.ruleX(data, {
        x: d => parseDate(d.date),
        y1: "low",
        y2: "high",
        stroke: color,
      }),
      Plot.ruleX(data, {
        x: d => parseDate(d.date),
        y1: "open",
        y2: "close",
        stroke: color,
        strokeWidth: 4,
        strokeLinecap: "round",
      }),
    ],
  });
}
