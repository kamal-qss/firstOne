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
	es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])

	yesterday = "QueryRan"
	# print(yesterday)
	startdate = date.today() - timedelta(days=7) - timedelta(hours=5, minutes=30)
	startdate = int((time.mktime(startdate.timetuple()))-19800)
	print("Startdate :{}".format(startdate))
	enddate = date.today()
	enddate = int((time.mktime(enddate.timetuple()))-19800)
	print("EndDate :{}".format(enddate))
	
	# Make a excel sheet store the headers Only
	workbook = Workbook('Data_QueryRan.xlsx')
	worksheet = workbook.add_worksheet()
	lista = ['appid','deviceid','devicemake','devicemodel','platform','apppackage','keyname','mobileoperator','ssid','app','song','album'
	,'pstate','source','ipaddress','city','station','duration','timestamp','created_date','created_time']

	r = 0
	c = 0
	for item in lista:
		worksheet.write(r, c, item)
		c = c + 1

	# Query the elasticsearch cluster 
	i=0
	results = helpers.scan(client = es,
                    scroll = '2m',
                    query = {"query": {"range": {"timestamp": {"gte": startdate,"lte": enddate}}}}, 
                    index = "tendays")
	for item in results:
		dataJson = item["_source"]
		data_appid = dataJson["app_id"]
		data_deviceid = dataJson["device_id"]
		data_devicemake = '"'+dataJson["events"]["ma"]+'"'
		data_devicemodel = '"'+dataJson["events"]["d"]+'"'
		data_platform = '"'+dataJson["events"]["p"]+'"'
		data_apppackage = '"'+dataJson["events"]["ap"]+'"'
		try:
			data_keyname = '"'+dataJson["key"]+'"'
		except Exception as e:
			data_keyname = ""
		data_mobileoperator = '"'+dataJson["events"]["network"]["ope"]+'"'
		data_ssid = '"'+dataJson["events"]["network"]["ssid"]+'"'
		try:
			data_App = '"'+dataJson["events"]["segmentation"]["App"]+'"'
		except Exception as e:
			data_App = ""
		
		try:
			data_Song = '"'+dataJson["events"]["segmentation"]["Song"]+'"'
		except Exception as e:
			data_Song = ""
		
		try:
			data_Album = '"'+dataJson["events"]["segmentation"]["Album"]+'"'
		except Exception as e:
			data_Album = ""
		
		try:
			data_PState = '"'+dataJson["events"]["segmentation"]["PState"]+'"'
		except Exception as e:
			data_PState = ""
		try:
			data_Source = '"'+dataJson["events"]["segmentation"]["Source"]+'"'
		except Exception as e:
			data_Source = ""
		data_ipAddress = dataJson["ipAddress"]
		data_city = dataJson["city"]
		try:
			data_station = '"'+dataJson["events"]["segmentation"]["Station"]+'"'
		except Exception as e:
			data_station = ""
		try:
			data_duration = '"'+dataJson["events"]["segmentation"]["Duration"]+'"'
		except Exception as e:
			data_duration = ""
		
		data_timestamp = dataJson["timestamp"]
		data_created_date = dataJson["created_date"]
		data_created_time = dataJson["created_time"]

		lista = [data_appid,data_deviceid,data_devicemake,data_devicemodel,data_platform,data_apppackage,data_keyname,data_mobileoperator,data_ssid,data_App,data_Song,data_Album,data_PState,data_Source,data_ipAddress,data_city,data_station,data_duration,data_timestamp,data_created_date,data_created_time]
		r =r + 1
		c = 0
		for item in lista:
			worksheet.write(r, c, item)
			c = c + 1
		i=i+1
	print("Value of i:{}".format(i))
	workbook.close()

queryresultalter()

