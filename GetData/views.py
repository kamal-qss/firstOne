from django.shortcuts import render
from GetData.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from StagingData.settings import BASE_DIR
# from pyignite.datatypes.cache_config import CacheMode
# from pyignite.datatypes.prop_codes import *
# from socket import create_connection
# from pyignite.exceptions import SocketError
from pyignite import Client
import ssl

import json
import csv
from django.http import HttpResponse
from datetime import date, timedelta
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from pyignite.connection import Connection

import time
import datetime;
from array import *
from dateutil.relativedelta import relativedelta
#pg
import psycopg2
import base64

# from pyignite.api import (
# cache_get, cache_put, cache_get_or_create_with_config,
# )

# Create your views here.
@login_required(login_url='/UserApp/userlogin/')
def getData(request):
	value = 0
	loginUser = request.user
	eventD = Eventsdata.objects.all().order_by('-id')[:2000]
	page = request.GET.get('page', 1)
	paginator = Paginator(eventD, 50)

	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	return render(request,"GetData.html",{"contacts":contacts,"loginUser":loginUser,"value":value})

@login_required(login_url='/UserApp/userlogin/')
def eventBrief(request,val=None):
	# print(val)
	eventD = Eventsdata.objects.get(id=val)
	return render(request,"EventBrief.html",{"eventD":eventD})

