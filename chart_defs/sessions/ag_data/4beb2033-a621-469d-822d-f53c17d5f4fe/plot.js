function plotChart(data, {width} = {}) {
  const height = 500;
  const margin = {top: 20, right: 30, bottom: 40, left: 60};

  return Plot.plot({
    width,
    height,
    margin,
    x: {
      label: "Year",
      tickFormat: d => d.slice(0, 4)
    },
    y: {
      label: "Total Value",
      grid: true,
      transform: d => d / 1e9,
      tickFormat: d => d.toFixed(1) + "B"
    },
    color: {
      legend: true,
      scheme: "category10"
    },
    marks: [
      Plot.areaY(data, Plot.stackY({
        x: d => d.Year,
        y: d => d.TotalValue,
        z: d => d["Commodity Type"],
        fill: d => d["Commodity Type"],
        title: d => `${d["Commodity Type"]}\nYear: ${d.Year}\nValue: ${d.TotalValue.toLocaleString()}`
      })),
      Plot.ruleY([0])
    ],
    style: {
      fontSize: "12px"
    }
  });
}
