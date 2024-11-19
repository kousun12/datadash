function plotChart(data, {width} = {}) {
  const height = width * 0.7;
  
  return Plot.plot({
    width,
    height,
    color: {
      type: "log",
      scheme: "YlOrRd"
    },
    x: {
      label: "Pickup Location ID",
      domain: d3.range(1, d3.max(data.getColumn('PULocationID').toArray()) + 1)
    },
    y: {
      label: "Dropoff Location ID",
      domain: d3.range(1, d3.max(data.getColumn('DOLocationID').toArray()) + 1)
    },
    marks: [
      Plot.cell(data, {
        x: "PULocationID",
        y: "DOLocationID",
        fill: "trip_count",
        tip: true
      }),
      Plot.text(data, {
        x: "PULocationID",
        y: "DOLocationID",
        text: d => d.trip_count > 1000 ? d.trip_count.toString() : "",
        fill: "white"
      })
    ]
  });
}
