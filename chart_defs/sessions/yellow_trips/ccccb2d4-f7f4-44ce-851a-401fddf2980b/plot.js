function plotChart(data, {width} = {}) {
  const height = width * 0.6;
  const margin = {top: 20, right: 30, bottom: 40, left: 40};

  // Get unique hours for the slider
  const hours = Array.from(new Set(data.getChild('pickup_hour').toArray().map(d => d.getHours()))).sort((a, b) => a - b);

  // Create a color scale
  const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data.getChild('pickup_count').toArray())]);

  // Create the plot
  return Plot.plot({
    width,
    height,
    margin,
    style: {
      fontFamily: "sans-serif",
      background: "#f0f0f0"
    },
    x: {
      label: "PULocationID",
      nice: true
    },
    y: {
      label: "Pickup Count",
      nice: true
    },
    color: {
      type: "sequential",
      scheme: "YlOrRd",
      label: "Pickup Count",
      legend: true
    },
    marks: [
      Plot.dot(data, {
        x: "PULocationID",
        y: "pickup_count",
        r: d => Math.sqrt(d.pickup_count) / 2,
        fill: d => colorScale(d.pickup_count),
        title: d => `Location ID: ${d.PULocationID}\nPickups: ${d.pickup_count}`,
        opacity: 0.7
      })
    ],
    facet: {
      data: data,
      x: d => d.pickup_hour.getHours(),
      label: "Hour of Day"
    },
    fx: {
      domain: hours,
      label: "Hour"
    }
  });
}