function plotChart(data, {width} = {}) {
  const margin = {bottom: 60, left: 200, right: 120};

  return Plot.plot({
    width,
    marginLeft: margin.left,
    marginBottom: margin.bottom,
    marginRight: margin.right,
    x: {
      label: "Hour of Day",
    },
    y: {
      label: null,
      domain: d3.groupSort(data, g => d3.sum(g, d => d.pickup_count), d => d.Zone)
    },
    color: {
      type: "linear",
      scheme: "Blues",
      label: "Pickup Count"
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour,
        y: d => d.Zone,
        fill: d => d.pickup_count,
        tip: true,
        title: d => `${d.Zone}\nHour: ${d.hour}:00\nPickups: ${d.pickup_count.toLocaleString()}`
      }),
      Plot.text(data, Plot.groupY({x: "count"}, {
        y: d => d.Zone,
        text: d => d.Zone,
        dx: -10,
        dy: 0,
        fontSize: 9,
        textAnchor: "end"
      }))
    ]
  });
}
