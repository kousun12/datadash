WITH pickup_counts AS (
  SELECT PULocationID, COUNT(*) as pickup_count
  FROM yellow_trips
  GROUP BY PULocationID
)
SELECT 
  y.PULocationID,
  COALESCE(p.pickup_count, 0) as pickup_count
FROM yellow_trips y
LEFT JOIN pickup_counts p ON y.PULocationID = p.PULocationID
GROUP BY y.PULocationID, p.pickup_count
ORDER BY pickup_count DESC