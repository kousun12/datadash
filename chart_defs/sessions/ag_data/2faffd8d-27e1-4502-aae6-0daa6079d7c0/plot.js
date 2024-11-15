function plotChart(data, {width} = {}) {
  // Data validation and preparation
  if (!data || typeof data.getColumn !== 'function') {
    console.error("Invalid or empty Arrow data");
    return displayError("No data available to display");
  }

  // Extract columns using Arrow methods
  const years = data.getColumn('year').toArray();
  const commodities = data.getColumn('Commodity').toArray();
  const attributes = data.getColumn('Attribute').toArray();
  const units = data.getColumn('Unit').toArray();
  const values = data.getColumn('value').toArray();
  const commodityTypes = data.getColumn('commodity_type').toArray();

  // Convert 'value' to numeric, filtering out non-numeric values
  const validData = values.map((value, i) => {
    const numValue = Number(value);
    if (isNaN(numValue)) {
      console.warn(`Invalid numeric value: ${value} for ${commodities[i]}`);
      return null;
    }
    return {
      year: years[i],
      commodity: commodities[i],
      attribute: attributes[i],
      unit: units[i],
      value: numValue,
      commodity_type: commodityTypes[i]
    };
  }).filter(d => d !== null);

  if (validData.length === 0) {
    return displayError("No valid numeric data to display");
  }

  // Get unique commodities and attributes for dropdowns
  const uniqueCommodities = [...new Set(commodities)];
  const uniqueAttributes = [...new Set(attributes)];

  // Create dropdown inputs
  const commoditySelect = Inputs.select(uniqueCommodities, {label: "Commodity", value: uniqueCommodities[0]});
  const attributeSelect = Inputs.select(uniqueAttributes, {label: "Attribute", value: uniqueAttributes[0]});

  // Filter data based on selections
  const filteredData = validData.filter(d => 
    d.commodity === commoditySelect && d.attribute === attributeSelect
  );

  // Determine y-axis range
  const yExtent = d3.extent(filteredData, d => d.value);
  const yDomain = [Math.min(0, yExtent[0]), yExtent[1]];

  // Create the plot
  const plot = Plot.plot({
    width,
    height: 500,
    marginRight: 80,
    x: {
      label: "Marketing/Calendar Year",
      tickRotate: 45
    },
    y: {
      label: "Value",
      grid: true,
      domain: yDomain
    },
    color: {
      legend: true
    },
    marks: [
      Plot.line(filteredData, {
        x: "year",
        y: "value",
        stroke: "commodity_type",
        strokeWidth: 2,
        curve: "natural"
      }),
      Plot.dot(filteredData, {
        x: "year",
        y: "value",
        stroke: "commodity_type",
        fill: "white",
        title: d => `${d.commodity}: ${d.attribute}\nValue: ${d.value} ${d.unit}\nYear: ${d.year}`
      }),
      Plot.text(filteredData, Plot.selectLast({
        x: "year",
        y: "value",
        text: d => d.commodity,
        dx: 3,
        anchor: "start"
      }))
    ]
  });

  // Combine inputs and plot
  return html`
    <div>
      ${commoditySelect}
      ${attributeSelect}
      ${plot}
    </div>
  `;
}

function displayError(message) {
  return html`<div style="color: red; text-align: center; padding: 20px;">${message}</div>`;
}
