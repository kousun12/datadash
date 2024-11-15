function plotChart(data, {width} = {}) {
  // Data validation and preparation
  if (!Array.isArray(data) || data.length === 0) {
    console.error("Invalid or empty data");
    return displayError("No data available to display");
  }

  // Convert 'value' to numeric, filtering out non-numeric values
  const validData = data.filter(d => {
    const numValue = Number(d.value);
    if (isNaN(numValue)) {
      console.warn(`Invalid numeric value: ${d.value} for ${d.commodity}`);
      return false;
    }
    d.value = numValue;
    return true;
  });

  if (validData.length === 0) {
    return displayError("No valid numeric data to display");
  }

  // Get unique commodities and attributes for dropdowns
  const commodities = [...new Set(validData.map(d => d.commodity))];
  const attributes = [...new Set(validData.map(d => d.attribute))];

  // Create dropdown inputs
  const commoditySelect = Inputs.select(commodities, {label: "Commodity", value: commodities[0]});
  const attributeSelect = Inputs.select(attributes, {label: "Attribute", value: attributes[0]});

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
