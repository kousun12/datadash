function plotChart(data, {width} = {}) {
  const days = Array.from(new Set(data.getChild('formatted_day').toArray())).sort();
  const phoneNumbers = Array.from(new Set(data.getChild('phone_number').toArray()));

  return Plot.plot({
    width,
    height: Math.max(500, phoneNumbers.length * 25),
    x: {
      type: "band",
      label: "Date",
      domain: days,
      tickFormat: d => d.split('-')[2], // Show only day of month
      tickRotate: 0
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
        x: d => d.formatted_day,
        y: d => d.phone_number,
        fill: d => d.message_count,
        title: d => `${d.phone_number}\n${d.formatted_day}\nMessages: ${d.message_count}`,
        tip: true
      })
    ],
    marginBottom: 50, // Increase bottom margin for date labels
    marginRight: 100 // Increase right margin for color legend
  });
}
