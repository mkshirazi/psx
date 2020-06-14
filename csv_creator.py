import requests
import scrapy
import pandas as pd
import datetime
from datetime import timedelta, date
from scrapy import Selector

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = '2020-01-01'
end_date = '2020-06-14'
start_date_ = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
end_date_ = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()


url = "https://dps.psx.com.pk/historical"
payload = 'date='+ str(start_date)
headers = {
  'Accept': 'text/html, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

response = requests.request("POST", url, headers=headers, data = payload)

#print(response.text.encode('utf8'))

table_html = response.text.encode('utf8')
sel = Selector(text=table_html)

headings = sel.css('div>table>thead>tr ::text').extract()
records = len(sel.css('div>table>tbody>tr').extract())
a =[]
if records > 0:
	for i in range(1,records+1):
		a.append(sel.css('div>table>tbody>tr:nth-of-type('+ str(i) + ') td ::text').extract())
	df = pd.DataFrame(a,columns=headings)
	df["DATE"] = start_date_
else:
	df = pd.DataFrame(columns=headings)
	df["DATE"] = start_date_

for date in daterange(start_date_ + timedelta(1),end_date_):
	payload = 'date='+ str(date)
	response = requests.request("POST", url, headers=headers, data = payload)
	sel = Selector(text=response.text.encode('utf8'))
	n_records = len(sel.css('div>table>tbody>tr').extract())
	if n_records > 0:
		a =[]
		for i in range(1,records+1):
			a.append(sel.css('div>table>tbody>tr:nth-of-type('+ str(i) + ') td ::text').extract())
		temp = pd.DataFrame(a,columns=headings)
		temp["DATE"] = date
		df = df.append(temp)

df = df.set_index(['DATE','SYMBOL'])
df = df.dropna()	
df.to_csv("/mnt/d/example_psx.csv")
print(df)