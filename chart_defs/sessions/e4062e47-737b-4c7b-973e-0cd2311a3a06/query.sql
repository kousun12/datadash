WITH pickup_counts AS (
  SELECT PULocationID, COUNT(*) as pickup_count
  FROM yellow_trips
  GROUP BY PULocationID
)
SELECT 
  y.PULocationID,
  COALESCE(p.pickup_count, 0) as pickup_count,
  COALESCE(z.Zone, 'Unknown') as zone_name
FROM yellow_trips y
LEFT JOIN pickup_counts p ON y.PULocationID = p.PULocationID
LEFT JOIN taxi_zone_lookup z ON y.PULocationID = z.LocationID
GROUP BY y.PULocationID, p.pickup_count, z.Zone
ORDER BY pickup_count DESC
