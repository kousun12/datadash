function plotChart(data, {width} = {}) {
  // Comprehensive data validation and error handling
  if (!data || typeof data.getColumn !== 'function') {
    console.error("Invalid or empty Arrow data");
    return displayError("No data available to display. Please check the data source.");
  }

  try {
    // Extract columns using Arrow methods with error handling
    const years = data.getColumn('year')?.toArray() ?? [];
    const commodities = data.getColumn('Commodity')?.toArray() ?? [];
    const attributes = data.getColumn('Attribute')?.toArray() ?? [];
    const units = data.getColumn('Unit')?.toArray() ?? [];
    const values = data.getColumn('value')?.toArray() ?? [];
    const commodityTypes = data.getColumn('commodity_type')?.toArray() ?? [];

    if (!years.length || !commodities.length || !attributes.length || !values.length) {
      throw new Error("One or more required columns are missing or empty");
    }

    // Convert 'value' to numeric, filtering out non-numeric values
    const validData = values.map((value, i) => {
      const numValue = Number(value);
      if (isNaN(numValue)) {
        console.warn(`Invalid numeric value: ${value} for ${commodities[i]} in year ${years[i]}`);
        return null;
      }
      return {
        year: years[i],
        commodity: commodities[i],
        attribute: attributes[i],
        unit: units[i] || 'N/A',
        value: numValue,
        commodity_type: commodityTypes[i] || 'Unspecified'
      };
    }).filter(d => d !== null);

    if (validData.length === 0) {
      return displayError("No valid numeric data to display. All values were invalid or missing.");
    }

    // Get unique commodities, attributes, and commodity types for dropdowns
    const uniqueCommodities = [...new Set(validData.map(d => d.commodity))];
    const uniqueAttributes = [...new Set(validData.map(d => d.attribute))];
    const uniqueCommodityTypes = [...new Set(validData.map(d => d.commodity_type))];

    // Create dropdown inputs
    const commodityTypeSelect = Inputs.select(uniqueCommodityTypes, {label: "Commodity Type", value: uniqueCommodityTypes[0]});
    const commoditySelect = Inputs.select(uniqueCommodities, {label: "Commodity", value: uniqueCommodities[0]});
    const attributeSelect = Inputs.select(uniqueAttributes, {label: "Attribute", value: uniqueAttributes[0]});

    // Reactive filtering of data based on selections
    const filteredData = Generators.observe(notify => {
      const filtered = validData.filter(d => 
        d.commodity_type === commodityTypeSelect &&
        d.commodity === commoditySelect &&
        d.attribute === attributeSelect
      );
      notify(filtered);
      return filtered;
    });

    // Determine y-axis range dynamically
    const yExtent = d3.extent(filteredData, d => d.value);
    const yDomain = [Math.min(0, yExtent[0]), yExtent[1] * 1.1]; // Add 10% padding to the top

    // Create the plot
    const plot = Plot.plot({
      width,
      height: 500,
      marginRight: 120,
      x: {
        label: "Marketing/Calendar Year",
        tickRotate: 45
      },
      y: {
        label: filteredData.length > 0 ? `${filteredData[0].attribute} (${filteredData[0].unit})` : "Value",
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
          title: d => `${d.commodity}: ${d.attribute}\nValue: ${d.value.toLocaleString()} ${d.unit}\nYear: ${d.year}`
        }),
        Plot.text(filteredData, Plot.selectLast({
          x: "year",
          y: "value",
          text: d => d.commodity,
          dx: 3,
          dy: -3,
          fontSize: 10,
          fontWeight: "bold",
          fill: "commodity_type"
        }))
      ]
    });

    // Combine inputs and plot
    return html`
      <div>
        ${commodityTypeSelect}
        ${commoditySelect}
        ${attributeSelect}
        ${plot}
      </div>
    `;
  } catch (error) {
    console.error("Error in plotChart:", error);
    return displayError(`An error occurred while processing the data: ${error.message}`);
  }
}

function displayError(message) {
  return html`
    <div style="color: red; text-align: center; padding: 20px; border: 1px solid red; border-radius: 5px; background-color: #ffeeee;">
      <h3>Error</h3>
      <p>${message}</p>
      <p>Please check the data source and try again.</p>
    </div>
  `;
}
