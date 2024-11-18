function plotChart(data, {width} = {}) {
  const height = 800;
  const margin = {top: 40, right: 120, bottom: 40, left: 60};

  return Plot.plot({
    width,
    height,
    margin,
    x: {
      label: "Year",
      tickFormat: d => d.slice(0, 4)
    },
    y: {
      label: "Value",
      grid: true,
      transform: d => d / 1e6,
      tickFormat: d => d.toFixed(0) + "M"
    },
    color: {
      legend: true,
      scheme: "category10"
    },
    facet: {
      data: data,
      x: "Commodity Type",
      y: "Commodity",
      marginRight: 120
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "Year",
        y: d => +d.Value,
        fill: "Attribute",
        title: d => `${d.Commodity}\n${d.Attribute}\nYear: ${d.Year}\nValue: ${(+d.Value).toLocaleString()}`
      })),
      Plot.ruleY([0])
    ],
    style: {
      fontSize: "12px"
    },
    fx: {
      label: null
    },
    fy: {
      label: null
    }
  });
}
