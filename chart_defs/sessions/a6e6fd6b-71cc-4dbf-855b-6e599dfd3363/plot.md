---
title: "Message Frequency Heatmap"
toc: false
sidebar: false
header: false
footer: false
pager: false

---
```js
import {Editor} from "/components/Editor.js";
```

# Message Frequency Heatmap

This heatmap displays the frequency of messages over time for different phone numbers, allowing for easy visualization of communication patterns and relative activity levels among different contacts.


```js
const db = DuckDBClient.of({ds: FileAttachment("/data/imessages.db")});
```

```js
const data = db.sql`
WITH daily_counts AS (
  SELECT 
    date_trunc('day', column6) AS day,
    strftime(date_trunc('day', column6), '%Y-%m-%d') AS formatted_day,
    column1 AS phone_number,
    COUNT(*) AS message_count
  FROM ds.messages
  WHERE column1 != 'None'
  GROUP BY 1, 2, 3
)
SELECT 
  formatted_day,
  phone_number,
  message_count
FROM daily_counts
ORDER BY day, phone_number
`
```


```js
function plotChart(data, {width} = {}) {
  const days = Array.from(new Set(data.getChild('formatted_day').toArray())).sort();
  const phoneNumbers = Array.from(new Set(data.getChild('phone_number').toArray()));

  return Plot.plot({
    width,
    height: Math.max(500, phoneNumbers.length * 25),
    x: {
      type: "band",
      label: "Date",
      domain: days,
      tickFormat: d => d.split('-')[2], // Show only day of month
      tickRotate: 0
    },
    y: {
      label: "Phone Number",
      domain: phoneNumbers
    },
    color: {
      type: "linear",
      scheme: "YlOrRd",
      label: "Message Count",
      legend: true
    },
    marks: [
      Plot.cell(data, {
        x: d => d.formatted_day,
        y: d => d.phone_number,
        fill: d => d.message_count,
        title: d => `${d.phone_number}\n${d.formatted_day}\nMessages: ${d.message_count}`,
        tip: true
      })
    ],
    marginBottom: 50, // Increase bottom margin for date labels
    marginRight: 100 // Increase right margin for color legend
  });
}


function displayError(message) {
    return html`<div style="color: red; text-align: center; padding: 20px;">Error: ${message}</div>`;
}

function plotOrError(data, options) {
    try {
        return plotChart(data, options);
    } catch (e) {
        return displayError(e.message);
    }
}
```

```js
function getJSView() {
  const plotCodeString = "function plotChart(data, {width} = {}) {\n  const days = Array.from(new Set(data.getChild('formatted_day').toArray())).sort();\n  const phoneNumbers = Array.from(new Set(data.getChild('phone_number').toArray()));\n\n  return Plot.plot({\n    width,\n    height: Math.max(500, phoneNumbers.length * 25),\n    x: {\n      type: \"band\",\n      label: \"Date\",\n      domain: days,\n      tickFormat: d => d.split('-')[2], // Show only day of month\n      tickRotate: 0\n    },\n    y: {\n      label: \"Phone Number\",\n      domain: phoneNumbers\n    },\n    color: {\n      type: \"linear\",\n      scheme: \"YlOrRd\",\n      label: \"Message Count\",\n      legend: true\n    },\n    marks: [\n      Plot.cell(data, {\n        x: d => d.formatted_day,\n        y: d => d.phone_number,\n        fill: d => d.message_count,\n        title: d => `${d.phone_number}\\n${d.formatted_day}\\nMessages: ${d.message_count}`,\n        tip: true\n      })\n    ],\n    marginBottom: 50, // Increase bottom margin for date labels\n    marginRight: 100 // Increase right margin for color legend\n  });\n}\n";
  const e = Editor({value: plotCodeString, lang: "javascript"});
  return e;
}
function getSQLView() {
    const sqlString = `WITH daily_counts AS (
  SELECT 
    date_trunc('day', column6) AS day,
    strftime(date_trunc('day', column6), '%Y-%m-%d') AS formatted_day,
    column1 AS phone_number,
    COUNT(*) AS message_count
  FROM ds.messages
  WHERE column1 != 'None'
  GROUP BY 1, 2, 3
)
SELECT 
  formatted_day,
  phone_number,
  message_count
FROM daily_counts
ORDER BY day, phone_number
`;
    const e = Editor({value: sqlString, lang: "sql"});
    return e;
}
```

<div class="grid grid-cols-1">
    <div class="card">
        ${resize((width) => plotOrError(data, {width}))}
    </div>
</div>

### Raw Code

The following shows the `Plot` code as well as the `sql` used to drive the above visualizations.

<div class="grid grid-cols-2">
    <div class="card">
        ${getJSView()}
    </div>
    <div class="card">
        ${getSQLView()}
    </div>
</div>

### Data

This is the raw data resulting from the SQL query.

```js
display(Inputs.table(data));
```