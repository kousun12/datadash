function plotChart(data, {width} = {}) {
  const height = width * 0.7;
  
  // Get unique location IDs
  const locationIDs = new Set([...data.map(d => d.PULocationID), ...data.map(d => d.DOLocationID)]);
  const sortedLocationIDs = Array.from(locationIDs).sort((a, b) => a - b);
  
  return Plot.plot({
    width,
    height,
    marginLeft: 60,
    marginBottom: 60,
    color: {
      type: "log",
      scheme: "YlOrRd",
      label: "Trip Count"
    },
    x: {
      label: "Pickup Location ID",
      tickFormat: d => d,
      domain: sortedLocationIDs,
      padding: 0.1
    },
    y: {
      label: "Dropoff Location ID",
      tickFormat: d => d,
      domain: sortedLocationIDs,
      padding: 0.1
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
        text: d => d.trip_count.toString(),
        fill: "white",
        fontSize: 8
      })
    ]
  });
}
