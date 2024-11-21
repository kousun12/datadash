function plotChart(data, {width} = {}) {
  const height = 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 50;
  const marginLeft = 40;

  // Helper function to get max value from a column
  const getMaxValue = (columnName) => {
    let max = -Infinity;
    for (let i = 0; i < data.numRows; i++) {
      const value = data.get(i)[columnName];
      if (value > max) max = value;
    }
    return max;
  };

  return Plot.plot({
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    x: {
      type: "band",
      label: "Date",
      domain: data.toArray().map(d => d.date),
    },
    y: {
      label: "Price ($)",
      domain: [0, getMaxValue("high")],
    },
    y2: {
      label: "Volume",
      domain: [0, getMaxValue("volume")],
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(data, {
        x: d => d.date,
        y: d => d.volume,
        fill: d => d.close > d.open ? "green" : "red",
        fillOpacity: 0.3,
        y2: "y2"
      }),
      Plot.ruleY(data, {
        x: d => d.date,
        y1: d => d.low,
        y2: d => d.high,
        stroke: d => d.close > d.open ? "green" : "red",
      }),
      Plot.rectY(data, {
        x: d => d.date,
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.close > d.open ? "green" : "red",
      }),
    ],
  });
}
