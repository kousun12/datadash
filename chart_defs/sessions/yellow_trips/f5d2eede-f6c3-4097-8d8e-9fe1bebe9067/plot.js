function plotChart(data, {width} = {}) {
  const height = 500;
  const margin = {top: 30, right: 30, bottom: 50, left: 150};

  return Plot.plot({
    width,
    height,
    marginLeft: margin.left,
    marginRight: margin.right,
    marginTop: margin.top,
    marginBottom: margin.bottom,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ":00",
      domain: [0, 23],
      ticks: 12  // Show 12 ticks, which will be every 2 hours
    },
    y: {
      label: null,
      domain: d3.groupSort(data, g => d3.sum(g, d => d.pickup_count), d => d.Zone)
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour,
        y: d => d.Zone,
        fill: d => d.pickup_count,
        tip: true,
        title: d => `${d.Zone}\nHour: ${d.hour}:00\nPickups: ${d.pickup_count}`
      }),
      Plot.text(data, Plot.groupY({x: "count"}, {
        y: d => d.Zone,
        text: d => d.Zone,
        dx: -15,
        dy: 0,
        fontSize: 10,
        textAnchor: "end"
      }))
    ]
  });
}
