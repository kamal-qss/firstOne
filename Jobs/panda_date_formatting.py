import pandas as pd
from datetime import date, timedelta
import numpy as np

file_read = pd.read_csv('/home/dhananjai/Desktop/remove_id_with_date.csv', low_memory=False)
file_read['event_date'] = file_read['event_date'].astype(str)
file_read['event_date'] = file_read['event_date'].str[4:6]+ '/'+file_read['event_date'].str[6:8] +'/'+file_read['event_date'].str[:4]
file_read.to_csv('/home/dhananjai/Desktop/uninstall_data_with-date.csv',index=False)