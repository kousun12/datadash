function plotChart(data, {width} = {}) {
  const days = Array.from(new Set(data.getChild('day').toArray())).sort();
  const phoneNumbers = Array.from(new Set(data.getChild('phone_number').toArray()));

  return Plot.plot({
    width,
    height: Math.max(500, phoneNumbers.length * 25),
    x: {
      type: "band",
      label: "Date",
      tickFormat: d => d.substring(0, 10), // Format date as YYYY-MM-DD
      domain: days
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
        x: d => d.day,
        y: d => d.phone_number,
        fill: d => d.message_count,
        title: d => `${d.phone_number}\n${d.day}\nMessages: ${d.message_count}`
      })
    ]
  });
}
