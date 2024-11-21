function plotChart(data, {width} = {}) {
  const margin = {top: 40, right: 160, bottom: 60, left: 60};

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
      label: "Pickup Count",
      axis: "left"
    },
    color: {
      legend: true
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
        title: d => `Zone: ${d.Zone}\nHour: ${d.hour.toString().padStart(2, '0')}:00\nPickups: ${d.pickup_count.toLocaleString()}\nTotal Pickups: ${d.total_pickups.toLocaleString()}`,
      }),
      Plot.text(data, Plot.selectLast({
        x: d => 24,
        y: "pickup_count",
        text: "Zone",
        dx: 6,
        fontSize: 10,
        textAnchor: "start"
      }))
    ],
    tip: {
      format: {
        x: x => x.toString().padStart(2, '0') + ':00',
        y: y => y.toLocaleString()
      }
    },
    color: {
      legend: true,
      scheme: "tableau10"
    }
  });
}
