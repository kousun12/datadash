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
      domain: data.getColumn("date"),
    },
    y: {
      label: "Price ($)",
      domain: [0, Math.max(...data.getColumn("high"))],
    },
    y2: {
      label: "Volume",
      domain: [0, Math.max(...data.getColumn("volume"))],
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
