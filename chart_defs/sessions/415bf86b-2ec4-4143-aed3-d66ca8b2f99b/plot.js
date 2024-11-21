function plotChart(data, {width} = {}) {
  const height = 500;
  const marginTop = 30;
  const marginRight = 30;
  const marginBottom = 40;
  const marginLeft = 60;

  // Convert Arrow table to array
  const dataArray = data.toArray();

  return Plot.plot({
    width,
    height,
    marginTop,
    marginRight,
    marginBottom,
    marginLeft,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ":00",
      domain: d3.range(24)
    },
    y: {
      label: "Pickup Location ID",
      domain: d3.groupSort(dataArray, g => -d3.sum(g, d => d.trip_count), d => d.PULocationID)
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Number of Trips"
    },
    marks: [
      Plot.cell(dataArray, {
        x: d => d.hour,
        y: d => d.PULocationID,
        fill: d => d.trip_count,
        tip: true,
        title: d => `Location: ${d.PULocationID}\nHour: ${d.hour}:00\nTrips: ${d.trip_count}`
      })
    ]
  });
}