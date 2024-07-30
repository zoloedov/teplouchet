SELECT name, round(avg(value), 3) as avarage, max(value) as maximum, min(value) as minimum, scheme, report_order FROM
(SELECT * FROM vkt_data WHERE timestamp > datetime("now","localtime", "-1 hour") AND timestamp < datetime("now","localtime") AND quality = "Good" AND report_order > 0)
GROUP by  name ORDER by scheme
