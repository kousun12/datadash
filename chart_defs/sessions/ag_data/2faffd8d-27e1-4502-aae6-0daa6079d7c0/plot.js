function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    marginRight: 40,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
    },
    y: {
      label: "Value",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(data, {
        x: "year",
        y: "value",
        stroke: "commodity",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(data, {
        x: "year",
        y: "value",
        stroke: "commodity",
        fill: "white",
        title: d => `${d.commodity}: ${d.attribute}\nValue: ${d.value} ${d.unit}\nYear: ${d.year}`
      }),
      Plot.text(data, Plot.selectLast({
        x: "year",
        y: "value",
        text: d => d.commodity,
        dx: 3,
        anchor: "start"
      }))
    ],
    facet: {
      data,
      y: "commodity_type"
    },
    fy: {
      domain: ["Crops", "Livestock/Dairy"]
    }
  });
}