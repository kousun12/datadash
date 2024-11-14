---
toc: false
---


```js
const db = await DuckDBClient.of({base: FileAttachment("./data/cpi.parquet")});
const data = db.sql`SELECT * FROM base`; // returns Arrow table
```

```js
function calculateYearlyChange(data) {
  const changes = [];
  for (let i = 1; i < data.length; i++) {
    const previous = data[i - 1];
    const current = data[i];
    const change = ((current.CPIAUCSL - previous.CPIAUCSL) / previous.CPIAUCSL) * 100;
    changes.push({
      DATE: current.DATE,
      YearlyChange: change
    });
  }
  return changes;
}

function plotYearlyChange(data, {width} = {}) {
  return Plot.plot({
    title: "Year-to-Year CPI Change (%)",
    width,
    y: {
      label: "Year-to-Year Change (%)",
      grid: true,
      tickFormat: d => d.toFixed(1) + '%'
    },
    x: {
      label: "Year →",
      grid: true,
      tickFormat: d3.timeFormat("%Y"),
    },
    marks: [
      Plot.gridY({ strokeOpacity: 0.5 }),
      Plot.line(data, {
        x: d => new Date(d.DATE),
        y: "YearlyChange",
        stroke: "var(--theme-accent)",
        strokeWidth: 2
      })
    ],
    caption: "Year-to-Year CPI Percent Change"
  });
}

function plotTimeline(data, {width} = {}) {
  return Plot.plot({
    title: "Consumer Price Index (CPI) Historical Trend",
    width,
    y: {
      label: "CPI (1982-1984 = 100)",
      grid: true,
      tickFormat: d => d.toLocaleString()
    },
    x: {
      label: "Year →",
      grid: true,
      tickFormat: d3.timeFormat("%Y"),
    },
    
    marks: [
      Plot.gridY({ strokeOpacity: 0.5 }),
      Plot.gridX({ strokeOpacity: 0.5 }),
      Plot.rectY(data, { 
        x: new Date("1982-01-01"), x2: new Date("1984-01-01"), 
        fill: "#88888802", y: 0, y2: d3.max(data, d => d.CPIAUCSL) 
      }),
      Plot.areaY(data, {
        x: d => new Date(d.DATE),
        y: "CPIAUCSL",
        fill: "var(--theme-green)",
        stroke: "none",
      }),

      Plot.line(data, {
        x: d => new Date(d.DATE),
        y: "CPIAUCSL",
        stroke: "var(--theme-foreground)",
        strokeWidth: 2
      }),

      Plot.dot(data, {
        x: d => new Date(d.DATE),
        y: "CPIAUCSL",
        stroke: "var(--theme-foreground-focus)",
        fill: "var(--theme-foreground-fainter)",
        strokeWidth: 1,
        r: 2,
        filter: d => new Date(d.DATE).getMonth() === 0,
        title: d => `${d3.timeFormat("%B %Y")(new Date(d.DATE))}`,
        fill: "var(--theme-foreground-fainter)",
        strokeWidth: 1,
        r: 2,
        filter: d => new Date(d.DATE).getMonth() === 0,
        tip: {
          title: d => `${d3.timeFormat("%B %Y")(new Date(d.DATE))}`,
          body: d => `CPI: ${d.CPIAUCSL.toFixed(1)}`
        },
      }),
      Plot.ruleY([100], {stroke: "#888888", strokeDasharray: "5,5"}),

      Plot.ruleX([
        {date: new Date("1973-10-01"), label: "1973 Oil Crisis"},
        {date: new Date("1980-01-01"), label: "1980s Inflation Peak"},
        {date: new Date("2008-09-15"), label: "2008 Financial Crisis"},
        {date: new Date("2020-03-11"), label: "COVID-19 Pandemic"},
        {date: new Date("1951-02-07"), label: "1951 Inflation Spike"},
        {date: new Date("1990-07-01"), label: "1990 Oil Price Shock"},
        {date: new Date("1962-10-16"), label: "Cuban Missile Crisis"},
        {date: new Date("2001-09-11"), label: "9/11 Attacks"},
        {date: new Date("2022-02-24"), label: "Russia-Ukraine War Begins"}
      ], {
        x: "date",
        stroke: "var(--theme-red)",
        strokeWidth: 1.5,
        strokeDasharray: "4,2",
        title: d => d.label,
      }),
    ],
    
    caption: "Source: Federal Reserve Economic Data (FRED)"
  });
}
```

```js
// const url = 'https://substratelabs--datadash-api.modal.run';
const url = 'http://127.0.0.1:8000';

const promptInput = Inputs.textarea({
  placeholder: "What do you want to do?",
  value: ""
});
const todos = Mutable([])
const addItem = (item) => {
  todos.value.push(item)
  return todos.value
}

const send = Inputs.button("Send", { reduce: (prev) => {
    const prompt = promptInput.value
    console.log("Prompt:", prompt);
    // post request to url:
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt })
    }).then(response => response.json()).then(data => {
      console.log("Data:", data);
      if (data.todo) {
        addItem(data.todo)
      }
      promptInput.value = ""
    });
    return prev + 1;
  }}
);
```

```js
console.log(todos);
```

<div>
    <div class="card-body">
    <h2>CPI Over time</h2>
    <p>Consumer Price Index (CPI) Historical Trend</p>
    </div>
</div>

<div class="grid" style="grid-template-columns: 1fr 3fr; grid-auto-rows: 504px;">
  <div class="card">
    <div class="card-content">
      <div class="content-area">
        ${todos.map(todo => html`<div class="todo-item">${todo}</div>`)}
      </div>
      <div class="input-area">
        ${promptInput}
        ${send}
      </div>
    </div>
  <div class="card">
    ${resize((width) => plotTimeline(data, {width}))}
  </div>
  <div class="card">
    ${resize(async (width) => {
      const yearlyChangeData = calculateYearlyChange(await data.toArray());
      if (yearlyChangeData.length === 0) {
        return html`<div class="no-data-message">No data available for plotting.</div>`;
      } else {
        return plotYearlyChange(yearlyChangeData, {width});
      }
    })}
  </div>
    ${resize((width) => plotTimeline(data, {width}))}
  </div>
</div>

<style>
  .card {
    display: flex;
    flex-direction: column;
  }
  .card-content {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .content-area {
    flex: 1;
    min-height: 0;
    background: var(--theme-background-alt);
    border: solid 1px var(--theme-foreground-faintest);
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 6px;
  }
  .input-area {
    margin-top: auto;
  }
  .card div form {
    width: 100%;
  }
  .card div textarea {
    height: 48px;
    padding: 9px;
    border-radius: 6px;
    resize: none;
    width: 100%;
  }
  .card button {
    padding: 4px 10px;
    margin: 12px 0;
  }
  .todo-item {
    padding: 0.3rem;
    margin: 0.5rem;
    background: var(--theme-foreground-faintest);
    border-radius: 4px;
  }
</style>
