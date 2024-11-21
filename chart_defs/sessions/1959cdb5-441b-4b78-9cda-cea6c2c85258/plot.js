function plotChart(data, {width} = {}) {
  // Convert Arrow table to JavaScript array
  const dataArray = data.toArray();

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
      domain: dataArray.map(d => d.date),
    },
    y: {
      label: "Price ($)",
    },
    y2: {
      label: "Volume",
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(dataArray, {
        x: "date",
        y: "volume",
        fill: d => d.close > d.open ? "green" : "red",
        fillOpacity: 0.3,
        y2: "y2"
      }),
      Plot.ruleY(dataArray, {
        x: "date",
        y1: "low",
        y2: "high",
        stroke: d => d.close > d.open ? "green" : "red",
      }),
      Plot.rectY(dataArray, {
        x: "date",
        y1: d => Math.min(d.open, d.close),
        y2: d => Math.max(d.open, d.close),
        fill: d => d.close > d.open ? "green" : "red",
      }),
    ],
  });
}
