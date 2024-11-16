function plotChart(data, {width} = {}) {
  return Plot.plot({
    width,
    height: 600, // Increased height to accommodate rotated labels
    marginBottom: 80, // Increased bottom margin for x-axis labels
    marginRight: 120, // Increased right margin for legend
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45,
      labelOffset: 50 // Increased offset to prevent overlap with rotated labels
    },
    y: {
      label: "Value (Million bushels)",
      grid: true
    },
    color: {
      legend: true,
      scheme: "tableau10" // Use a color scheme that works well for multiple categories
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "year",
        y: "value",
        fill: "Commodity",
        stroke: "white",
        strokeWidth: 1,
        curve: "natural"
      })),
      Plot.tip(data, Plot.pointerY({
        x: "year",
        y: Plot.stackY({
          y: "value",
          offset: "zero",
          order: "sum",
          reverse: true
        }),
        title: (d) => `${d.Commodity}\nYear: ${d.year}\nValue: ${d.value.toLocaleString()} million bushels`,
        fill: "Commodity",
        fillOpacity: 0.8
      }))
    ],
    tooltip: {
      hidden: false
    }
  });
}
