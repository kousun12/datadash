WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    "Commodity" AS commodity,
    "Commodity Type" AS commodity_type,
    "Attribute" AS attribute,
    "Unit" AS unit,
    "Value text" AS value,
    "Source" AS source
  FROM ag_data
  WHERE "Attribute" = 'Beginning stocks'
)
SELECT * FROM filtered_data
ORDER BY year, commodity