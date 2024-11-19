WITH hourly_pickups AS (
  SELECT 
    EXTRACT(DOW FROM tpep_pickup_datetime) AS day_of_week,
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour_of_day,
    COUNT(*) AS pickup_count
  FROM yellow_trips
  GROUP BY 1, 2
)
SELECT 
  day_of_week,
  hour_of_day,
  pickup_count
FROM hourly_pickups
ORDER BY day_of_week, hour_of_day