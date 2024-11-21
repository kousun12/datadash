function plotChart(data, {width} = {}) {
  const height = width * 0.6;
  const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.pickup_count)]);

  return Plot.plot({
    width,
    height,
    style: {
      fontFamily: "sans-serif",
      background: "#f0f0f0"
    },
    color: {
      type: "sequential",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.PULocationID % 10,
        y: d => Math.floor(d.PULocationID / 10),
        fill: d => d.pickup_count,
        title: d => `Zone: ${d.zone_name}\nLocation ID: ${d.PULocationID}\nPickups: ${d.pickup_count.toLocaleString()}`,
      })
    ],
    x: {
      label: "Location ID (mod 10)",
      nice: true
    },
    y: {
      label: "Location ID (div 10)",
      nice: true
    },
    marginTop: 40,
    marginRight: 40,
    marginBottom: 40,
    marginLeft: 40,
    caption: "Heatmap of Taxi Pickups by Zone"
  });
}
