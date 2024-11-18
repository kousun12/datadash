function plotChart(data, {width} = {}) {
  const height = 500;
  const margin = {top: 20, right: 30, bottom: 40, left: 50};

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
      grid: true
    },
    color: {
      legend: true
    },
    facet: {
      data,
      x: "Commodity Type",
      y: "Commodity",
      marginRight: 90
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: "Year",
        y: "Value",
        fill: "Attribute",
        title: d => `${d.Commodity}\n${d.Attribute}\nYear: ${d.Year}\nValue: ${d.Value.toLocaleString()}`
      })),
      Plot.ruleY([0])
    ]
  });
}