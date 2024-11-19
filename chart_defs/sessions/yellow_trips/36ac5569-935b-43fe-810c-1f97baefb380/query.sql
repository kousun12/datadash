WITH trip_counts AS (
  SELECT 
    PULocationID, 
    DOLocationID, 
    COUNT(*) as trip_count
  FROM yellow_trips
  GROUP BY PULocationID, DOLocationID
)
SELECT * FROM trip_counts
ORDER BY trip_count DESC
LIMIT 10000