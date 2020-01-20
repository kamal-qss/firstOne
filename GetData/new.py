from pyignite import Client

nodes = [
    ('35.154.247.92', 10800),
    ('35.154.247.92', 10801),
]

client = Client()
client.connect(nodes)

QUERY = ''' SELECT ID, APPID, EVENTS, DEVICE_ID, "TIMESTAMP", MTIMESTAMP, UPTIMESTAMP, IPADDRESS, CITY, 
                COUNTRY, EVENTNAME, CREATED_DATE, CREATED_TIME FROM PUBLIC.EVENTSDATA WHERE 
                "TIMESTAMP" > '{}' AND "TIMESTAMP" < '{}' ;'''