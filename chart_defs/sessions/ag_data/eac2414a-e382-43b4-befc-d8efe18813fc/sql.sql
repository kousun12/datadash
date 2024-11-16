WITH filtered_data AS (
  SELECT 
    "Marketing/calendar year" AS year,
    Commodity,
    "Commodity Type",
    Attribute,
    Unit,
    "Value text" AS value
  FROM ag_data
  WHERE "Commodity Type" = 'Crops'
    AND Attribute = 'Beginning stocks'
    AND Unit = 'Million bushels'
)
SELECT * FROM filtered_data
ORDER BY year, Commodity