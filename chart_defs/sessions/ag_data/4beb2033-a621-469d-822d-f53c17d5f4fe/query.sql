WITH ranked_commodities AS (
  SELECT Commodity, COUNT(*) as count,
         ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) as rank
  FROM ag_data
  GROUP BY Commodity
),
top_commodities AS (
  SELECT Commodity
  FROM ranked_commodities
  WHERE rank <= 5
)
SELECT ad."Commodity Type", ad.Commodity, ad.Attribute, ad."Marketing/calendar year" as Year, ad."Value text" as Value
FROM ag_data ad
JOIN top_commodities tc ON ad.Commodity = tc.Commodity
WHERE ad.Attribute IN ('Beginning stocks', 'Production', 'Imports')
  AND ad."Marketing/calendar year" >= '2010/11'
ORDER BY ad."Commodity Type", ad.Commodity, ad."Marketing/calendar year", ad.Attribute