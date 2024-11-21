WITH hourly_counts AS (
  SELECT 
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
    PULocationID,
    COUNT(*) AS trip_count
  FROM yellow_trips
  GROUP BY 1, 2
),
top_locations AS (
  SELECT PULocationID
  FROM hourly_counts
  GROUP BY PULocationID
  ORDER BY SUM(trip_count) DESC
  LIMIT 20
)
SELECT 
  h.hour,
  h.PULocationID,
  h.trip_count
FROM hourly_counts h
JOIN top_locations t ON h.PULocationID = t.PULocationID
ORDER BY h.PULocationID, h.hour