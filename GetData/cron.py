import psycopg2
from pyignite import Client
import json
import csv
from datetime import date, timedelta
import os
import base64
import datetime
import time
import re

def filter(song_name):
    return (song_name.replace('_',' ').
            replace(':', '').
            replace('|', ' ').
            replace('-', ' ').
            replace('+', ' ').
            replace('  ',' ').
            replace('\"', '').
            replace('#', '').
            replace('(', '').
            replace(')', '').
            replace('[', ''))

    
def remove_bdata(toreg):
    return re.sub("[\(\[].*?[\)\]]", "", toreg)

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def domain(inputString):
    pattern = r"[www.[(\w]*\.(com|org|net|LINK|Audio|Info|co|Net|COM|In|info|me|IN|ME|io|name|in|PK|TANDA|Fun|Com|Co|INFO|Fm|m4a|im|Name|pk|La|CC|cc|mp3|click|mobi)\S*"
    return re.sub(pattern, '', inputString)

def select_before_list(inputString):
    before_select_list = ['Feat', 'Ft', 'ft', 'By', 'by', 'DJ', 'dj','320', 'Hd', 'HD', 'Lyric','Latest', 'Official', 'official', 'Video', ' -', '(From']
    for i in before_select_list:
        try:
            return inputString[0: inputString.index(i)]
        except:
            pass
    return inputString

