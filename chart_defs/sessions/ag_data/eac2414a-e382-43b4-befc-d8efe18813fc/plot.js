function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 600,
    marginBottom: 80,
    marginRight: 120,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45,
      labelOffset: 50
    },
    y: {
      label: "Value (Million bushels)",
      grid: true
    },
    color: {
      legend: true,
      scheme: "tableau10"
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: d => d.year,
        y: d => +d.value,
        z: d => d.Commodity,
        fill: d => d.Commodity,
        stroke: "white",
        strokeWidth: 1,
        curve: "natural"
      })),
      Plot.ruleY([0]),
      Plot.tip(data, Plot.pointerX({
        x: d => d.year,
        y: d => +d.value,
        z: d => d.Commodity,
        title: d => `${d.Commodity}\nYear: ${d.year}\nValue: ${(+d.value).toLocaleString()} million bushels`,
        fill: d => d.Commodity,
        fillOpacity: 0.8
      }))
    ],
    tooltip: {
      hidden: false
    }
  });
}
