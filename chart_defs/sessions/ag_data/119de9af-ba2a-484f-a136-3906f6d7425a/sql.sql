WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    "Commodity Type" AS commodity_type,
    Commodity,
    Attribute,
    Unit,
    "Value text" AS value
  FROM ag_data
  WHERE Attribute = 'Beginning stocks'
    AND "Marketing/calendar year" >= '1990/91'
)
SELECT *
FROM filtered_data
ORDER BY year, commodity_type, Commodity