def export_users_csv():
    print("Hello")
    nodes = [
        ('35.154.247.92', 10800),
        ('35.154.247.92', 10801),
    ]
    conn = psycopg2.connect(dbname="VTIONData", host="vtionproddb.chgz4nqwpdta.ap-south-1.rds.amazonaws.com",
                            user="vtion", password="per4mance")
    cur = conn.cursor()
    client = Client()
    client.connect(nodes)

    yesterday = date.today() - timedelta(days=1)
    yesterdayMidnight = int(time.mktime(yesterday.timetuple())) - 19800
    print("FROM : ", yesterdayMidnight)
    todayMidnight = yesterdayMidnight + 86400
    print(todayMidnight)
    
    yesterdayMidnight = '1579199400'
    todayMidnight = '1579285800'
      
    QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, 
                 COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE 
                 "TIMESTAMP" > '{}' AND "TIMESTAMP" < '{}' ;'''.format(yesterdayMidnight,todayMidnight)
    
    result = client.sql(
        QUERY,
        include_field_names=True,
    )
    next(result)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    namespac = BASE_DIR + str("/target/Data_"+yesterday.strftime('%m_%d_%Y')+'.csv')

    with open(namespac, 'w+') as writeFile:
        print("START : ", time.localtime(time.time()))
        writer = csv.writer(writeFile)
        
        writer.writerow(
            ['appid', 'DeviceId', 'vtionid', 'deviceModel', 'platform', 'apppackage', 'keyname', 'mobileOperator',
             'app', 'song', 'album', 'Pstate', 'Program', 'Episode', 'Source', 'ipaddress', 'city', 'station',
             'duration', 'timestamp', 'created_date', 'created_time', 'stationName', 'artist_name', 'genre',
             'education', 'ownership', 'nccs_code', 'age', 'gender', 'number', 'Uninstall', 'Reward_option'])
        i = 0
        for row in result:
            nccs = age = gender = number = status = ''
            artist_name = ''
            genre = ''
            try:
                cur.execute('''SELECT nccs_code FROM public.installdata WHERE deviceid = '{}';'''.format(row[6]))
                nccs_result = cur.fetchone()
                nccs_res = nccs_result[0]
            except Exception as e:
                nccs_res = ''
                pass

            if i == 0:
                x = row[2]
                i = 1
            else:
                x = row[5]
                urlSafeEncodedBytes = base64.urlsafe_b64encode(row[6].encode("utf-8"))
                vtionid = str(urlSafeEncodedBytes, "utf-8")
                try:
                    y = json.loads(x)
                    if y.get("segmentation") is None:
                        writer.writerow([row[1],row[6],vtionid,y.get("d"),y.get("p"),y.get("ap"),row[2],y.get("network").get("ope"),"","","","","","","",row[10],row[11],"","",row[7],row[3],row[4]])
                    else:
                        if y.get("ap") == "com.video.meter":
                            song = y.get("segmentation").get("Song")
                            app = y.get("segmentation").get("App")
                            education = y.get("segmentation").get("Highest Education")
                            ownership = y.get("segmentation").get("Ownership")
                            if row[2] == 'FM_Tuned':
                                try:
                                    QUERYa = ''' SELECT STATION FROM MASTERTABLEDEMO WHERE CITY = '{}'
                                    AND FREQUENCY = '{}'; '''.format(
                                        row[11], y.get("segmentation").get("Station"))
                                    resulta = client.sql(
                                        QUERYa,
                                        include_field_names=True,
                                    )
                                    next(resulta)
                                    stationName = [rowa for rowa in resulta]
                                    writer.writerow(
                                        [row[1], row[6], vtionid, y.get("d"), y.get("p"), y.get("ap"), row[2],
                                        y.get("network").get("ope"), y.get("segmentation").get("App"),
                                        y.get("segmentation").get("Song"), y.get("segmentation").get("Album"),
                                        y.get("segmentation").get("PState"), "", "",
                                        y.get("segmentation").get("Source"), row[10], row[11],
                                        y.get("segmentation").get("Station"), y.get("segmentation").get("Duration"),
                                        row[7], row[3], row[4], stationName[0][0], "", "", "", "", nccs_res])
                                except Exception as e:
                                    writer.writerow(
                                        [row[1], row[6], vtionid, y.get("d"), y.get("p"), y.get("ap"), row[2],
                                        y.get("network").get("ope"), y.get("segmentation").get("App"),
                                        y.get("segmentation").get("Song"), y.get("segmentation").get("Album"),
                                        y.get("segmentation").get("PState"), "", "",
                                        y.get("segmentation").get("Source"), row[10], row[11],
                                        y.get("segmentation").get("Station"), y.get("segmentation").get("Duration"),
                                        row[7], row[3], row[4], "", "", "", "", "", nccs_res])

                            elif row[2] == 'Video_Tuned' or row[2] == 'Video_off':
                                try:
                                    writer.writerow([row[1], row[6], vtionid, y.get("d"), y.get("p"), y.get("ap"), row[2],
                                                    y.get("network").get("ope"), y.get("segmentation").get("App"),
                                                    y.get("segmentation").get("Song"), y.get("segmentation").get("Album"),
                                                    y.get("segmentation").get("PState"),
                                                    y.get("segmentation").get("Program"),
                                                    y.get("segmentation").get("Episode"),
                                                    y.get("segmentation").get("Source"), row[10], row[11], "",
                                                    y.get("segmentation").get("Duration"), row[7], row[3], row[4], "", "",
                                                    "", "", "", nccs_res])

                                except Exception as e:
                                    pass

                            elif row[2] == 'Audio_Tuned':
                                try:
                                    if song: 
                                        if song.isdigit():
                                            continue          
                                        song = song.strip()
                                        filter_new = ['Download', 'download', 'AUD', 'Advertise', '%']
                                        status_filter = (filter_new[0] in song or filter_new[1] in song or filter_new[2] in
                                                        song or filter_new[3] in song or filter_new[4] in song)
                                        if str(status_filter) == 'False':
                                            album = y.get("segmentation").get("Album")
                                            if album is None:
                                                album_filter = False
                                            else:
                                                a_filter = ['unknown', 'Advertise', 'Sponsored']
                                                album_filter = (a_filter[0] in album or a_filter[1] in album
                                                                or a_filter[2] in album)

                                            if str(album_filter) == 'False':
                                                QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA
                                                WHERE TRACKNAME = '{}';'''.format(song)
                                                details = client.sql(
                                                    QUERY,
                                                    include_field_names=True,
                                                )
                                                next(details)
                                                for det in details:
                                                    artist_name = det[0]
                                                    genre = det[1]
                                                if artist_name:
                                                    pass
                                                else:
                                                    QUERY = '''SELECT ARTISTNAME, GENRE FROM PUBLIC.SONG_DATA_ADD 
                                                    WHERE TRACKNAME = '{}';'''.format(song)
                                                    details = client.sql(
                                                        QUERY,
                                                        include_field_names=True,
                                                    )
                                                    next(details)
                                                    for det in details:
                                                        artist_name = det[0]
                                                        genre = det[1]
                                                    
                                                if app == 'Amazon Music':
                                                    pass
                                                    if '%' in song or song.isdigit():
                                                        continue
                                                    else:
                                                        if 'ñ' in song:
                                                            song = song.replace('ñ', 'n')
                                                        else:
                                                            pass
                                                    song = deEmojify(filter(remove_bdata(song).replace(')', '').replace('(', '')))
                                                    
                                                elif app == 'Spotify' or 'Spot' in app:
                                                    if '%' in song:
                                                        continue
                                                    else:
                                                        song = filter(deEmojify(remove_bdata(song))) 
                                                            
                                                elif app == 'Gaana':
                                                    if 'Gaana' in song or song.isdigit() or song ==',':
                                                        continue
                                                    else:
                                                        if 'ñ' in song or '├▒' in song:
                                                            song = song.replace('ñ', 'n').replace('├▒', 'n')
                                                        else:
                                                            pass
                                                    song = select_before_list(remove_bdata(deEmojify(song))).lstrip('Ep 0123456789-.')
                                                
                                                elif app == 'Google Play Music':
                                                    aa = song
                                                    if song.isdigit() or 'high quality' in song or song == ',':
                                                        continue
                                                    else:
                                                        song = domain(remove_bdata(song)).lstrip(' 0123456789.-').strip()
                                                        if '128k' in song or '256k' in song or 'p3' in song:
                                                            song = song.replace('(128k)', '').replace('(256k)', '').replace('128k', '').replace('256k', '').replace('.mp3', '')
                                                        song = select_before_list(filter(deEmojify(song)))
                                                        
                                                elif app == 'Hungama':
                                                    song = filter(remove_bdata(deEmojify(song)))
                                                    
                                                elif app == 'i Music':   
                                                    song = song.replace('-',' ').replace(':',' ').replace('   ', ' ').replace('  ', ' ').replace('.mp3', '')
                                                    if 'Unknown artist' in song or 'i Music' in song or '//' in song:
                                                        continue
                                                    song = deEmojify(select_before_list(filter(domain(remove_bdata(song))).lstrip(' 0123456789.-').strip())).strip()
                                                    
                                                elif app == 'JioSaavn':
                                                    song = filter(remove_bdata(song))
                                                
                                                elif app =='Saavn': #combine with jio savan
                                                    song = filter(domain(remove_bdata(song)))
                                                    app = 'JioSaavn'
                                                
                                                elif app == 'MX Player' :
                                                    if '--:--:--' in song or 'Insufficient balance' in song or 'Expiry Date' in song :
                                                        continue
                                                    else:
                                                        song = deEmojify(filter(remove_bdata(song)).replace('  ',' ')).strip()
                                                    
                                                elif app == 'Music Player':       
                                                    song = domain(filter(remove_bdata(song))).replace('  ',' ').lstrip(' 0123456789.-').strip()
                                                    
                                                elif app == 'Wynk Music':
                                                    song = remove_bdata(deEmojify(song)).lstrip(' 0123456789.-').strip()
                                                    if song.isdigit() or '%' in song:
                                                        continue
                                                    elif '(From' in song:           
                                                        song = song.replace('(From', '')
                                                    else:
                                                        if '")' in song:
                                                            song = remove_bdata(song.replace('\")', ''))

                                                elif app == 'YouTube Music':
                                                    song = filter(deEmojify(remove_bdata(song)))

                                                else:
                                                    song = song
                                                    app = app

                                                try:
                                                    if song:
                                                        if song.isdigit():
                                                            continue          
                                                        song = song.strip()
                                                        writer.writerow(
                                                            [row[1], row[6], vtionid, y.get("d"), y.get("p"), y.get("ap"),
                                                            row[2],
                                                            y.get("network").get("ope"), app,
                                                            song,
                                                            y.get("segmentation").get("Album"),
                                                            y.get("segmentation").get("PState"), "", "",
                                                            y.get("segmentation").get("Source"), row[10], row[11],
                                                            y.get("segmentation").get("Station"),
                                                            y.get("segmentation").get("Duration"), row[7], row[3], row[4], "",
                                                            artist_name, genre, '', '', nccs_res, '', '', '',
                                                            ''])
                                                    else:
                                                        pass
                                                except Exception as e:
                                                    pass
                                        else:
                                            pass
                                    else:
                                        pass
                                except Exception as e:
                                    pass
                            elif row[2] == 'Register' or row[2] == 'Profile':
                                if ownership:
                                    try:
                                        own = ownership.split(',')
                                        if len(own) >= 9:
                                            num_own = 9
                                        else:
                                            num_own = len(own)
                                        cur.execute(
                                            '''SELECT nccs_code FROM public.nccs_flat where education = '{}' 
                                                and ownership = '{}';'''.format(education, num_own))
                                        nccs = cur.fetchone()
                                    except Exception as e:
                                        pass
                            
                                try:
                                    try:
                                        cur.execute(
                                            '''SELECT payment_option FROM public.payment_option where deviceid = '{}';
                                            '''.format(row[6]))
                                        payment_option = cur.fetchone()
                                        payment = payment_option[0]
                                    except:
                                        payment = 'Amazon voucher'
                                        pass

                                    age = y.get("segmentation").get("age")
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
                                    num_status = "+" in number
                                    if str(num_status) == 'True':
                                        number = ''
                                    else:
                                        try:
                                            cur.execute(
                                                '''SELECT i_status FROM public.appsflyer where
                                                    number = '{}';'''.format(number))
                                            status_now = cur.fetchone()
                                            status = status_now[0]
                                            if status != 'True':
                                                status = ''
                                        except:
                                            pass
                                    try:
                                        writer.writerow(
                                            [row[1], row[6], vtionid, y.get("d"), y.get("p"), y.get("ap"), row[2],
                                            y.get("network").get("ope"), y.get("segmentation").get("App"),
                                            y.get("segmentation").get("Song"), y.get("segmentation").get("Album"),
                                            y.get("segmentation").get("PState"), "", "",
                                            y.get("segmentation").get("Source"), row[10], row[11],
                                            y.get("segmentation").get("Station"),
                                            y.get("segmentation").get("Duration"), row[7], row[3], row[4], "",
                                            artist_name, genre, education, ownership, nccs[0], age, gender, number,
                                            status, payment])
                                    except Exception as e:
                                        pass
                                        writer.writerow(
                                            [row[1], row[6], vtionid, y.get("d"), y.get("p"), y.get("ap"), row[2],
                                                y.get("network").get("ope"), y.get("segmentation").get("App"),
                                                y.get("segmentation").get("Song"), y.get("segmentation").get("Album"),
                                                y.get("segmentation").get("PState"), "", "",
                                                y.get("segmentation").get("Source"), row[10], row[11],
                                                y.get("segmentation").get("Station"),
                                                y.get("segmentation").get("Duration"), row[7], row[3], row[4], "",
                                                artist_name, genre, education, ownership, "", age, gender, number, status,
                                                payment])
                                except Exception as e:
                                    pass
                            else:
                                writer.writerow([row[1], row[6],vtionid, y.get("d"), y.get("p"), y.get("ap"), row[2],
                                                y.get("network").get("ope"), y.get("segmentation").get("App"),
                                                y.get("segmentation").get("Song"), y.get("segmentation").get("Album"),
                                                y.get("segmentation").get("PState"), "", "",
                                                y.get("segmentation").get("Source"), row[10], row[11],
                                                y.get("segmentation").get("Station"),
                                                y.get("segmentation").get("Duration"), row[7], row[3], row[4], "",
                                                artist_name, genre, education, ownership, ""])
                except Exception as e:
                    pass
        client.close()
        writeFile.close()
export_users_csv()

print("END : ", time.localtime(time.time()))


