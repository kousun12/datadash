function plotChart(data, {width} = {}) {
  const hours = Array.from(new Set(data.getChild('hour').toArray())).sort();
  const phoneNumbers = Array.from(new Set(data.getChild('phone_number').toArray()));

  return Plot.plot({
    width,
    height: 500,
    y: {
      grid: true,
      label: "Message Count"
    },
    x: {
      type: "time",
      label: "Time"
    },
    color: {
      scheme: "tableau10"
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "hour",
        y: "message_count",
        z: "phone_number",
        fill: "phone_number",
        stroke: "phone_number",
        title: d => `${d.phone_number}: ${d.message_count} messages`
      })),
      Plot.ruleY([0])
    ],
    legend: true
  });
}