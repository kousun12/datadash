function plotChart(data, {width} = {}) {
  const margin = {top: 20, right: 200, bottom: 40, left: 60};

  return Plot.plot({
    width,
    height: 500,
    marginTop: margin.top,
    marginRight: margin.right,
    marginBottom: margin.bottom,
    marginLeft: margin.left,
    x: {
      label: "Hour of Day",
      domain: [0, 23],
      tickFormat: d => d.toString().padStart(2, '0') + ':00'
    },
    y: {
      label: "Pickup Count",
      grid: true
    },
    color: {
      legend: true,
      scheme: "tableau10"
    },
    marks: [
      Plot.line(data, {
        x: "hour",
        y: "pickup_count",
        stroke: "Zone",
        strokeWidth: 2,
        curve: "monotone-x"
      }),
      Plot.dot(data, {
        x: "hour",
        y: "pickup_count",
        stroke: "Zone",
        fill: "white",
        r: 3,
        title: d => `Zone: ${d.Zone}\nHour: ${d.hour.toString().padStart(2, '0')}:00\nPickups: ${d.pickup_count.toLocaleString()}`,
        stroke: "Zone",
        strokeWidth: 2,
        fill: "white"
      }),
      Plot.ruleY([0]),
      Plot.text(data, Plot.selectLast({
        x: "hour",
        y: "pickup_count",
        z: "Zone",
        text: "Zone",
        textAnchor: "start",
        dx: 5
      }))
    ],
    tip: true
  });
}
