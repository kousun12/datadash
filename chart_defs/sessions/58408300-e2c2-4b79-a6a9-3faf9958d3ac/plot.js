function plotChart(data, {width} = {}) {
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  
  return Plot.plot({
    width,
    height: 400,
    marginLeft: 60,
    x: {
      label: "Hour of Day",
      tickFormat: d => d.toString().padStart(2, '0') + ":00"
    },
    y: {
      label: "Day of Week",
      domain: days
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Number of Pickups"
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour_of_day,
        y: d => days[d.day_of_week],
        fill: d => d.pickup_count,
        tip: true
      })
    ],
    facet: {
      data: data,
      y: d => days[d.day_of_week]
    },
    fy: {
      axis: "left"
    }
  });
}