import sqlite3

connection = sqlite3.connect('vkt.db')
cursor = connection.cursor()
# cursor.execute('DROP TABLE IF EXISTS vkt_data')
cursor.execute('CREATE TABLE vkt_data (id INTEGER PRIMARY KEY AUTOINCREMENT,\
 name TEXT, value REAL, timestamp DATETIME, quality TEXT, test TINYINT, scheme TEXT, report_order TINYINT)')
# cursor.execute('CREATE unique INDEX time_and_id ON vkt_data(timestamp ASC, external_id)')
cursor.execute('CREATE unique INDEX time_and_id ON vkt_data(timestamp ASC, id)')
# cursor.execute('DROP TABLE IF EXISTS latest_calibration')
# cursor.execute('CREATE TABLE latest_calibration (id INTEGER PRIMARY KEY AUTOINCREMENT, result_name TEXT, value TEXT)')
connection.close()