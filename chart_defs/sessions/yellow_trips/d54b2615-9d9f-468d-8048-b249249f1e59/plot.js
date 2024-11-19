function plotChart(data, {width} = {}) {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const hours = Array.from({length: 24}, (_, i) => i);

  return Plot.plot({
    width,
    height: Math.min(400, width * 0.7),
    color: {
      type: "linear",
      scheme: "YlOrRd",
      legend: true,
      label: "Number of trips"
    },
    x: {
      label: "Hour of day",
      tickFormat: d => d.toString().padStart(2, '0') + ':00'
    },
    y: {
      label: "Day of week",
      domain: days
    },
    marks: [
      Plot.cell(data, {
        x: d => d.hour_of_day,
        y: d => days[d.day_of_week],
        fill: d => d.trip_count,
        tip: true
      })
    ],
    marginLeft: 60,
    marginBottom: 50,
    style: {
      fontSize: 12
    }
  });
}