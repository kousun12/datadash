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
    console.log("You said:", promptInput.value);
    promptInput.value = ""
    fetch()
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
    ${promptInput}
    ${send}
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
  .card div textarea {
    width: 100%;
    height: 48px;
    padding: 9px;
    margin-bottom: 12px;
    border-radius: 6px;
    resize: none;
  }
  .card button {
    padding: 4px;
    margin: 12px 0;
  }
</style>