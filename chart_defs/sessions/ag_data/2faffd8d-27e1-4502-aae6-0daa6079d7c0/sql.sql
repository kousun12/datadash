SELECT 
  "Marketing/calendar year" as year,
  Commodity,
  Attribute,
  Unit,
  "Value text" as value,
  "Commodity Type" as commodity_type
FROM ag_data
ORDER BY "Marketing/calendar year"