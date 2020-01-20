
from django.shortcuts import render
from django.core.paginator import Paginator
from pyignite import Client
import ssl
import json
import csv
from django.http import HttpResponse
from datetime import date, timedelta
from django.core.mail import EmailMessage
import os
from django.http import HttpResponseRedirect

def export_users_csv():
	print("Hello")
	nodes = [
 		('127.0.0.1', 10800),
 		('127.0.0.1', 10801),
	]

	client = Client()
	client.connect(nodes)

	yesterday = date.today() - timedelta(days=1)
	datecsv = yesterday.strftime('%m/%d/%Y')
	print(datecsv)

	QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE APPID != '5def994ce96b09565e1f1ddd' AND CREATED_DATE = {} AND EVENTNAME!='_app_crash' AND ID!=735550 ORDER BY ID; '''.format("'"+datecsv+"'")
	print(QUERY)
	result = client.sql(
		QUERY,
		include_field_names=True,
	)

	print(next(result))

	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	print(BASE_DIR)

	namespac = BASE_DIR + str("/target/Data_"+yesterday.strftime('%m_%d_%Y')+'.csv')
	print(type(namespac))
	with open(namespac, 'w+') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerow(['appid','DeviceId','deviceModel','platform','apppackage','keyname','mobileOperator','app','song','album','Pstate','Source','ipaddress','city','station','duration','timestamp','created_date','created_time'])

		i = 0
		for row in result:
			if i == 0:
				print(row)
				x = row[2]
				y = json.loads(x)
				if y.get("segmentation") is None:
					writer.writerow([row[1],row[3],y.get("d"),y.get("p"),y.get("ap"),row[10],y.get("network").get("ope"),"","","","","",row[7],row[8],"","",row[4],row[11],row[12]])
				else:
					writer.writerow([row[1],row[3],y.get("d"),y.get("p"),y.get("ap"),row[10],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),y.get("segmentation").get("Source"),row[7],row[8],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[4],row[11],row[12]])
				i = 1
			else:
				print(row)
				x = row[5]
				y = json.loads(x)
				if y.get("segmentation") is None:
					writer.writerow([row[1],row[6],y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),"","","","","",row[10],row[11],"","",row[7],row[3],row[4]])
				else:
					writer.writerow([row[1],row[6],y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),y.get("segmentation").get("Source"),row[10],row[11],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[7],row[3],row[4]])		

	client.close()
	writeFile.close()

export_users_csv()

