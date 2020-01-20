# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 20:04:54 2018

@author: neel_
"""

import numpy as np
import pandas as pd
import os
import time
#import datetime
import operator
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#%matplotlib inline
import math
import seaborn as sns
#import catplot
sns.set(style="ticks")
from datetime import datetime
import matplotlib.mlab as mlab
import pylab as pl
from scipy.stats import norm
from datetime import timedelta
import csv
import openpyxl
from openpyxl import load_workbook
import string
import datetime

#Set working directory from where the files to collect
aPath='/var/django/StagingData/static/charts/'
os.chdir(aPath)


#Read the data file with bad rows
def file_read(f_name):
    f=open(f_name,'rt',encoding="utf8")
    reader=csv.reader(f)

    csv_list = []
    for l in reader:
        csv_list.append(l)
    f.close()
    return csv_list
# PUT 1 if the 
ftype=1
#ftype=int(ftype)
if ftype==1:
    Infname='Data_QueryRan.xlsx'
    df=pd.read_excel(Infname, error_bad_lines=False) #, error_bad_lines=False, helps to skip the bad lines where the data extends beyond the columns

if ftype==2:
    Infname=input('' )
    df=pd.read_csv(Infname, error_bad_lines=False) #, error_bad_lines=False, helps to skip the bad lines where the data extends beyond the columns

if ftype!=1 and ftype!=2:
    print ('Enter either 1 or 2')
    quit()


#df=pd.read_excel('VTION_DExport_VTIONAPP_Jan_11.xlsx', error_bad_lines=False)

df['created_date']=pd.to_datetime(df['created_date']).dt.date



def time_convrt(s):
    y=s['timestamp']
    x=datetime.datetime.fromtimestamp(y).isoformat()
    return x
df['time_convert']=df.apply(time_convrt,axis=1)
df['time_convert']=pd.to_datetime(df['time_convert']).dt.time


#df=df.sort_values(by=['deviceid','created_date','created_time','pstate'],ascending=[True,True,True,False])
df=df.sort_values(by=['deviceid','created_date','time_convert'],ascending=[True,True,True])

df['pstate'] = df['pstate'].replace(np.nan, 'None', regex=True)
list(df)




df['prev_pstate']=df['pstate'].shift()
df['prev_did']=df['deviceid'].shift()
df['prev_date']=df['created_date'].shift()



def ses_func(d_x):
    global s_id
    if s_id==1:
        y=s_id
        s_id=s_id+1
        return y
    if d_x['pstate']=='"true"':
        y=s_id
        return y
    if d_x['pstate']=='"false"' and d_x['prev_pstate']=='"true"' and d_x['deviceid']==d_x['prev_did'] and d_x['created_date']==d_x['prev_date']:
        y=s_id
        s_id=s_id+1
        return y
    if d_x['pstate']=='"false"' and (d_x['prev_pstate']!='"true"' or d_x['deviceid']!=d_x['prev_did'] or d_x['created_date']!=d_x['prev_date']):
        s_id=s_id+1
        y=s_id
        s_id=s_id+1
        return y

#    if (pd.isnull(d_x['Pstate'])):
    if (d_x['pstate']!='"true"' and d_x['pstate']!='"false"'):
        s_id=s_id+1
        y=s_id
        s_id=s_id+1
        return y

s_id=1
r_num=0
df['pstate']=df['pstate'].astype(str)
df['pstate']
df['ses_id']=df.apply(ses_func,axis=1)
list(df)
df.drop(['prev_pstate','prev_did','prev_date'], axis = 1, inplace = True)

#df=df.sort_values(by=['ses_id'],ascending=[True])


df.to_csv('Data_sessionID.csv',index=False,encoding="utf8")
df=pd.read_csv('Data_sessionID.csv')

#for i in range(len(df['ses_id'])):
 #   y=df['timestamp'].iloc[i]
  #  x=datetime.datetime.fromtimestamp(y).isoformat()
   # df['time'].iloc[i]=x


t_en=pd.read_excel('Input_DataValues.xlsx',sheet_name='English')
eng_char=t_en['Texts'].tolist()


def isEnglish(s):
    text=s['app']
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.replace(' ','')
    for letter in text:
        if letter not in eng_char:
            return 'Junk'

def isEnglish_song(s):
    text=s['song']
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.replace(' ','')
    for letter in text:
        if letter not in eng_char:
            return 'Junk'

def isEnglish_album(s):
    text=s['album']
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.replace(' ','')
    for letter in text:
        if letter not in eng_char:
            return 'Junk'


dferror=pd.DataFrame()
dfwarning=pd.DataFrame()

t=df[df['deviceid'].isnull()]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device ID Blank'
#if x==0:
#    t['Errortype']='None'
dferror=dferror.append(t)

t=df[df['deviceid'].isnull()==False]
t=t[t['deviceid'].str.len()!=36]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device ID length less than 36'
dferror=dferror.append(t)

#Deviceid has not equal to 4 Hypens '-'
t=df[df['deviceid'].isnull()==False]
t=t[t['deviceid'].str.count('-')!=4]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device ID does not have 4 Hyphens'
dferror=dferror.append(t)


t_ev=pd.read_excel('Input_DataValues.xlsx',sheet_name='Event_name')
event_name=t_ev['keyname'].tolist()




t=df[df['keyname'].isin(event_name)==False]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Event/Key Name not in range'
dferror=dferror.append(t)

t_mop=pd.read_excel('Input_DataValues.xlsx',sheet_name='Mob_op')
mob_op=t_mop['mobileoperator'].tolist()

#mob_op=['"!DEA-H | Vodafone IN"','"!DEA-H"','"!dea"','"AirTel"','"Airtel | airtel"',
# '"Airtel"','"IDEA"','"IND airtel"','"IND-JIO"','"Idea"','"JIO 4G | Jio 4G"','"JIO 4G"',
# '"Jio 4G"','"VODAFONE IN | Vodafone IN"','"VODAFONE IN"','"VODAFONE"','"VODAFONEIN | Vodafone IN"',
# '"VODAFONEIN"','"Vodafone IN"','"Vodafone"','"airtel"']

temp_mop=df.copy()

t=temp_mop[temp_mop['mobileoperator'].isin(mob_op)==False]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Alert - Mobile Operator Name Name not in range'
dfwarning=dfwarning.append(t)
t['mobileoperator']

t_app=pd.read_excel('Input_DataValues.xlsx',sheet_name='app')
seg_app=t_app['app'].tolist()
t=df.copy()
t=t[t['app'].isnull()==False]
#t.to_csv('test.csv')
t['app']=t['app'].astype(str)
t['app_junk']=t.apply(isEnglish,axis=1)
t=t[t['app_junk']=='Junk']
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Alert - Non-English characters in app list'
dfwarning=dfwarning.append(t)



t_fm=pd.read_excel('Input_DataValues.xlsx',sheet_name='FM_app')
fm_search=t_fm['fm_app'].tolist()

fm=df[df['keyname']=='"FM_Tuned"']
#fm_search=['FM','Radio','radio','एफ़एम रेडियो','रेडियो']
pattern = '|'.join(fm_search)
t=fm[fm['app'].str.contains(pattern)==False]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='FM app value not in range'
dferror=dferror.append(t)


aud=df[df['keyname']=='"Audio_Tuned"']
aud_search=['""','" "']
aud_search.extend(fm_search)
pattern = '|'.join(aud_search)
t=aud[aud['app'].isin(aud_search)==True]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Audio app value not in range'
dferror=dferror.append(t)


#Album
t_albm=pd.read_excel('Input_DataValues.xlsx',sheet_name='album')
alb_list=t_albm['album'].tolist()
t=df.copy()

alb=['Downloading', '% completed', 'Downloads remaining', 'downloads remaining']
alb.extend(alb_list)
pat_alb = '|'.join(alb)
t=df.copy()
t=t[t['album'].str.contains(pat_alb)==True]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Album - Downloading'
dferror=dferror.append(t)

t_alb=df.copy()
t_alb.album=t_alb.album.str.replace('"','')
t_alb['album']=pd.to_numeric(t_alb['album'],errors='coerce') #Make the non-numeric values to blank
t_alb = t_alb[t_alb['album'].isnull()==False] #Take the blank rows where Radio station valuee are non numeric
t_alb['Errortype']='Album having only numeric value'
dferror=dferror.append(t_alb)


t=df.copy()
t=t[t['album'].isnull()==False]
#t.to_csv('test.csv')
t['album']=t['album'].astype(str)
t['album_junk']=t.apply(isEnglish_album,axis=1)
t=t[t['album_junk']=='Junk']
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Alert - Non-English characters in album list'
dfwarning=dfwarning.append(t)




#Song

t_song=pd.read_excel('Input_DataValues.xlsx',sheet_name='song')
song_list=t_song['song'].tolist()

sng=['%"', 'downloading', 'Downloading','"1"','"1%"','"10%"','"11%"','"100%"','"0%"','"2%"','"20%"','"3%"','"30%"']
sng.extend(song_list)

pat_sng = '|'.join(sng)
t=df.copy()
t=t[t['song'].str.contains(pat_sng)==True]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Song - Downloading/Wrong value'
dferror=dferror.append(t)

t_sng=df.copy()
t_sng.song=t_sng.song.str.replace('"','')
t_sng['song']=pd.to_numeric(t_sng['song'],errors='coerce') #Make the non-numeric values to blank
t_sng = t_sng[t_sng['song'].isnull()==False] #Take the blank rows where Radio station valuee are non numeric
t_sng['Errortype']='Song having only numeric value'
dferror=dferror.append(t_sng)

t=df.copy()
t=t[t['song'].isnull()==False]
#t.to_csv('test.csv')
t['song']=t['song'].astype(str)
t['song_junk']=t.apply(isEnglish_song,axis=1)
t=t[t['song_junk']=='Junk']
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Alert - Non-English characters in song list'
dfwarning=dfwarning.append(t)



t_source=pd.read_excel('Input_DataValues.xlsx',sheet_name='source')
seg_source=t_source['source'].tolist()

sourc=df[df['keyname'].isin(['"Audio_Tuned"','"FM_Tuned"'])==True]
source_search=['"BT"','"Speaker"','"UnKnown"','"Wire_HeadPhone"','"Wire_Headset"']
t=sourc[sourc['source'].isin(seg_source)==False]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Segment Source value not in range'
dferror=dferror.append(t)


#
d_station=pd.read_excel('Input_DataValues.xlsx',sheet_name='Radio')

city_list=[]
city_list=d_station['segment_City'].tolist()
t=df[df['city'].isin(city_list)==False]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Alert - Check City List'
dfwarning=dfwarning.append(t)



list(df)

channel_list=[]
t=df.groupby(['station']).agg({'deviceid':'nunique'}).reset_index()
channel_list=t['station'].tolist()

app_list=[]
t=df.groupby(['app']).agg({'deviceid':'nunique'}).reset_index()
app_list=t['app'].tolist()

#Checking Date column
dayT=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
monT=['1','2','3','4','5','6','7','8','9','10','11','12']
df['created_date']=df['created_date'].astype(str)
t_date=df.copy()
t_date['created_date']=pd.to_datetime(t_date['created_date']).dt.date
t_date['created_date']=t_date['created_date'].astype(str)
t1=t_date['created_date'].str.split('-',expand=True)
t2=t_date.copy()
t2['mon']=t1[1]
t2['day']=t1[2]
t2['yr']=t1[0]
t2['mon']=t2['mon'].astype(str)
t2['day']=t2['day'].astype(str)
t2['yr']=t2['yr'].astype(str)
#t2.to_csv('date_test.csv')

t=pd.DataFrame()

t=t2[t2['yr']!='2018']
t=t[t['yr']!='2019']

t2['mon']=pd.to_numeric(t2['mon'],errors='coerce') #Make the non-numeric values to blank
t3=t2[t2['mon'].isnull()==True] #Take the blank rows where Radio station valuee are non numeric
t2['day']=pd.to_numeric(t2['day'],errors='coerce') #Make the non-numeric values to blank
t4=t2[t2['day'].isnull()==True] #Take the blank rows where Radio station valuee are non numeric

t5=t2[t2['mon']>12]
t6=t2[t2['day']>31]

t=t.append(t3)
t=t.append(t4)
t=t.append(t5)
t=t.append(t6)
list(t)
t.drop(columns =["mon",'day','yr'], inplace = True)
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Date value not in range dd-mm-yyyy'
dferror=dferror.append(t)
#t.to_csv('date_test.csv')

#Checking Time column
df['created_time']=df['created_time'].astype(str)
t_t=df[df['created_time'].isnull()==False]
t1=t_t['created_time'].str.split(':',expand=True)
t2=df.copy()
t3=t2[t2['created_time'].isnull()==True]
t3['Errortype']='Alert - Time value(created_time) is blank'
dfwarning=dfwarning.append(t3)

t3=t2[t2['created_time'].isnull()==False]
t3['hr']=t1[0]
t3['mn']=t1[1]
t3['sc']=t1[2]


mn_sc=['00','01','02','03','04','05','06','07','08','09','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
       '17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41',
       '42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59']

t=t3[t3['hr'].isin(['00','01','02','03','04','05','06','07','08','09','0','1','2','3','4','5','6','7','8','9','10','11',
     '12','13','14','15','16','17','18','19','20','21','22','23'])==False]
t=t3[t3['mn'].isin(mn_sc)==False]
t=t3[t3['sc'].isin(mn_sc)==False]
t.drop(columns =["hr",'mn','sc'], inplace = True)
t['Errortype']='Alert - Time value not in range'
dfwarning=dfwarning.append(t)

#Checking Station name
df.station=df.station.str.replace('"','')
t=df[df['keyname']=='"FM_Tuned"']
t['station']=pd.to_numeric(t['station'],errors='coerce') #Make the non-numeric values to blank
t = t[t['station'].isnull()==True] #Take the blank rows where Radio station valuee are non numeric
t['Errortype']='Radio Stattion value (MHz) non-numeric'
dferror=dferror.append(t)

#Checking Device Make
d_dmake=pd.read_excel('Input_DataValues.xlsx',sheet_name='Dev_make')
div_list=d_dmake['devicemake'].tolist()
t=df[df['devicemake'].isin(div_list)==False]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Alert - Check Device make List'
dfwarning=dfwarning.append(t)

#Checking Device Model (Device model should contain the name of device make)
t_dev_make_mod=df.copy()
t_dev_make_mod.devicemake=t_dev_make_mod.devicemake.str.replace('"','')
t_dev_make_mod['C'] = t_dev_make_mod.apply(lambda x: x.devicemake in x.devicemodel, axis=1)
t=t_dev_make_mod[t_dev_make_mod['C']==False]
t.drop(['C'], axis = 1, inplace = True)
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Check Device Make & Model name'
dferror=dferror.append(t)

def isEnglish_make(s):
    text=s['devicemake']
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.replace(' ','')
    for letter in text:
        if letter not in eng_char:
            return 'Junk'

def isEnglish_model(s):
    text=s['devicemodel']
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.replace(' ','')
    for letter in text:
        if letter not in eng_char:
            return 'Junk'

t=df.copy()
t['devicemake']=t['devicemake'].astype(str)
t['make_junk']=t.apply(isEnglish_make,axis=1)
t=t[t['make_junk']=='Junk']
t.drop(['make_junk'], axis = 1, inplace = True)
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device make - Contains non-English character'
dferror=dferror.append(t)

t=df.copy()
t['devicemodel']=t['devicemodel'].astype(str)
t['mod_junk']=t.apply(isEnglish_make,axis=1)
t=t[t['mod_junk']=='Junk']
t.drop(['mod_junk'], axis = 1, inplace = True)
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device model - Contains non-English character'
dferror=dferror.append(t)

t=df.copy()
t=t[t['devicemake'].isnull()==True]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device make - Blank'
dferror=dferror.append(t)

t=df.copy()
t=t[t['devicemodel'].isnull()==True]
x=len(t['deviceid'])
if x>0:
    t['Errortype']='Device model - Blank'
dferror=dferror.append(t)
#Device make and model checking ends



df['deviceid']

df_noerr=df.copy()
df_noerr['Errortype']='Total Records'
df_noerr['deviceid']='Across all devices'


dferror.to_csv('Error_data.csv',index=False)

#Writing error reports
writer = pd.ExcelWriter('Error_report.xlsx', engine='openpyxl')
dferror.to_excel(writer, sheet_name='Error_detail', startrow=0, index=False)




err_rep=dferror.groupby(['deviceid','created_date','Errortype']).agg({'ses_id':'nunique'}).reset_index()
err_rep.rename(columns={'ses_id': 'Number of sessions'}, inplace=True)
err_rep1=df_noerr.groupby(['deviceid','created_date','Errortype']).agg({'ses_id':'nunique'}).reset_index()
err_rep1.rename(columns={'ses_id': 'Number of sessions'}, inplace=True)
err_rep=err_rep.append(err_rep1)
err_rep.to_excel(writer, sheet_name='device_rep', startrow=0, index=False)

err_rep=dferror.groupby(['created_date','Errortype']).agg({'ses_id':'nunique'}).reset_index()
err_rep.rename(columns={'ses_id': 'Number of sessions'}, inplace=True)
err_rep1=df_noerr.groupby(['created_date','Errortype']).agg({'ses_id':'nunique'}).reset_index()
err_rep1.rename(columns={'ses_id': 'Number of sessions'}, inplace=True)
err_rep=err_rep.append(err_rep1)
err_rep.to_excel(writer, sheet_name='datewise_rep', startrow=0, index=False)

err_rep=dferror.groupby(['created_date']).agg({'ses_id':'nunique'}).reset_index()
err_rep.rename(columns={'ses_id': 'Number of sessions','created_date':'created_date(Any error)'}, inplace=True)
err_rep['status']='Having any error'
err_rep1=df_noerr.groupby(['created_date']).agg({'ses_id':'nunique'}).reset_index()
err_rep1.rename(columns={'ses_id': 'Number of sessions','created_date':'created_date(Any error)'}, inplace=True)
err_rep1['status']='Total Records'
err_rep=err_rep.append(err_rep1)
err_rep.to_excel(writer, sheet_name='Overall_Err_rep', startrow=0, index=False)

#Write warning
df_all=df.copy()
df_all['Errortype']='Total Records'

err_rep=dfwarning.groupby(['created_date','Errortype']).agg({'deviceid':'nunique','ses_id':'nunique'}).reset_index()
err_rep.rename(columns={'deviceid': 'Number of devices','ses_id': 'Number of sessions'}, inplace=True)
err_rep1=df_all.groupby(['created_date','Errortype']).agg({'deviceid':'nunique','ses_id':'nunique'}).reset_index()
err_rep1.rename(columns={'deviceid': 'Number of devices','ses_id': 'Number of sessions'}, inplace=True)
err_rep=err_rep.append(err_rep1)
err_rep.to_excel(writer, sheet_name='alert', startrow=0, index=False)

dfwarning.to_excel(writer, sheet_name='alert_detail', startrow=0, index=False)


#Check session with True and False state
df=pd.read_csv('Data_sessionID.csv')
t_Pstate1=df[df['keyname']=='"Audio_Tuned"']
t_Pstate2=df[df['keyname']=='"FM_Tuned"']
t_Pstate1=t_Pstate1.append(t_Pstate2)
print (t_Pstate1['pstate'].isnull())
er_state=t_Pstate1.groupby(['deviceid','created_date','ses_id']).agg({'pstate':'nunique'}).reset_index()
er_state.rename(columns={'pstate': 'Pstate(error)'}, inplace=True)
t=er_state[er_state['Pstate(error)']==1]
t['Errortype']='Pstate not having combination of True/False'
t.to_excel(writer, sheet_name='PState_warn1', startrow=0, index=False)

t=t.groupby(['Errortype','created_date']).agg({'deviceid':'nunique','ses_id':'nunique'}).reset_index()
t.rename(columns={'deviceid': 'Number of DeviceId','ses_id': 'Number of SessionId'}, inplace=True)

t1=er_state.copy()
t1['Errortype']='All Records'
t1=t1.groupby(['Errortype','created_date']).agg({'deviceid':'nunique','ses_id':'nunique'}).reset_index()
t1.rename(columns={'deviceid': 'Number of DeviceId','ses_id': 'Number of SessionId'}, inplace=True)

t=t.append(t1)

t.to_excel(writer, sheet_name='PState_warn2', startrow=0, index=False)



writer.save()

err_sess=dferror.groupby(['ses_id']).agg({'deviceid':'nunique'}).reset_index()

#Session ID with erroneous data, to be excluded from final analysis
ErSess_list=err_sess['ses_id'].tolist()

df_clean=df[df['ses_id'].isin(ErSess_list)==False]
df_clean['created_date']=pd.to_datetime(df_clean['created_date']).dt.date

df_clean.to_csv('Clean_data.csv',index=False)


#Check Duration
df_clean=pd.read_csv('Clean_data.csv')
t=df_clean.copy()
t.duration=t.duration.str.replace('"','')
t=t[t['duration'].isnull()==False]

#Scatter Plot
t['duration']=t['duration'].astype(int)
tem1=t.loc[t['keyname']=='"FM_Tuned"']
tem2=t.loc[t['keyname']=='"Audio_Tuned"']

tem1=tem1.loc[tem1['duration'] > 6]
tem2=tem2.loc[tem2['duration'] > 6]

num_arr=np.array(tem1['duration'])
num_arr

max_fm=np.max(num_arr, axis=0)
mean_fm = np.mean(num_arr, axis=0)
sd_fm = np.std(num_arr, axis=0)
top_perFM=np.percentile(num_arr, 99.71)
print(mean_fm+3*sd_fm)

#tem1['created_time']=tem1['created_time'].astype(datetime)

x=tem1['timestamp'].tolist()
y=tem1['duration'].tolist()
plt.scatter(x,y, label='scatterplot', color='k', s=25, marker="o")
plt.xlabel('timestamp')
plt.ylabel('duration')
plt.title('Scatter graph FM\nCheck it out')
plt.legend()
# plt.show()

#Audio
num_arr=np.array(tem2['duration'])
num_arr

max_aud=np.max(num_arr, axis=0)
mean_aud = np.mean(num_arr, axis=0)
sd_aud = np.std(num_arr, axis=0)
top_perAud=np.percentile(num_arr, 99.6)

print(mean_aud+3*sd_aud)

#tem2['created_time']=tem2['created_time'].astype(datetime)

x=tem2['timestamp'].tolist()
y=tem2['duration'].tolist()
plt.scatter(x,y, label='scatterplot', color='k', s=25, marker="o")
plt.xlabel('timestamp')
plt.ylabel('duration')
plt.title('Scatter graph Audio\nCheck it out')
plt.legend()
# plt.show()

tem3=tem2.loc[tem2['source'].isin(['"Wire_Headset"','"Wire_HeadPhone"'])==True]
x=tem3['timestamp'].tolist()
y=tem3['duration'].tolist()
plt.scatter(x,y, label='scatterplot', color='k', s=25, marker="o")
plt.xlabel('timestamp')
plt.ylabel('duration')
plt.title('Scatter graph Audio wired headset\nCheck it out')
plt.legend()
# plt.show()

tem4=tem2.loc[tem2['source'].isin(['"BT"','"Speaker"','"UnKnown"'])==True]
x=tem4['timestamp'].tolist()
y=tem4['duration'].tolist()
plt.scatter(x,y, label='scatterplot', color='k', s=25, marker="o")
plt.xlabel('timestamp')
plt.ylabel('duration')
plt.title('Scatter graph Audio Speaker/BT\nCheck it out')
plt.legend()
# plt.show()

fm_durclean=tem1.loc[tem1['duration'] > (mean_fm+3*sd_fm)]
aud_durclean=tem2.loc[tem2['duration'] > (mean_aud+3*sd_aud)]

sesid_durclean=fm_durclean['ses_id'].tolist()
sesid_durclean.extend(aud_durclean['ses_id'].tolist())
t_6s=t[t['duration']<7]
sesid_durclean.extend(t_6s['ses_id'].tolist())


df_cleanDur=df_clean[df_clean['ses_id'].isin(sesid_durclean)==False]
df_cleanDur.to_csv('CleanData_WithDur.csv',index=False)  #Clean data with removing duration outlier

#Duration checking ends

df_cleanDur=pd.read_csv('CleanData_WithDur.csv')
t=df_cleanDur.copy()
temp=t.groupby(['ses_id']).agg({'city':'nunique'}).reset_index()
temp['city']=temp['city'].astype(int)
temp=temp[temp['city']>1]
dup_city=temp['ses_id'].tolist()
temp1=t[t['ses_id'].isin(dup_city)==True]

temp1.to_csv('Chk_dupCity.csv',index=False)



list(err_rep)
