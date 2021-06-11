#!/usr/bin/env python3

import pandas as pd
from datetime import datetime, timedelta
import sqlite3

df = pd.read_csv('~/Downloads/Bilbrist - Bilbrist.csv')
con = sqlite3.connect('db.sqlite')
cur = con.cursor()
days = {
    'Måndag': 'Monday', 'Tisdag': 'Tuesday', 'Onsdag': 'Wednesday', 'Torsdag': 'Thursday', 'Fredag': 'Friday',
    'Lördag': 'Saturday', 'Söndag': 'Sunday'
}
day_n = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 1, 'Sunday': 0
}
months = {
    'Maj': 'May', 'Juni': 'June'
}
month_n = {
    'May': 5, 'June': 6
}

rows = []
for index, row in df.iterrows():
    month = months[row[0].strip()]
    _month_n = month_n[month]
    day = days[row[1].strip()]
    _day_n = day_n[day]

    # Infer exact date from month and day
    start_date = datetime(2021, _month_n, 1, 1)
    test_day_n = start_date.weekday()
    while test_day_n != _day_n:
        start_date = start_date + timedelta(days=1)
        test_day_n = start_date.weekday()

    target_date = start_date
    hours, minutes, _ = row[2].split(':')
    hours = hours if len(hours) == 2 else '0' + hours
    time = hours + ':' + minutes
    target_timestamp = target_date.strftime('%Y-%m-%d') + ' ' + time
    district = row[3]
    rows.append((time, day, month, district, target_timestamp))

cur.executemany('INSERT INTO bilbrist VALUES (?, ?, ?, ?, ?)', rows)
con.commit()
con.close()
