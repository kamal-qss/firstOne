from django.shortcuts import render
from django.core.paginator import Paginator
import ssl
import json
import csv
from django.http import HttpResponse
from datetime import date, timedelta
import time
import datetime
from django.core.mail import EmailMessage
import os
import glob
from xlsxwriter.workbook import Workbook
from django.http import HttpResponseRedirect
from pyignite import Client
from elasticsearch import Elasticsearch,helpers


def queryresultalter():
	# es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
	es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])

	yesterday = "QueryRan"
	# print(yesterday)
	startdate = date.today() - timedelta(days=7) - timedelta(hours=5, minutes=30)
	startdate = int((time.mktime(startdate.timetuple()))-19800)
	# print("startdate :{}".format(startdate))
	enddate = date.today()
	enddate = int((time.mktime(enddate.timetuple()))-19800)
	# print("EndDate :{}".format(enddate))


	# Migration job
	nodes = [
 		('35.154.247.92', 10800),
 		('35.154.247.92', 10801),
	]

	client = Client()
	client.connect(nodes)

	QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE "TIMESTAMP" >= '{}' AND "TIMESTAMP" <= '{}' AND EVENTNAME!='_app_crash'; '''.format(startdate,enddate)
	print(QUERY)
	result = client.sql(
		QUERY,
		include_field_names=True,
	)
	print(next(result))
	i = 0

	for row in result:
		if i == 0:
			str_id = str(row[3]) + str(row[4])
			print(str_id)
			eventdetails = row[2]
			y = json.loads(eventdetails)
			doc = {
				"id" : row[0],
				"uptimestamp" : row[6],
				"city" : row[8],
				"device_id" : row[3],
				"created_time" : row[12],
				"timestamp" : row[4],
				"created_date" : row[11],
				"country" : row[9],
				"mtimestamp" : row[5],
				"ipAddress" : row[7],
				"app_id" : row[1],
				"events" : y,
				"key" : row[10]
	        }
		else:
			str_id = str(row[6]) + str(row[7])
			print(str_id)
			eventdetails = row[5]
			y = json.loads(eventdetails)
			doc = {
				"id" : row[0],
				"uptimestamp" : row[9],
				"city" : row[11],
				"device_id" : row[6],
				"created_time" : row[4],
				"timestamp" : row[7],
				"created_date" : row[3],
				"country" : row[12],
				"mtimestamp" : row[8],
				"ipAddress" : row[10],
				"app_id" : row[1],
				"events" : y,
				"key" : row[2]
	        }

		# save the data to es
		res = es.index(index="tendays", doc_type='eventdetails',id=str_id, body=doc)
		print(res['result'])	
		i = i + 1
	print(i)

queryresultalter()


