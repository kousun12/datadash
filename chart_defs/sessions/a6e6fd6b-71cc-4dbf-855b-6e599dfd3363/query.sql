WITH daily_counts AS (
  SELECT 
    date_trunc('day', column6) AS day,
    column1 AS phone_number,
    COUNT(*) AS message_count
  FROM messages
  WHERE column1 != 'None'
  GROUP BY 1, 2
)
SELECT 
  day,
  phone_number,
  message_count
FROM daily_counts
ORDER BY day, phone_number