@login_required(login_url='/UserApp/userlogin/')
def pythonignite(request):
	# print("Connection Pending!")
	loginUser = request.user
	nodes = [
 		('127.0.0.1', 10800),
 		('127.0.0.1', 10801),
	]
	# nodes = [
 # 		('35.154.247.92', 10800),
 # 		('35.154.247.92', 10801),
	# ]
	client = Client()
	client.connect(nodes)
	#QUERY = ''' SELECT * FROM PUBLIC.EVENTSDATA ORDER BY TIMESTAMP DESC LIMIT 2000; '''
	#QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA ORDER BY TIMESTAMP DESC LIMIT 2000; '''
	#QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM EVENTSDATA WHERE ID > (SELECT MAX(ID)-2000 FROM EVENTSDATA) ORDER BY "TIMESTAMP" DESC LIMIT 0,2000; '''
	QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE ID > (SELECT MAX(ID) FROM EVENTSDATA)-2000  ORDER BY ID DESC LIMIT 2000;  '''

	result = client.sql(
		QUERY,
		include_field_names=True,
	)
	print(next(result))
	eventsdata = []
	i = 0
	for row in result:
		# print(row)
		if i == 0:
			eventsdata.append({
				"ID":row[0],
				"APPID":row[1],
				"EVENTS":row[2],
				"DEVICE_ID":row[3],
				"TIMESTAMP":row[4],
				"MTIMESTAMP":row[5],
				"UPTIMESTAMP":row[6],
				"IPADDRESS":row[7],
				"CITY":row[8],
				"COUNTRY":row[9],
				"EVENTNAME":row[10],
				"CREATED_DATE":row[11],
				"CREATED_TIME":row[12],
			})
			i = 1
		else:		
			eventsdata.append({
				"ID": row[0],
				"APPID": row[1],
				"EVENTNAME": row[2],
				"CREATED_DATE": row[3],
				"CREATED_TIME": row[4],
				"EVENTS": row[5],
				"DEVICE_ID": row[6],
				"TIMESTAMP": row[7],
				"MTIMESTAMP": row[8],
				"UPTIMESTAMP": row[9],
				"IPADDRESS": row[10],
				"CITY": row[11],
				"COUNTRY": row[12],
				})

	# print("Connection Establish!")

	client.close()

	# Pagenation
	page = request.GET.get('page', 1)

	paginator = Paginator(eventsdata, 50)

	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	return render(request,"Pythonignite.html",{"contacts":contacts,"loginUser":loginUser})

@login_required(login_url='/UserApp/userlogin/')
def search_deviceid_postgres(request):
	value = 1
	if request.method=='GET':
		sdeviceid = request.GET.get('sdeviceid')
	# print(sdeviceid)
	loginUser = request.user
	eventD = Eventsdata.objects.filter(device_id=sdeviceid).order_by('-id')
	return render(request,"GetData.html",{"contacts":eventD,"loginUser":loginUser,"value":value,"sdeviceid":sdeviceid})

@login_required(login_url='/UserApp/userlogin/')
def search_deviceid_ignite(request):
	value = 1
	loginUser = request.user
	if request.method=='GET':
		sdeviceid = request.GET.get('sdeviceid')
	# print(sdeviceid)
	nodes = [
 		('127.0.0.1', 10800),
 		('127.0.0.1', 10801),
	]
	# nodes = [
 # 		('35.154.247.92', 10800),
 # 		('35.154.247.92', 10801),
	# ]
	client = Client()
	client.connect(nodes)
	QUERY = '''SELECT * FROM (SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE DEVICE_ID='{}' AND "TIMESTAMP"> '1575138600' LIMIT 0,500) AS t ORDER BY t.ID desc; '''.format(sdeviceid)
	result = client.sql(
		QUERY,
		include_field_names=True,
	)
	print(next(result))
	eventsdata = []
	i = 0
	for row in result:
		# print(row)
		if i == 0:
			eventsdata.append({
				"ID":row[0],
				"APPID":row[1],
				"EVENTS":row[2],
				"DEVICE_ID":row[3],
				"TIMESTAMP":row[4],
				"MTIMESTAMP":row[5],
				"UPTIMESTAMP":row[6],
				"IPADDRESS":row[7],
				"CITY":row[8],
				"COUNTRY":row[9],
				"EVENTNAME":row[10],
				"CREATED_DATE":row[11],
				"CREATED_TIME":row[12],
			})
			i = 1
		else:		
			eventsdata.append({
				"ID": row[0],
				"APPID": row[1],
				"EVENTNAME": row[2],
				"CREATED_DATE": row[3],
				"CREATED_TIME": row[4],
				"EVENTS": row[5],
				"DEVICE_ID": row[6],
				"TIMESTAMP": row[7],
				"MTIMESTAMP": row[8],
				"UPTIMESTAMP": row[9],
				"IPADDRESS": row[10],
				"CITY": row[11],
				"COUNTRY": row[12],
				})
	# print("Connection Establish!")
	client.close()
	return render(request,"Pythonignite.html",{"contacts":eventsdata,"loginUser":loginUser,"value":value,"sdeviceid":sdeviceid})

def export_users_csv(request):
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

	QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE APPID != '5def994ce96b09565e1f1ddd' AND CREATED_DATE = {} AND EVENTNAME!='_app_crash' AND ID!=855263 ORDER BY ID; '''.format("'"+datecsv+"'")
	
	print(QUERY)
	result = client.sql(
		QUERY,
		include_field_names=True,
	)

	print(next(result))

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(datecsv+"_IgniteEvents")
	writer = csv.writer(response)
	writer.writerow(['appid','deviceid','devicemodel','platform','apppackage','keyname','mobileoperator','app','song','album','pstate','source','ipaddress','city','station','duration','timestamp','to_char','created_time'])

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
			try:
				y = json.loads(x)
			except:
				pass
			if y.get("segmentation") is None:
				writer.writerow([row[1],row[6],y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),"","","","","",row[10],row[11],"","",row[7],row[3],row[4]])
			else:
				writer.writerow([row[1],row[6],y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),y.get("segmentation").get("Source"),row[10],row[11],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[7],row[3],row[4]])		

	client.close()
	return response


