WITH hourly_pickups AS (
  SELECT 
    PULocationID,
    date_trunc('hour', tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS pickup_count
  FROM yellow_trips
  GROUP BY PULocationID, pickup_hour
)
SELECT 
  hp.PULocationID,
  hp.pickup_hour,
  hp.pickup_count
FROM hourly_pickups hp
ORDER BY hp.pickup_hour, hp.pickup_count DESC