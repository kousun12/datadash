WITH daily_counts AS (
  SELECT 
    date_trunc('day', column6) AS day,
    strftime(date_trunc('day', column6), '%Y-%m-%d') AS formatted_day,
    column1 AS phone_number,
    COUNT(*) AS message_count
  FROM messages
  WHERE column1 != 'None'
  GROUP BY 1, 2, 3
)
SELECT 
  formatted_day,
  phone_number,
  message_count
FROM daily_counts
ORDER BY day, phone_number
