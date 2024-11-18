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
        title: (d) => {
          const commodity = d.get('Commodity');
          const year = d.get('year');
          const value = (+d.get('value')).toLocaleString();
          return `${commodity}\nYear: ${year}\nValue: ${value} million bushels`;
        },
        lineWidth: 1,
        frameAnchor: "bottom-left",
        fillOpacity: 0.8
      }))
    ],
    tooltip: {
      hidden: false
    }
  });
}
