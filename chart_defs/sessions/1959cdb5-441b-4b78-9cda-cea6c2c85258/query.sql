SELECT date, open, high, low, close, volume
FROM dji_data
WHERE ticker = 'MMM'
ORDER BY date