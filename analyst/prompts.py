generate_chart = """Respond with both the SQL and Observable Plot code required to implement this visualization. 
Respond only with a single sql code fence and a javascript code fence, nothing else.
The SQL flavor is DuckDB. 
The javascript code fence should include a function `plotChart` that returns a valid Observable Plot. `displayError` will be available to you as per `plot.j2`. Do not include any new imports.
Remember that `data` is an Apache Arrow table, so you cannot use normal array functions or indexing.
For example your response should be in this form:

```sql
<Your SQL code here>
```

```javascript
function plotChart(data, {width} = {}) {
return Plot.plot({
width,
...
});
}
```
"""
