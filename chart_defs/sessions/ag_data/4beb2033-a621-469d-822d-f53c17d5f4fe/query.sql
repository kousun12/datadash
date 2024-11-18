SELECT 
  "Commodity Type",
  "Marketing/calendar year" AS Year,
  SUM(CAST("Value text" AS FLOAT)) AS TotalValue
FROM ag_data
WHERE "Marketing/calendar year" >= '2010/11'
  AND Attribute IN ('Beginning stocks', 'Production', 'Imports')
GROUP BY "Commodity Type", "Marketing/calendar year"
ORDER BY "Commodity Type", "Marketing/calendar year"
