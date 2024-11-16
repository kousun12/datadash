function plotChart(data, {width} = {}) {
  // NB data is an Apache Arrow table
  const years = data.getColumn('year').toArray();
  const commodities = data.getColumn('commodity').toArray();
  const commodityTypes = data.getColumn('commodity_type').toArray();
  const values = data.getColumn('value').toArray();
  const units = data.getColumn('unit').toArray();
  const sources = data.getColumn('source').toArray();
  const attributes = data.getColumn('attribute').toArray();

  const uniqueCommodities = [...new Set(commodities)];

  return Plot.plot({
    width,
    height: 600,
    marginRight: 200,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
    },
    y: {
      label: `${attributes[0]} (${units[0]})`,
      grid: true
    },
    color: {
      legend: true,
      scheme: "tableau10"
    },
    marks: [
      Plot.line(data.toArray(), {
        x: "year",
        y: "value",
        stroke: "commodity",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(data.toArray(), {
        x: "year",
        y: "value",
        stroke: "commodity",
        title: d => `${d.commodity}\nType: ${d.commodity_type}\nValue: ${d.value} ${d.unit}\nSource: ${d.source}`
      }),
      Plot.text(data.toArray(), Plot.selectLast({
        x: "year",
        y: "value",
        text: "commodity",
        dx: 3,
        textAnchor: "start",
        fontSize: 10
      }))
    ],
    color: {
      domain: uniqueCommodities,
      range: d3.schemeTableau10
    },
    legend: {
      color: {
        columns: (width > 640) ? 2 : 1,
        label: "Commodity"
      }
    }
  });
}