def export_Nielson_csv(request):
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

	QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE APPID = '5def994ce96b09565e1f1ddd' AND EVENTNAME!='_app_crash' ORDER BY ID; '''
	print(QUERY)
	result = client.sql(
		QUERY,
		include_field_names=True,
	)

	print(next(result))

	response = HttpResponse(content_type='text/csv')
	# response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(datecsv+"_IgniteEvents")
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format("NeilsonData")
	writer = csv.writer(response)
	writer.writerow(['appid','deviceid','devicemodel','platform','apppackage','keyname','mobileoperator','app','song','album','pstate','source','ipaddress','city','station','duration','timestamp','to_char','created_time'])

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
	return response

def queryresultalter(request):
	conn = psycopg2.connect(dbname="VTIONData",host= "vtionproddb.chgz4nqwpdta.ap-south-1.rds.amazonaws.com", user="vtion", password="per4mance")
	cur = conn.cursor()
	
	nodes = [
 		('35.154.247.92', 10800),
 		('35.154.247.92', 10801),
	]

	client = Client()
	client.connect(nodes)
	artist_name = ''
	genre = ''
	
	yesterday = "QueryRan"
	if request.method=='GET':
		'''squery = request.GET.get('squery')'''
		starttimestamp = request.GET.get('starttimestamp')
		endtimestamp = request.GET.get('endtimestamp')

	print("lol")
	QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE "TIMESTAMP" > '{}' AND "TIMESTAMP" < '{}' AND EVENTNAME!='_app_crash';'''.format(starttimestamp,endtimestamp)
	#QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE "TIMESTAMP" > '{}' AND "TIMESTAMP" < '{}' AND EVENTNAME='Register';'''.format(starttimestamp,endtimestamp)
	
	print(QUERY)
	result = client.sql(
		QUERY,
		include_field_names=True,
	)

	next(result)

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(yesterday+"_IgniteEvents")
	writer = csv.writer(response)
	writer.writerow(['appid','deviceid'	,'vtionid','devicemodel','platform','apppackage','keyname','mobileoperator','app','song','album','pstate','program','episode','source','ipaddress','city','station','duration','timestamp','to_char','created_time','artists', 'genre','education','ownership','nccs_code','age','gender','number', 'uninstall'])

	i = 0
	for row in result:
		nccs = age = gender = number = status = ''

		if i == 0:
			print(row)
			x = row[2]
			urlSafeEncodedBytes = base64.urlsafe_b64encode(row[3].encode("utf-8"))
			vtionid = str(urlSafeEncodedBytes, "utf-8")
			y = json.loads(x)
			if y.get("segmentation") is None:
				pass
				#writer.writerow([row[1],row[3],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[10],y.get("network").get("ope"),"","","","","","","",row[7],row[8],"","",row[4],row[11],row[12],"","",""])
			else:
				if row[10] == 'Video_Tuned' or row[10] == 'Video_off':
					song = y.get("segmentation").get("Song")
					try:
						if song:
							QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA WHERE TRACKNAME = '{}';'''.format(song)
							details = client.sql(
								QUERY,
								include_field_names=True,
							)
							print(next(details))
							for det in details:
								artist_name = det[0]
								genre = det[1]
							print("Testing with second table : ------------------------------------------------------//")
							if artist_name:
								pass
							else:
								QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA_ADD WHERE TRACKNAME = '{}';'''.format(song)
								details = client.sql(
									QUERY,
									include_field_names=True,
								)
								print(next(details))
								for det in details:
									artist_name = det[0]
									genre = det[1]
							writer.writerow([row[1],row[3],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[10],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),y.get("segmentation").get("Program"),y.get("segmentation").get("Episode"),y.get("segmentation").get("Source"),row[7],row[8],"",y.get("segmentation").get("Duration"),row[4],row[11],row[12], artist_name, genre,"","","","","","",""])
						else:
							pass
						
					
					except Exception as e:
						raise e
  
				elif row[10] == 'Audio_Off':
					pass
    
				else:
					song = y.get("segmentation").get("Song")
					education = y.get("segmentation").get("Highest Education")
					ownership = y.get("segmentation").get("Ownership")
					if ownership:
						try:
							print(ownership)
							print(education)
							own = ownership.split(',')
							print(len(own))
							if len(own) >= 9 :
								num_own = 9
							else :
								num_own = len(own)
							cur.execute('''SELECT nccs_code FROM public.nccs_flat where education = '{}' and ownership = '{}';'''.format(education,num_own))
							nccs = cur.fetchone()
							
							print("Found reply from postgres :", nccs[0])

						except Exception as e:
							print("query error")
					if row[10] == 'Register' or row[10] =='Profile':
						try:
							# cur.execute('''SELECT age, gender, number FROM public.installdata where deviceid = '{}';'''.format(row[3]))
							# data  = cur.fetchone()
							# age = data[0]
							# gender = data[1]
							# number = data[2]
							age =  y.get("segmentation").get("age")
							if age:
								pass
							else:
								age = y.get("segmentation").get("Age")

							gender = y.get("segmentation").get("Gender")
							if gender:
								pass
							else:
								gender = y.get("segmentation").get("gender")
							number = y.get("segmentation").get("Mobile Number")
							try:
								cur.execute('''SELECT i_status FROM public.appsflyer where number = '{}';'''.format(number))
								status_now  = cur.fetchone()
								status = status_now[0]
								if status == 'True':
									status = 'True'
								else:
									status = ''
								print("Status : -------------> ", status)
							except:
								pass
						except Exception as e:
							print("First case error :",e)
					try:
						if song:
							QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA WHERE TRACKNAME = '{}';'''.format(song)
							details = client.sql(
								QUERY,
								include_field_names=True,
							)
							next(details)
							# print(next(details))
							for det in details:
								artist_name = det[0]
								genre = det[1]
						print("lol its here")
						try:
							writer.writerow([row[1],row[3],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[10],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),"","",y.get("segmentation").get("Source"),row[7],row[8],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[4],row[11],row[12], artist_name, genre, education, ownership, nccs[0], age, gender, number, status])
						except Exception as e:
							print("first case : ",e)
							writer.writerow([row[1],row[3],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[10],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),"","",y.get("segmentation").get("Source"),row[7],row[8],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[4],row[11],row[12], artist_name, genre, education, ownership,'',age, gender, number,status])
					except Exception as e:
						print(e)
						pass
					
			i = 1
		else:
			print(row)
			x = row[5]
			#Encoder
			urlSafeEncodedBytes = base64.urlsafe_b64encode(row[6].encode("utf-8"))
			vtionid = str(urlSafeEncodedBytes, "utf-8")
			#Decoder
			# decodedBytes = base64.b64decode(urlSafeEncodedStr)
			# decodedStr = str(decodedBytes, "utf-8")
			# print("TYPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEee : ", type(row[6]))
			try:
				y = json.loads(x)
				if y.get("segmentation") is None:
					writer.writerow([row[1],row[6],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),"","","","","","","",row[10],row[11],"","",row[7],row[3],row[4],"",""])
				else:
					if row[2] == 'Video_Tuned' or row[2] == 'Video_off':
						song = y.get("segmentation").get("Song")
						try:
							if song:
								QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA WHERE TRACKNAME = '{}';'''.format(song)
								details = client.sql(
									QUERY,
									include_field_names=True,
								)
								next(details)
								# print(next(details))
								for det in details:
									artist_name = det[0]
									genre = det[1]
								writer.writerow([row[1],row[6],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),y.get("segmentation").get("Program"),y.get("segmentation").get("Episode"),y.get("segmentation").get("Source"),row[10],row[11],"",y.get("segmentation").get("Duration"),row[7],row[3],row[4], artist_name, genre,"","",""])
							else:
								pass
							
							
						except Exception as e:
							pass
					
					elif row[2] == 'Audio_Off':
						pass
						

					else:
						song = y.get("segmentation").get("Song")
						education = y.get("segmentation").get("Highest Education")
						ownership = y.get("segmentation").get("Ownership")
						
						if ownership:
							try:
								own = ownership.split(',')
								if len(own) >= 9 :
									num_own = 9
								else :
									num_own = len(own)	
								cur.execute('''SELECT nccs_code FROM public.nccs_flat where education = '{}' and ownership = '{}';'''.format(education,num_own))
								nccs = cur.fetchone()
								print("Found reply from postgres :", nccs[0])
							except Exception as e:
								print("query error")
						if row[2] == 'Register' or row[2] =='Profile':
							try:
								# cur.execute('''SELECT age, gender, number FROM public.installdata where deviceid = '{}';'''.format(row[6]))
								# data  = cur.fetchone()
								# age = data[0]
								# gender = data[1]
								# number = data[2]
								age =  y.get("segmentation").get("Age")
								if age :
									pass
								else:
									age = y.get("segmentation").get("age")
								gender = y.get("segmentation").get("Gender")
								if gender:
									pass
								else:
									gender = y.get("segmentation").get("gender")
								number = y.get("segmentation").get("Mobile Number")
								try:
									cur.execute('''SELECT i_status FROM public.appsflyer where number = '{}';'''.format(number))
									status_now  = cur.fetchone()
									status = status_now[0]
								except:
									pass
							except Exception as e:
								print(e)
						
						try:
							if song:
								QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA WHERE TRACKNAME = '{}';'''.format(song)
								details = client.sql(
									QUERY,
									include_field_names=True,
								)
								next(details)
								# print(next(details))
								for det in details:
									artist_name = det[0]
									genre = det[1]
								if artist_name:
										pass
								else:
									QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA_ADD WHERE TRACKNAME = '{}';'''.format(song)
									details = client.sql(
										QUERY,
										include_field_names=True,
									)
									print(next(details))
									for det in details:
										artist_name = det[0]
										genre = det[1]
							
       
							try:
								writer.writerow([row[1],row[6],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),"","",y.get("segmentation").get("Source"),row[10],row[11],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[7],row[3],row[4], artist_name, genre, education, ownership, nccs[0], age, gender, number, status])
							except Exception as e:
								print("Second case :",e)
								writer.writerow([row[1],row[6],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),y.get("segmentation").get("App"),y.get("segmentation").get("Song"),y.get("segmentation").get("Album"),y.get("segmentation").get("PState"),"","",y.get("segmentation").get("Source"),row[10],row[11],y.get("segmentation").get("Station"),y.get("segmentation").get("Duration"),row[7],row[3],row[4], artist_name, genre, education, ownership, '', age, gender, number, status])
							
						except Exception as e:
							print("passed without writing main  : ",e)
							pass
						

			except Exception as e:
				pass
			

	client.close()
	return response

