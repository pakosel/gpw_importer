import pandas as pd
from datetime import timedelta, date
import psycopg2
import config as cfg
#import locale
#locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
baseUrl = r'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date='
max=cfg.max_rows_import
#print stocks.head(max)

start_date = cfg.start_date
end_date = cfg.end_date

try:
	connection = psycopg2.connect(user=cfg.db['user'],password=cfg.db['pass'],host=cfg.db['host'],port=cfg.db['port'],database=cfg.db['database'])
	cursor = connection.cursor()
	postgres_insert_query = """ INSERT INTO quotes (name, date, price) VALUES (%s,%s,%s)"""
	d = start_date
	delta = timedelta(days=1)
	while d <= end_date:
		tempd = d
		dStr = d.strftime("%d-%m-%Y")
		d += delta
		url = baseUrl + dStr
		tables = pd.read_html(url, decimal=',', thousands=u'\xa0')
		if len(tables) < 2:
			continue
		print dStr + ' imported successfully'
		stocks = tables[1]
		cnt = 0;
		for i, row in stocks.iterrows():
			v = float(row[2])
#			print(row[0], row[2], v)
			record_to_insert = (row[0], tempd, row[2])
			cursor.execute(postgres_insert_query, record_to_insert)
			cnt = cnt+1
			if cnt == max:
				break
	connection.commit()
	count = cursor.rowcount
	
except (Exception, psycopg2.Error) as error :
	if(connection):
		print("Failed to insert record into mobile table", error)
finally:
	if(connection):
		cursor.close()
		connection.close()
