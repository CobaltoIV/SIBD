SELECT severity, locality, week_day, COUNT(*)
FROM f_incident NATURAL JOIN d_location NATURAL JOIN d_time
GROUP BY CUBE(severity, locality,week_day);