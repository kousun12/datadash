---
toc: false
---

```js
const cpiPage = await FileAttachment("./cpi.md").text();
const url = 'https://substratelabs--datadash-api.modal.run';

const promptInput = Inputs.textarea({
  placeholder: "What do you want to do?",
  value: ""
});

const send = Inputs.button("Send", { reduce: (prev) => {
    const prompt = promptInput.value
    console.log("Prompt:", prompt);
    // post request to url:
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({query: prev})
    }).then(response => response.json()).then(data => {
      console.log("Data:", data);
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
        <!-- Content will go here -->
      </div>
      <div class="input-area">
        ${promptInput}
        ${send}
      </div>
    </div>
  </div>
  <div class="card">${
    resize((width) => Plot.plot({
      title: "How big are penguins, anyway? 🐧", 
      width,
      grid: true,
      x: {label: "Body mass (g)"},
      y: {label: "Flipper length (mm)"},
      color: {legend: true},
      marks: [
        Plot.linearRegressionY(penguins, {x: "body_mass_g", y: "flipper_length_mm", stroke: "species"}),
        Plot.dot(penguins, {x: "body_mass_g", y: "flipper_length_mm", stroke: "species", tip: true})
      ]
    }))
  }</div>
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
