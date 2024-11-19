function plotChart(data, {width} = {}) {
  const height = width * 0.7;
  
  // Get the maximum values for PULocationID and DOLocationID
  const maxPULocationID = d3.max(data, d => d.PULocationID);
  const maxDOLocationID = d3.max(data, d => d.DOLocationID);
  
  return Plot.plot({
    width,
    height,
    color: {
      type: "log",
      scheme: "YlOrRd"
    },
    x: {
      label: "Pickup Location ID",
      domain: d3.range(1, maxPULocationID + 1)
    },
    y: {
      label: "Dropoff Location ID",
      domain: d3.range(1, maxDOLocationID + 1)
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
