---
toc: false
---


```js
const db = await DuckDBClient.of({base: FileAttachment("./data/cpi.parquet")});
const data = db.sql`SELECT * FROM base`;
```

```js
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
      label: "Date →",
      grid: true,
      tickFormat: d3.timeFormat("%Y"),
      tickRotate: 45
    },
    
    marks: [
      Plot.gridY({ strokeOpacity: 0.5 }),
      Plot.gridX({ strokeOpacity: 0.5 }),
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
      
      // January dots using arrow data
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
      // mark the baseline years:
      Plot.rectY(data, { 
        x: new Date("1982-01-01"), x2: new Date("1984-01-01"), 
        fill: "#88888802", y: 0, y2: d3.max(data, d => d.CPIAUCSL) 
      }),
      Plot.ruleY([100], {stroke: "#888888", strokeDasharray: "5,5"}),
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
        <div>
          <ul>
            ${todos.map(todo => `<li>${todo}</li>`)}
          </ul>
        </div>
      </div>
      <div class="input-area">
        ${promptInput}
        ${send}
      </div>
    </div>
  </div>
  <div class="card">${resize((width) => plotTimeline(data, {width}))}</div>
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
</style>
