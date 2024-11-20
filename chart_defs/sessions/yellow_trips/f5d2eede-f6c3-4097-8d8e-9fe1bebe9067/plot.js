function plotChart(data, {width} = {}) {
  const height = Math.max(500, data.numRows * 25); // Adjust height based on number of zones
  const margin = {top: 40, right: 100, bottom: 60, left: 200};

  return Plot.plot({
    width,
    height,
    marginLeft: margin.left,
    marginRight: margin.right,
    marginTop: margin.top,
    marginBottom: margin.bottom,
    x: {
      label: "Hour of Day",
      tickFormat: d => d + "h",
      domain: [0, 23],
      ticks: 24
    },
    y: {
      label: null,
      domain: data.select('Zone').distinct().toArray().sort((a, b) => {
        const sumA = data.filter(d => d.Zone === a).select('pickup_count').sum();
        const sumB = data.filter(d => d.Zone === b).select('pickup_count').sum();
        return sumB - sumA;
      })
    },
    color: {
      type: "linear",
      scheme: "Greens",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour,
        y: d => d.Zone,
        fill: d => d.pickup_count,
        tip: true,
        title: d => `${d.Zone}\nPickups: ${d.pickup_count.toLocaleString()}`
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
