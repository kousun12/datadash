function plotChart(data, {width} = {}) {
  const height = 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 50;
  const marginLeft = 40;

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
    },
    y: {
      label: "Price ($)",
      domain: [d3.min(data, d => d.low), d3.max(data, d => d.high)],
    },
    y2: {
      label: "Volume",
      domain: [0, d3.max(data, d => d.volume)],
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(data, {
        x: "date",
        y: "volume",
        y2: 0,
        fill: d => d.close > d.open ? "green" : "red",
        fillOpacity: 0.3,
        y2: "y2"
      }),
      Plot.ruleY(data, {
        x: "date",
        y1: "low",
        y2: "high",
        stroke: d => d.close > d.open ? "green" : "red",
      }),
      Plot.rectY(data, {
        x: "date",
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.close > d.open ? "green" : "red",
      }),
    ],
  });
}
