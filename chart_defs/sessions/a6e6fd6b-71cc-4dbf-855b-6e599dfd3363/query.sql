WITH hourly_counts AS (
  SELECT 
    date_trunc('hour', column6) AS hour,
    column1 AS phone_number,
    COUNT(*) AS message_count
  FROM messages
  WHERE column1 != 'None'
  GROUP BY 1, 2
)
SELECT 
  hour,
  phone_number,
  message_count
FROM hourly_counts
ORDER BY hour, phone_number