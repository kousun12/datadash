function plotChart(data, {width} = {}) {
  const margin = {top: 40, right: 40, bottom: 60, left: 120};

  return Plot.plot({
    width,
    height: 600,
    marginTop: margin.top,
    marginRight: margin.right,
    marginBottom: margin.bottom,
    marginLeft: margin.left,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ':00'
    },
    y: {
      label: null,
      axis: "left"
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: "hour",
        y: "Zone",
        fill: "pickup_count",
        title: d => `Zone: ${d.Zone}\nHour: ${d.hour.toString().padStart(2, '0')}:00\nPickups: ${d.pickup_count.toLocaleString()}`,
        tip: true
      }),
      Plot.text(data, Plot.selectLast({
        x: d => 24,
        y: "Zone",
        text: "Zone",
        dx: 6,
        fontSize: 10,
        textAnchor: "start"
      }))
    ],
    tip: true
  });
}
