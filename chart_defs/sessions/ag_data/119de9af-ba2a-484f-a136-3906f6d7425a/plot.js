function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    marginRight: 80,
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
        fill: "commodity_type"
      }),
      Plot.text(data, Plot.selectLast({
        x: "year",
        y: "value",
        text: d => d.commodity,
        dx: 3,
        dy: -3,
        anchor: "start",
        fontSize: 10
      })),
      Plot.tip(data, Plot.pointerX({
        x: "year",
        y: "value",
        title: d => `${d.commodity} (${d.commodity_type})\nYear: ${d.year}\nValue: ${d.value} ${d.unit}`
      }))
    ],
    facet: {
      data: data,
      y: "unit"
    },
    fy: {
      label: "Unit"
    }
  });
}