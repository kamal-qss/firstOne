import pandas as pd
from datetime import date, timedelta
import numpy as np

data_main_np = []
for day_back in range(3):
    
    yesterday = date.today() - timedelta(days=day_back+2)
    files_location = "/home/dhananjai/Desktop/data_panda/Data_"+yesterday.strftime('%m_%d_%Y')+'.csv'
    print(files_location)
    file_read = pd.read_csv(files_location, low_memory=False)
    data_main_np.append(file_read.values)

comb_np_array = np.vstack(data_main_np)
data_main = pd.DataFrame(comb_np_array)

data_main.columns = ['appid',	'DeviceId',	'vtionid',	'deviceModel',	'platform',	'apppackage',	'keyname',	'mobileOperator', 'app', 'song',	'album', 'Pstate', 'Program', 'Episode', 'Source','ipaddress', 'city',	'station', 'duration',	'timestamp', 'created_date',	'created_time',	'stationName', 'artist_name', 'genre', 'education', 'ownership', 'nccs_code', 'age', 'gender', 'number', 'Uninstall', 'Reward_option']
data_main = data_main.loc[(data_main['Pstate'] == 'false') | (data_main['Pstate'] == False)]
        
df_fm = data_main.loc[(data_main['keyname'] == 'FM_Tuned')]
df_audio = data_main.loc[(data_main['keyname'] == 'Audio_Tuned')]
df_video = data_main.loc[(data_main['keyname'] == 'Video_Tuned')]



# df_audio.drop(df_audio.loc[df_audio['Pstate']==True].index, inplace=True)
# df_fm.drop(df_fm.loc[df_fm['Pstate']==True].index, inplace=True)

# df_video.drop(df_video.loc[df_video['Pstate']==True].index, inplace=True)

df_video.drop(df_video.loc[df_video['Program'].isnull()].index, inplace = True)
df_audio.drop(df_audio.loc[df_audio['song'].isnull() | df_audio['song'] == ''].index, inplace = True)

# # Audio Tuned
df_audio.drop(['appid' , 'DeviceId', 'deviceModel', 'platform', 'apppackage', 'keyname', 
 				'Pstate', 'Source', 'ipaddress', 'Program', 'city', 'stationName','station',  
 				'Episode', 'education', 'ownership', 'nccs_code', 'age', 'gender',
 				'number', 'Uninstall', 'Reward_option'], axis = 1, inplace= True)

# # Video Tuned
df_video.drop(['appid' , 'DeviceId', 'deviceModel', 'platform', 'apppackage', 'keyname', 
 				'Pstate', 'song', 'album', 'Source', 'ipaddress','city', 'station', 'stationName', 
 				'artist_name', 'genre', 'education', 'ownership', 'nccs_code', 'age', 'gender',
 				'number', 'Uninstall', 'Reward_option'], axis = 1, inplace= True)
 			
# # FM Tuned	 

df_fm.drop(['appid' , 'DeviceId', 'deviceModel', 'platform', 'apppackage', 'keyname', 
 				'Pstate', 'song', 'album', 'Source', 'ipaddress', 'Program', 
 				'Episode', 'artist_name', 'genre', 'education', 'ownership', 'nccs_code', 'age', 'gender',
 				'number', 'Uninstall', 'Reward_option'], axis = 1, inplace= True)



df_audio.reset_index(drop = True, inplace= True)
df_fm.reset_index(drop = True, inplace= True)
df_video.reset_index(drop = True, inplace= True)


list_ts_date_fm = []
list_ts_time_fm = []

list_ts_date_audio = []
list_ts_time_audio = []

list_ts_date_video = []
list_ts_time_video = []

for i in range (len(df_fm['duration'])):
    try:
        ts = df_fm['timestamp'][i]-int(df_fm['duration'][i])
        list_ts_date_fm.append(pd.to_datetime(ts, unit ='s').tz_localize('UTC').tz_convert('Asia/Kolkata').date().strftime('%d/%m/%Y'))
        list_ts_time_fm.append(pd.to_datetime(ts, unit ='s').tz_localize('UTC').tz_convert('Asia/Kolkata').time().strftime('%r'))
    except:
        pass
    
for i in range (len(df_audio['duration'])):
    try:
        ts = df_audio['timestamp'][i]-int(df_audio['duration'][i])
        list_ts_date_audio.append(pd.to_datetime(ts, unit ='s').tz_localize('UTC').tz_convert('Asia/Kolkata').date().strftime('%d/%m/%Y'))
        list_ts_time_audio.append(pd.to_datetime(ts, unit ='s').tz_localize('UTC').tz_convert('Asia/Kolkata').time().strftime('%r'))
    except:
        pass

for i in range (len(df_video['duration'])):
    try:
        ts = df_video['timestamp'][i]-int(df_video['duration'][i])
        list_ts_date_video.append(pd.to_datetime(ts, unit ='s').tz_localize('UTC').tz_convert('Asia/Kolkata').date().strftime('%d/%m/%Y'))
        list_ts_time_video.append(pd.to_datetime(ts, unit ='s').tz_localize('UTC').tz_convert('Asia/Kolkata').time().strftime('%r'))
    except:
        pass
    
df_fm['start_date'] = pd.DataFrame(list_ts_date_fm)
df_fm['start_time'] = pd.DataFrame(list_ts_time_fm)

df_audio['start_date'] = pd.DataFrame(list_ts_date_audio)
df_audio['start_time'] = pd.DataFrame(list_ts_time_audio)

df_video['start_date'] = pd.DataFrame(list_ts_date_video)
df_video['start_time'] = pd.DataFrame(list_ts_time_video)



# print(df_fm.columns.tolist())

df_fm = df_fm.rename({'created_time': 'end_time'}, axis='columns')
df_audio = df_audio.rename({'created_time': 'end_time'}, axis='columns')
df_video = df_video.rename({'created_time': 'end_time'}, axis='columns')


# # # # vtionid	mobileOperator	app	song	album	artist_name	genre	start_date	start_time	end_time	duration

df_audio = df_audio[['vtionid', 'mobileOperator', 'app', 'song', 'album', 'artist_name' , 'genre', 'start_date', 'start_time', 'end_time', 'duration']]
df_fm =  df_fm[['vtionid', 'mobileOperator', 'start_date', 'start_time',  'end_time', 	'duration',	'station',	'city',	'stationName']]
df_video = df_video[['vtionid','mobileOperator','app','start_date','start_time', 'end_time', 'duration', 'Program','Episode']]

# # print(df_fm)

#Drop timestamp
# print(df_fm)
# # # print(df_audio.columns.tolist())
# # # print(df_video.columns.tolist())


df_fm.to_csv('/home/dhananjai/Desktop/Desktop_files/New2/var/django/StagingData/Jobs/test/fm_test31.csv',index=False)
df_audio.to_csv('/home/dhananjai/Desktop/Desktop_files/New2/var/django/StagingData/Jobs/test/audio_test31.csv',index=False)
df_video.to_csv('/home/dhananjai/Desktop/Desktop_files/New2/var/django/StagingData/Jobs/test/video_test31.csv',index=False)

# # # df_audio.to_csv('audio_test2.csv',index=False)
# # # df_video.to_csv('video_test2.csv',index=False)


df_fm.reset_index(drop = True, inplace= True)
df_audio.reset_index(drop = True, inplace= True)
df_video.reset_index(drop = True, inplace= True)