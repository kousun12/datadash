function plotChart(data, {width} = {}) {
  const days = Array.from(new Set(data.getChild('day').toArray())).sort();
  const phoneNumbers = Array.from(new Set(data.getChild('phone_number').toArray()));

  return Plot.plot({
    width,
    height: Math.max(500, phoneNumbers.length * 25),
    x: {
      type: "time",
      label: "Date",
      tickFormat: "%Y-%m-%d"
    },
    y: {
      label: "Phone Number",
      domain: phoneNumbers
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Message Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: "day",
        y: "phone_number",
        fill: "message_count",
        title: d => `${d.phone_number}\n${d.day}\nMessages: ${d.message_count}`
      })
    ]
  });
}
