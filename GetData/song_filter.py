import psycopg2
from pyignite import Client
import json
from datetime import date, timedelta
import os
import base64
import datetime
import time
import re

nodes = [
    ('35.154.247.92', 10800),
    ('35.154.247.92', 10801),
]
conn = psycopg2.connect(dbname="VTIONData", host="vtionproddb.chgz4nqwpdta.ap-south-1.rds.amazonaws.com",
                        user="vtion", password="per4mance")
cur = conn.cursor()
client = Client()
client.connect(nodes)

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

def filter_song(song, app):
   
    if app == 'Amazon Music':
        pass
        if '%' in song or song.isdigit():
            return ["S"]
        else:
            if 'ñ' in song:
                song = song.replace('ñ', 'n')
            else:
                pass
        song = deEmojify(filter(remove_bdata(song).replace(')', '').replace('(', '')))
        
    elif app == 'Spotify' or 'Spot' in app:
        if '%' in song:
            return ["S"]
        else:
            song = filter(deEmojify(remove_bdata(song))) 
                
    elif app == 'Gaana':
        if 'Gaana' in song or song.isdigit() or song ==',':
            return ["S"]
        else:
            if 'ñ' in song or '├▒' in song:
                song = song.replace('ñ', 'n').replace('├▒', 'n')
            else:
                pass
        song = select_before_list(remove_bdata(deEmojify(song))).lstrip('Ep 0123456789-.')
    
    elif app == 'Google Play Music':
        if song.isdigit() or 'high quality' in song or song == ',':
            return ["S"] 
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
            return ["S"] 
        song = deEmojify(select_before_list(filter(domain(remove_bdata(song))).lstrip(' 0123456789.-').strip())).strip()
        
    elif app == 'JioSaavn':
        song = filter(remove_bdata(song))
    
    elif app =='Saavn':
        song = filter(domain(remove_bdata(song)))
        app = 'JioSaavn'
    
    elif app == 'MX Player' :
        if '--:--:--' in song or 'Insufficient balance' in song or 'Expiry Date' in song :
            return ["S"]
        else:
            song = deEmojify(filter(remove_bdata(song)).replace('  ',' ')).strip()
        
    elif app == 'Music Player':       
        song = domain(filter(remove_bdata(song))).replace('  ',' ').lstrip(' 0123456789.-').strip()
        
    elif app == 'Wynk Music':
        song = remove_bdata(deEmojify(song)).lstrip(' 0123456789.-').strip()
        if song.isdigit() or '%' in song:
            return ["S"]
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
        
    return [song, app];