@login_required(login_url='/UserApp/userlogin/')
def drawgraph(request):
	loginUser = request.user
	# es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
	es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
	today = str(datetime.date.today())
	new_date = today[5:7]+"/"+today[8:10]+"/"+today[0:4]
	list_data = es.search(index="radio_kpi", body={"query": {"match_all": {}}})["hits"]["hits"]
	print(list_data)
	x = []
	for item in list_data:
		x.append(item["_source"])
		print(item["_source"])
	print(x)

	return render(request,"EventsDetails.html",{"data":x,"loginUser":loginUser})

class CreateChart(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		# es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}]) //changed by kamal
		es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
		today = str(datetime.date.today())
		new_date = today[5:7]+"/"+today[8:10]+"/"+today[0:4]
		list_data = es.search(index="radio_kpi", 
		body = {
				"from" : 0, "size" : 7,
				
				"sort": [{
					"tuned_date.keyword": {
					"order": "desc"
					}
					}],
				"query": {
				"range": {
					"tuned_date.keyword": {
					"lte": new_date
					}
				}
			}
		}
		)["hits"]["hits"]
		
		# print(list_data)
		labeldates = []
		labelcount = []
		for item in list_data:
			labeldates.append(item["_source"]["tuned_date"])
			labelcount.append(item["_source"]["count"])
			# print(item["_source"])
		# print(labeldates)
		# 
		# print(labelcount)
		colour = [
	                'rgba(25, 255, 122, 0.2)',
	                'rgba(25, 255, 122, 0.2)',
	                'rgba(25, 255, 122, 0.2)',
	                'rgba(25, 255, 122, 0.2)',
	                'rgba(25, 255, 122, 0.2)',
	                'rgba(25, 255, 122, 0.2)',
	                'rgba(25, 255, 122, 0.2)',
	            	]
		data = {
			"labeldates":labeldates,
			"labelcount":labelcount,
			"colour":colour
		}
		return Response(data)


class CreateChartAudio(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		# es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
		es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
		today = str(datetime.date.today())
		new_date = today[5:7]+"/"+today[8:10]+"/"+today[0:4]
		list_data = es.search(index="audio_kpi", 
		body = {
				"from" : 0, "size" : 7,
				
				"sort": [{
					"tuned_date.keyword": {
					"order": "desc"
					}
					}],
				"query": {
				"range": {
					"tuned_date.keyword": {
					"lte": new_date
					}
				}
			}
		}
		)["hits"]["hits"]
		
		# print(list_data)
		labeldates = []
		labelcount = []
		for item in list_data:
			labeldates.append(item["_source"]["tuned_date"])
			labelcount.append(item["_source"]["count"])
			# print(item["_source"])
		# print(labeldates)
		# print(labelcount)
		print("kamal going right")
		[print(ll) for ll in labelcount]
		[print(zoo) for zoo in labeldates]
		colour = [
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	            	]
		data = {
			"labeldates":labeldates,
			"labelcount":labelcount,
			"colour":colour
		}
		return Response(data)

"""def drawgraphpie(request):
	loginUser = request.user
	es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

	arr = [[0],[0,0],[0,0,0],[0,0,0,0],[0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0,0]]
	print(arr)

	currentdate = int(datetime.datetime.now().timestamp())
	print(currentdate)
	enddate = date.today()
	enddate = int((time.mktime(enddate.timetuple()))-19800)
	startdate = date.today() - timedelta(days=7) - timedelta(hours=5, minutes=30)
	startdate = int((time.mktime(startdate.timetuple()))-19800)

	list_data = es.search(index="installed_data", body= {"query": {"range": {"install_date_ts": {"gte": startdate,"lte": enddate}}},})["hits"]["hits"]
	for item in list_data:
		print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
		x = item
		device_id = x["_source"]['device_id']
		day = x["_source"]['install_date_ts']
		daya = x["_source"]['install_date']
		diff = currentdate - day
		diff = int(diff/86400)
		print(diff)
		print(device_id)
		print(daya)
		i = diff
		j = 1
		while i > 0:
			try:
				queryDate = ((date.today() - timedelta(days=i)).strftime('%m/%d/%Y'))
				print("Query Date {}".format(queryDate))
				listinside = es.search(index="tunedondata", body= {"query": {"bool": { "must" : [{"match_phrase": {"tuned_date" : queryDate }},{"match_phrase":{"device_id" : device_id }}]},}})["hits"]["hits"]
				k = 0
				for itemin in listinside:
					tuned  = listinside[k]["_source"]["tuned_date"]
					print(tuned)
					if tuned == queryDate:
						print("saving at {},{}".format(diff,j))
						arr[diff-1][j-1] = arr[diff-1][j-1] + 1
						k = k + 1
			except Exception as e:
				pass
				# print(" data not found !! at {},{}".format(diff,j))
				# arr[diff][j] = 0
			i = i - 1
			j = j + 1
			print(arr)
	print(arr)

	datearray = [0,0,0,0,0,0,0]
	itr = 7
	while itr > 0 :
		datetopaste = date.today() - timedelta(days=itr) - timedelta(hours=5, minutes=30)
		# print(datetopaste)
		datearray[6-itr+1] = str(datetopaste)
		itr = itr - 1
	# print(datearray)

	i = 7
	datalabel = []
	datacount = []
	while i >= 0:
		beforethirty = datetime.datetime.now() - relativedelta(days=i)
		date_formated = beforethirty.strftime("%m%d%Y")
		strid = "date_"+date_formated
		print(strid)
		try:
			truecount = es.search(index="fm_competingapp_true",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["truecount"]
		except Exception as e:
			truecount = 0
		try:
			falsecount = es.search(index="fm_competingapp_false",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["falsecount"]	
		except Exception as e:
			falsecount = 0
		try:
			nomatchcount = es.search(index="fm_competingapp_nomatch",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["nomatchcount"]	
		except Exception as e:
			nomatchcount = 0
		
		count = truecount + falsecount + nomatchcount
		datalabel.append(strid)
		datacount.append(count)
		print(count)
		# print(i)
		i = i - 1
	datanew = {
		"datalabel":datalabel,
		"datacount":datacount,
	}
	print(datanew)
	return render(request,"Notification_FMCompeting.html",{"data":"Hello","loginUser":loginUser,"dataarray":arr,"dates":datearray,"datacount":datacount})
"""
@login_required(login_url='/UserApp/userlogin/')
def drawgraphpie(request):
	loginUser = request.user
	es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

	arr = [[0],[0,0],[0,0,0],[0,0,0,0],[0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
	# print(arr)
	currentdate = date.today() + timedelta(days=1) - timedelta(hours=5, minutes=30) 
	currentdate = int((time.mktime(currentdate.timetuple()))-19800)
	# print(currentdate)
	enddate = date.today()
	enddate = int((time.mktime(enddate.timetuple()))-19800)
	print("EndDate :{}".format(enddate))
	startdate = date.today() - timedelta(days=8) - timedelta(hours=5, minutes=30)
	startdate = int((time.mktime(startdate.timetuple()))-19800)
	print("startdate :{}".format(startdate))

	list_data = es.search(index="installed_data", body= {"query": {"range": {"install_date_ts": {"gte": startdate,"lte": enddate}}},},size=10000)["hits"]["hits"]
	for item in list_data:
		x = item
		device_id = x["_source"]['device_id']
		day = x["_source"]['install_date_ts']
		daya = x["_source"]['install_date']
		diff = enddate - day
		print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print(diff)
		diff = int(diff/86400)
		print("DIff: {}".format(diff))
		print("device_id: {} ,install_date: {}".format(device_id,daya))
		i = diff + 1
		j = 1
		while i > 0:
			try:
				queryDate = ((date.today() - timedelta(days=i)).strftime('%m/%d/%Y'))
				print("Query Date {}".format(queryDate))
				listinside = es.search(index="tunedondata", body= {"query": {"bool": { "must" : [{"match_phrase": {"tuned_date" : queryDate }},{"match_phrase":{"device_id" : device_id }}]},}})["hits"]["hits"]
				k = 0
				for itemin in listinside:
					tuned  = listinside[k]["_source"]["tuned_date"]
					print(tuned)
					if tuned == queryDate:
						print("saving at {},{}".format(diff,j-1))
						# arr[diff-1][j-1] = arr[diff-1][j-1] + 1
						arr[diff][j-1] = arr[diff][j-1] + 1
						k = k + 1
						print(arr)
			except Exception as e:
				pass
			i = i - 1
			j = j + 1
			# print(arr)
	# print(arr)

	datearray = [0,0,0,0,0,0,0]
	itr = 7
	while itr > 0 :
		datetopaste = date.today() - timedelta(days=itr) - timedelta(hours=5, minutes=30)
		# print(datetopaste)
		datearray[6-itr+1] = str(datetopaste)
		itr = itr - 1
	# print(datearray)

	i = 7
	datalabel = []
	datacount = []
	while i >= 0:
		beforethirty = datetime.datetime.now() - relativedelta(days=i)
		date_formated = beforethirty.strftime("%m%d%Y")
		strid = "date_"+date_formated
		print(strid)
		try:
			truecount = es.search(index="fm_competingapp_true",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["truecount"]
		except Exception as e:
			truecount = 0
		try:
			falsecount = es.search(index="fm_competingapp_false",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["falsecount"]	
		except Exception as e:
			falsecount = 0
		try:
			nomatchcount = es.search(index="fm_competingapp_nomatch",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["nomatchcount"]	
		except Exception as e:
			nomatchcount = 0
		
		count = truecount + falsecount + nomatchcount
		datalabel.append(strid)
		datacount.append(count)
		print(count)
		# print(i)
		i = i - 1
	datanew = {
		"datalabel":datalabel,
		"datacount":datacount,
	}
	print(datanew)
	return render(request,"Notification_FMCompeting.html",{"data":"Hello","loginUser":loginUser,"dataarray":arr,"dates":datearray,"datacount":datacount,"chartfor":"0"})

@login_required(login_url='/UserApp/userlogin/')
def drawgraphcohortFM(request):
	loginUser = request.user
	es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

	arr = [[0],[0,0],[0,0,0],[0,0,0,0],[0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
	# print(arr)
	currentdate = date.today() + timedelta(days=1) - timedelta(hours=5, minutes=30) 
	currentdate = int((time.mktime(currentdate.timetuple()))-19800)
	# print(currentdate)
	enddate = date.today()
	enddate = int((time.mktime(enddate.timetuple()))-19800)
	print("EndDate :{}".format(enddate))
	startdate = date.today() - timedelta(days=8) - timedelta(hours=5, minutes=30)
	startdate = int((time.mktime(startdate.timetuple()))-19800)
	print("startdate :{}".format(startdate))

	list_data = es.search(index="installed_data", body= {"query": {"range": {"install_date_ts": {"gte": startdate,"lte": enddate}}},},size=10000)["hits"]["hits"]
	for item in list_data:
		x = item
		device_id = x["_source"]['device_id']
		day = x["_source"]['install_date_ts']
		daya = x["_source"]['install_date']
		diff = enddate - day
		print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
		print(diff)
		diff = int(diff/86400)
		print("DIff: {}".format(diff))
		print("device_id: {} ,install_date: {}".format(device_id,daya))
		i = diff + 1
		j = 1
		while i > 0:
			try:
				queryDate = ((date.today() - timedelta(days=i)).strftime('%m/%d/%Y'))
				print("Query Date {}".format(queryDate))
				listinside = es.search(index="fmondata", body= {"query": {"bool": { "must" : [{"match_phrase": {"tuned_date" : queryDate }},{"match_phrase":{"device_id" : device_id }}]},}})["hits"]["hits"]
				k = 0
				for itemin in listinside:
					tuned  = listinside[k]["_source"]["tuned_date"]
					print(tuned)
					if tuned == queryDate:
						print("saving at {},{}".format(diff,j-1))
						# arr[diff-1][j-1] = arr[diff-1][j-1] + 1
						arr[diff][j-1] = arr[diff][j-1] + 1
						k = k + 1
						print(arr)
			except Exception as e:
				pass
			i = i - 1
			j = j + 1
			# print(arr)
	# print(arr)

	datearray = [0,0,0,0,0,0,0]
	itr = 7
	while itr > 0 :
		datetopaste = date.today() - timedelta(days=itr) - timedelta(hours=5, minutes=30)
		# print(datetopaste)
		datearray[6-itr+1] = str(datetopaste)
		itr = itr - 1
	# print(datearray)

	i = 7
	datalabel = []
	datacount = []
	while i >= 0:
		beforethirty = datetime.datetime.now() - relativedelta(days=i)
		date_formated = beforethirty.strftime("%m%d%Y")
		strid = "date_"+date_formated
		print(strid)
		try:
			truecount = es.search(index="fm_competingapp_true",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["truecount"]
		except Exception as e:
			truecount = 0
		try:
			falsecount = es.search(index="fm_competingapp_false",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["falsecount"]	
		except Exception as e:
			falsecount = 0
		try:
			nomatchcount = es.search(index="fm_competingapp_nomatch",body={"query": {"match": {"id" : strid}}})["hits"]["hits"][0]["_source"]["nomatchcount"]	
		except Exception as e:
			nomatchcount = 0
		
		count = truecount + falsecount + nomatchcount
		datalabel.append(strid)
		datacount.append(count)
		print(count)
		# print(i)
		i = i - 1
	datanew = {
		"datalabel":datalabel,
		"datacount":datacount,
	}
	print(datanew)
	return render(request,"Notification_FMCompeting.html",{"data":"Hello","loginUser":loginUser,"dataarray":arr,"dates":datearray,"datacount":datacount,"chartfor":1})

def showpyscript(request):
	loginUser = request.user
	
	return render(request,"ShowPyscript.html",{"loginUser":loginUser})

@login_required(login_url='/UserApp/userlogin/')
def artistMaster(request):
	loginUser = request.user
	nodes = [
 		('127.0.0.1', 10800),
 		('127.0.0.1', 10801),
	]

	client = Client()
	client.connect(nodes)

	#QUERY = ''' SELECT ID, TRACKID, TRACKDATA FROM PUBLIC.SONG_DATA ORDER BY ID DESC; '''
	QUERY = ''' SELECT TRACKNAME, ALBUMNAME, ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA ORDER BY ID DESC; '''
	#print(QUERY)
	result = client.sql(
		QUERY,
	)

	datatohtml = []
	'''for row in result:
		try:
			dataparsed = json.loads(row[2])
			try:
				genre = dataparsed.get("primary_genres").get("music_genre_list")[0].get("music_genre").get("music_genre_name")
			except Exception as e:
				genre = "-"
			dataauto ={
			"track_name":dataparsed.get("track_name"),
			"artist_name":dataparsed.get("artist_name"),
			"album_name":dataparsed.get("album_name"),
			"genre":genre
			}
			datatohtml.append(dataauto)
		except Exception as e:
			pass

	# print(datatohtml)'''
	for row in result:
		dataauto = {
			"track_name":row[0],
			"artist_name":row[2],
			"album_name":row[1],
			"genre":row[3],
		}
		datatohtml.append(dataauto)
	return render(request,"ArtistMaster.html",{"loginUser":loginUser,"datatohtml":datatohtml})

def exportPaytmRewards(request):

	es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
	listinside = es.search(index="rewardspaytm", body= {"query": {"match_phrase": {"status": 0}}},size=10000)["hits"]["hits"]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format("PaytmRewards")
	writer = csv.writer(response)
	writer.writerow(['deviceid','contactnumber','status'])

	i = 0
	for row in listinside:
		print(row.get("_source"))
		try:
			deviceid = row.get("_source").get("deviceid")
			contactnumber = row.get("_source").get("contactnumber")
			status = row.get("_source").get("status")
			timestamp = row.get("_source").get("timestamp")
			writer.writerow([deviceid,contactnumber,status])
			doc = {
				"contactnumber" : contactnumber,
				"deviceid" : deviceid,
				"status" : 1,
				"timestamp":timestamp
			}
			res = es.index(index="rewardspaytm", doc_type='dataone', id=deviceid ,body=doc)
			print(res['result'])	

		except Exception as e:
			print(e)
			pass
	return response


