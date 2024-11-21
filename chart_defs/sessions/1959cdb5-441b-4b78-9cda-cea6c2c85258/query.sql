SELECT 
    strftime(date, '%Y-%m-%d') AS date,
    open, 
    high, 
    low, 
    close, 
    volume
FROM dji_data
WHERE ticker = 'MMM'
ORDER BY date
