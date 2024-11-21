function plotChart(data, {width} = {}) {
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  const height = 400;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 30;
  const marginLeft = 40;

  return Plot.plot({
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    x: {
      type: "time",
      label: "Date",
    },
    y: {
      label: "Close Price ($)",
    },
    marks: [
      Plot.dot(data, {
        x: d => d.date,
        y: d => d.close,
      })
    ]
  });
}
