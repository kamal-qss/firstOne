from datetime import date, timedelta
import time
import datetime
from elasticsearch import Elasticsearch,helpers
import json
import requests
from pyignite import Client

def removesmall(data):
	return data.split("(")[0]

def removebig(data):
	return data.split("[")[0]

def artistgenre():
	api_token = '905748e88e234954c9849597855d2d57'
	api_url_base = 'http://api.musixmatch.com/ws/1.1/track.search'
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer {0}'.format(api_token)}

	# es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])

	# nodes = [
 	# 	('127.0.0.1', 10800),
 	# 	('127.0.0.1', 10801),
	# ]
	nodes = [('35.154.247.92', 10800), ('35.154.247.92', 10801)]
	val = str(date.today()- timedelta(days=1)).split("-")
	datelast = val[1]+'/'+val[2]+'/'+val[0]
	# print(datelast)
	# datelast = '07/20/2019'
	# res = es.search(size=2000,index="tendays", body= {"query": {
	# 	"bool": {
	# 	  "must": [
	# 	    {"match_phrase": {
	# 	      "created_date.keyword": datelast
	# 	    }},
	# 	    {"match_phrase": {
	# 	      "events.key.keyword": "Audio_Tuned"
	# 	    }}
	# 	  ]
	# 	}
	# }})
	# es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
	#datelast = '09/18/2019' 
	es = Elasticsearch([{'host': '13.235.1.36', 'port': 9200}])
	body =\
		{
		"query": {
			"bool": {
			"must": [
				{"match_phrase": {
				"created_date.keyword": datelast
				}},
				{"match_phrase": {
				"events.key.keyword": "Audio_Tuned"
				}}
			]
			}
		}
		}
	res = es.search(index='tendays', body=body, size=10000)
	print(res)

	client = Client()
	client.connect(nodes)
	i = 0
	for item in res["hits"]["hits"]:
		i = i + 1
		try:
			d = removesmall(item["_source"]["events"]["segmentation"]["Song"])
			d = removebig(d)
			
			print(d)
			QUERY = ''' SELECT ID FROM PUBLIC.SONG_DATA Where TRACKNAME = '{}'; '''.format(d)
			result = client.sql(QUERY)
			ignite = []
			for trackid in result:
				ignite.append(trackid)
				
			if ignite:
				
				print("Song already present in 1st table :", d)
				print("Track ID ===========================:", ignite)
				pass
			else:
				# d = 'Touch the Floor (feat. Masego)'
				try:
					QUERY = '''SELECT ID FROM PUBLIC.SONG_DATA_ADD Where VSONG = '{}'; '''.format(d)
					print("CHECKING of second table query : ", QUERY)
					result = client.sql(QUERY)
					print("reached herer..............................")
					# print(next(result))
				except Exception as e:
					print(e)
				print("outside the vla")
				ignite_add = []
				for trackid in result:
					print("############################################")
					print(trackid[0])
					ignite_add.append(trackid[0])
					
				if ignite_add:
					print("Song 2nd table:", d)
					print("Track ID =======================  C:", ignite_add)
					pass
				else:
					print("api call")
					api_url = '{0}?q_track={1}&page_size=1&page=1&s_track_rating=desc&apikey=905748e88e234954c9849597855d2d57'.format(api_url_base,d)
					response = requests.get(api_url, headers=headers)
					print(response)
					if response.status_code == 200:
						track_data = str(response.content)
						print(track_data)
						track_data = track_data[:1] + '"' + track_data[2:]
						track_data = track_data[:-2] + '"'
						# print(track_data)
						
						track_id = json.loads(response.content.decode('utf-8'))["message"]["body"]["track_list"][0]["track"]["track_id"]

						track_name = json.loads(response.content.decode('utf-8'))["message"]["body"]["track_list"][0]["track"]["track_name"]
						track_name = track_name.replace("'","\\'")
						
						album_name = json.loads(response.content.decode('utf-8'))["message"]["body"]["track_list"][0]["track"]["album_name"]
						album_name = album_name.replace("'","\\'")

						artist_name = json.loads(response.content.decode('utf-8'))["message"]["body"]["track_list"][0]["track"]["artist_name"]
						artist_name = artist_name.replace("'","\\'")

						try:
							genre = json.loads(response.content.decode('utf-8'))["message"]["body"]["track_list"][0]["track"]["primary_genres"]["music_genre_list"][0]["music_genre"]["music_genre_name"]
						except Exception as e:
							genre = "-"
						
						QUERY = ''' SELECT MAX(ID) FROM PUBLIC.SONG_DATA; '''
						re = client.sql(
							QUERY,
							include_field_names=True,
						)
						print(next(re))
						sqlId = next(re)[0] + 1
						print("SQL ID ASSIGNED : ", sqlId)
						INS_QUERY = """INSERT INTO PUBLIC.SONG_DATA (ID, TRACKID, TRACKDATA, TRACKNAME, ALBUMNAME, ARTISTNAME, GENRE, STATUS) VALUES({sqlId}, {trackid}, '{track_data}', '{track_name}', '{album_name}', '{artist_name}', '{genre}', 0);""".format(sqlId=sqlId,track_name=d,artist_name=artist_name,album_name=album_name,genre=genre,trackid=track_id,track_data=track_data)
						print(INS_QUERY)
						try:
							client.sql(INS_QUERY)
						except Exception as e:
							print("Passed due to same data : ", e)
							print("===========================================================================")
							QUERY = ''' SELECT MAX(ID) FROM PUBLIC.SONG_DATA_ADD; '''
							rre = client.sql(
								QUERY,
								include_field_names=True,
							)
							print(next(rre))
							try:
								sql = next(rre)[0] + 1
								print("Assigned SQL ID : ",sql)
							except:
								sql = 1
							print(" =========================> ", sql , type(sql))
							INS = """INSERT INTO SONG_DATA_ADD (ID, TRACKID, TRACKDATA, VSONG, TRACKNAME, ALBUMNAME, ARTISTNAME, GENRE, STATUS) VALUES({sqlId}, {trackid}, '{track_data}','{vsong}', '{track_name}', '{album_name}', '{artist_name}', '{genre}', 0);""".format(sqlId=sql,vsong = d,track_name=track_name,artist_name=artist_name,album_name=album_name,genre=genre,trackid=track_id,track_data=track_data)
							print(INS)
							try:
								client.sql(INS)
							except Exception as e:
								print("EROOOOOOOR : ",e)
								pass

						str_id = meta + str(track_id)
						print("Yes error is there")
						print(str_id)
						doc = {
							"track_id":track_id,
							"track_name":track_name,
							"album_name":album_name,
							"artist_name":artist_name,
							"genre":genre
						}
						res = es.index(index="songs", doc_type='mixmatch', id=str_id ,body=doc)
						print(res['result'])
						
					else:
						print("no data")
		except Exception as e:
				# raise e
				pass
	print(i)


artistgenre()
