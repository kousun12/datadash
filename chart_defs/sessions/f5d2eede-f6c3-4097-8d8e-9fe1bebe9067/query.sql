WITH hourly_pickups AS (
  SELECT 
    z.Zone,
    EXTRACT(HOUR FROM y.tpep_pickup_datetime) AS hour,
    COUNT(*) AS pickup_count
  FROM yellow_trips y
  JOIN zones z ON y.PULocationID = z.LocationID
  GROUP BY z.Zone, EXTRACT(HOUR FROM y.tpep_pickup_datetime)
),
top_zones AS (
  SELECT Zone, SUM(pickup_count) as total_pickups
  FROM hourly_pickups
  GROUP BY Zone
  ORDER BY total_pickups DESC
  LIMIT 10
)
SELECT hp.Zone, hp.hour, hp.pickup_count, tz.total_pickups
FROM hourly_pickups hp
JOIN top_zones tz ON hp.Zone = tz.Zone
ORDER BY tz.total_pickups DESC, hp.hour
