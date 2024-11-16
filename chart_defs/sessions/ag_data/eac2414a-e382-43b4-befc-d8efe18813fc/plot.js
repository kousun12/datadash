function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 500,
    marginRight: 100,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
    },
    y: {
      label: "Value (Million bushels)",
      grid: true
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(data, {
        x: "year",
        y: "value",
        stroke: "Commodity",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(data, {
        x: "year",
        y: "value",
        stroke: "Commodity",
        fill: "white"
      }),
      Plot.tip(data, Plot.pointerX({
        x: "year",
        y: "value",
        title: (d) => `${d.Commodity}\nYear: ${d.year}\nValue: ${d.value.toLocaleString()} million bushels`,
        stroke: "Commodity",
        fill: "white",
        fillOpacity: 0.8,
        strokeWidth: 2
      })),
      Plot.ruleY([0])
    ],
    tooltip: {
      hidden: false,
      position: "fixed"
    }
  });
}
