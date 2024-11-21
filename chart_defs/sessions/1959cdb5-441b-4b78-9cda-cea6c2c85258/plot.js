function plotChart(data, {width} = {}) {
  // Check if data is available and has rows
  if (!data || data.numRows === 0) {
    return displayError("No data available to plot.");
  }

  // Check if required columns exist
  const requiredColumns = ['date', 'open', 'high', 'low', 'close', 'volume'];
  const missingColumns = requiredColumns.filter(col => !data.schema.fields.some(field => field.name === col));
  if (missingColumns.length > 0) {
    return displayError(`Missing required columns: ${missingColumns.join(', ')}`);
  }

  const height = 500;
  const marginTop = 20;
  const marginRight = 30;
  const marginBottom = 50;
  const marginLeft = 40;

  // Helper function to get max value from a column
  const getMaxValue = (columnName) => {
    let max = -Infinity;
    for (let i = 0; i < data.numRows; i++) {
      const value = data.getChild(columnName).get(i);
      if (value !== null && value !== undefined && !isNaN(value)) {
        max = Math.max(max, value);
      }
    }
    return max === -Infinity ? 0 : max;
  };

  // Helper function to safely access data
  const safeGet = (d, key) => {
    const value = d[key];
    return value !== null && value !== undefined && !isNaN(value) ? value : null;
  };

  try {
    const xDomain = Array.from({length: data.numRows}, (_, i) => data.getChild('date').get(i))
      .filter(d => d !== null && d !== undefined);
    const yMax = getMaxValue("high");
    const y2Max = getMaxValue("volume");

    return Plot.plot({
      width,
      height,
      marginTop,
      marginRight,
      marginBottom,
      marginLeft,
      x: {
        type: "band",
        label: "Date",
        domain: xDomain,
      },
      y: {
        label: "Price ($)",
      },
      y2: {
        label: "Volume",
      },
      marks: [
        Plot.ruleY([0]),
        Plot.barY(data, {
          x: d => safeGet(d, 'date'),
          y: d => safeGet(d, 'volume'),
          fill: d => safeGet(d, 'close') > safeGet(d, 'open') ? "green" : "red",
          fillOpacity: 0.3,
          y2: "y2"
        }),
        Plot.ruleY(data, {
          x: d => safeGet(d, 'date'),
          y1: d => safeGet(d, 'low'),
          y2: d => safeGet(d, 'high'),
          stroke: d => safeGet(d, 'close') > safeGet(d, 'open') ? "green" : "red",
        }),
        Plot.rectY(data, {
          x: d => safeGet(d, 'date'),
          y1: d => Math.min(safeGet(d, 'open'), safeGet(d, 'close')),
          y2: d => Math.max(safeGet(d, 'open'), safeGet(d, 'close')),
          fill: d => safeGet(d, 'close') > safeGet(d, 'open') ? "green" : "red",
        }),
      ],
    });
  } catch (error) {
    return displayError(`Error creating plot: ${error.message}`);
  }
}
