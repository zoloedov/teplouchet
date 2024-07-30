SELECT name, round(avg(value), 3) as avarage, max(value) as maximum, min(value) as minimum, report_order FROM
	(SELECT * FROM vkt_data WHERE timestamp > datetime("now", "localtime", "start of day", "+9 hour") AND timestamp < datetime("now", "localtime") AND scheme = 'sn_' AND quality = "Good")
GROUP by name ORDER by report_order;