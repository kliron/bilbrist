from flask import Flask, request, url_for, redirect, render_template, flash, g, Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import math
import sqlite3
import secrets
import string
import calendar
import pandas as pd
import numpy as np
from typing import Dict, List
from district_names import district_names

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

app = Flask(__name__, static_url_path='/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(32))
auth = HTTPBasicAuth()
DATABASE = 'db.sqlite'
QUERY_LIMIT = 50
district_extractor_rgx = re.compile(r'([0-9]{3})\s*[\{\[\(][^0-9.]*?rt', re.MULTILINE)
CSV_SEP = ','
RESULTS_DIR = 'results'
TOP_N_RESULTS = 40

with open('secrets/httpauth.txt', 'r') as f:
    passw = f.read().replace('\n', '')

users = {
    "giannis": generate_password_hash(passw)
}


def get_db():
    con = getattr(g, '_database', None)
    if con is None:
        con = g._database = sqlite3.connect(DATABASE)
    return con


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/', defaults={'page': 0})
@app.route('/<int:page>')
@auth.login_required
def root(page):
    sortable = ['rowid', 'time', 'day', 'month', 'district', 'date']
    order_by = request.args.get('o')
    order_by = order_by if order_by in sortable else sortable[0]
    cur = get_db().cursor()
    cur.execute('SELECT COUNT(*) FROM bilbrist')
    total_rows = cur.fetchone()[0]
    total_pages = math.ceil(total_rows / QUERY_LIMIT)

    cur.execute('SELECT MAX(date) FROM bilbrist')
    latest_entry = cur.fetchone()[0]

    page = page if page > 0 else 1
    offset = 0 if page == 1 else (page - 1) * QUERY_LIMIT
    stmt = cur.execute(
        f'SELECT time, day, month, district, date, rowid FROM bilbrist ORDER BY {order_by} DESC LIMIT ? OFFSET ?',
        (QUERY_LIMIT, offset))
    data = []
    for row in stmt:
        data.append(row)
    return render_template('index.html',
                           data=data,
                           page=page,
                           total_pages=total_pages,
                           latest_entry=latest_entry,
                           district_names=district_names)


@app.route('/new_post', methods=['POST'])
@auth.login_required
def new_post():
    con = get_db()
    cur = con.cursor()
    posting = request.form['posting']
    # Different entries should be separated by at least one empty line
    entries = re.split(r'\n{2,}', posting)
    now = datetime.now()
    day = calendar.day_name[now.weekday()]
    month = calendar.month_name[now.month]
    for entry in entries:
        if not entry or entry.isspace():
            continue
        t = re.search(r'([0-9]{2})([0-9]{2})\s*BILBRIST', entry)
        if t is None or not len(t.groups()) == 2:
            flash('Could not parse time from posting', category='error')
            continue
        time_t = t.group(1) + ':' + t.group(2)
        districts = []
        for m in re.finditer(district_extractor_rgx, posting):
            districts.append(m.group(1))
        if not districts:
            flash('Did not find any `rt` entries in posting', category='error')
            continue
        rows = [(time_t, day, month, district, now.strftime('%Y-%m-%d %H:%M')) for district in districts]
        cur.executemany('INSERT INTO bilbrist VALUES (?, ?, ?, ?, ?)', rows)
        con.commit()
        flash(f'Saved {len(rows)} entries.', category='message')

    return redirect(url_for('root'))


@app.route('/save_post', methods=['POST'])
@auth.login_required
def save_post():
    now = datetime.now()
    time = now.strftime('%H:%M')
    day = calendar.day_name[now.weekday()]
    month = calendar.month_name[now.month]
    district = request.form['district'] or 'INVALID'
    district = district if re.match(r'[0-9]+', district) else 'INVALID'
    now = datetime.now()
    con = get_db()
    cur = con.cursor()
    cur.execute('INSERT INTO bilbrist VALUES (?, ?, ?, ?, ?)', [time, day, month, district, now])
    con.commit()
    flash(f'Saved 1 entry.', category='message')
    return redirect(url_for('root'))


@app.route('/delete_post', methods=['POST'])
@auth.login_required
def delete_post():
    page = request.form['page']
    rowid = request.form['rowid']
    con = get_db()
    cur = con.cursor()
    cur.execute('DELETE FROM bilbrist WHERE rowid = ?', [rowid])
    con.commit()
    return redirect(url_for('root', page=page))


@app.route('/edit_post/<int:rowid>', methods=['GET'])
@auth.login_required
def edit_post(rowid):
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT time, date, district, rowid FROM bilbrist WHERE rowid = ?', [rowid])
    row = cur.fetchone()
    return render_template('edit_post.html', row=row)


@app.route('/do_edit_post/<int:rowid>', methods=['POST'])
@auth.login_required
def do_edit_post(rowid):
    time = request.form['time']
    date = request.form['date']
    dt = None
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
    except ValueError as e:
        flash(f'Could not parse `{date}`. Dates must be in YYYY-MM-DD format.')
        return redirect(url_for('edit_post', rowid=rowid))

    day = calendar.day_name[dt.weekday()]

    m = re.match(r'[0-9]{2}:[0-9]{2}', time)
    if m is None:
        flash(f'Could not parse `{time}`. Time must be in HH:MM format.')
        return redirect(url_for('edit_post', rowid=rowid))

    date += (' ' + time)
    district = request.form['district'] or 'INVALID'
    district = district if re.match(r'[0-9]+', district) else 'INVALID'
    con = get_db()
    cur = con.cursor()
    cur.execute('UPDATE bilbrist SET time = ?, day = ?, district = ?, date = ? WHERE rowid = ?',
                [time, day, district, date, rowid])
    con.commit()
    return redirect(url_for('root'))


@app.route('/download', methods=['GET'])
@auth.login_required
def download():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT time, day, month, district, date, rowid FROM bilbrist ORDER BY rowid DESC')
    rows = cur.fetchall()
    colnames = CSV_SEP.join([desc[0] for desc in cur.description])
    csv = colnames + '\n' + '\n'.join([CSV_SEP.join([str(col) for col in row]) for row in rows])
    return Response(csv, mimetype='text/csv')


@app.route('/results', methods=['GET'])
@auth.login_required
def results():
    district = request.args.get('d')
    if not district or not re.match(r'^[0-9]+$', district):
        district = None

    con = get_db()
    cur = con.cursor()
    sql = 'SELECT time, day, month, district, date, rowid From bilbrist' if district is None else \
        'SELECT time, day, month, district, date, rowid From bilbrist where district = ?'
    params = [] if district is None else [district]
    res = cur.execute(sql, params)
    cols = [col[0] for col in res.description]
    df = pd.DataFrame.from_records(data=res.fetchall(), columns=cols)

    # Concatenate area code and district name since they are 1-to-1 mappings, they are essentially a single variable
    areas = df['district'].apply(lambda d: district_names.get(d, ['Unknown'])[0])
    df['district'] = df['district'] + ' - ' + areas
    
    df.date = pd.to_datetime(df.date, format='%Y-%m-%d %H:%M')
    now = datetime.now()
    time_now = now.time()
    intervals = [('00:00', '01:00'), ('01:00', '02:00'), ('02:00', '03:00'), ('03:00', '04:00'), ('04:00', '05:00'),
                 ('05:00', '06:00'), ('06:00', '07:00'), ('07:00', '08:00'), ('08:00', '09:00'), ('09:00', '10:00'),
                 ('10:00', '11:00'), ('11:00', '12:00'), ('12:00', '13:00'), ('13:00', '14:00'), ('14:00', '15:00'),
                 ('15:00', '16:00'), ('16:00', '17:00'), ('17:00', '18:00'), ('18:00', '19:00'), ('19:00', '20:00'),
                 ('20:00', '21:00'), ('21:00', '22:00'), ('22:00', '23:00'), ('23:00', '00:00')]
    interval_now = None
    for interval in intervals:
        if datetime.strptime(interval[0], '%H:%M').time() <= time_now <= datetime.strptime(interval[1], '%H:%M').time():
            interval_now = interval[0] + ' - ' + interval[1]
            break

    # This is to be able to use `between_time()`
    df = df.set_index(['date'])
    mask = [df.index.isin(df.between_time(intervals[i][0], intervals[i][1], include_start=True, include_end=False).index) for i in range(0, len(intervals))]

    df['interval'] = np.where(mask[0], ' - '.join(intervals[0]),
                              np.where(mask[1], ' - '.join(intervals[1]),
                                       np.where(mask[2], ' - '.join(intervals[2]),
                                                np.where(mask[3], ' - '.join(intervals[3]),
                                                         np.where(mask[4], ' - '.join(intervals[4]),
                                                                  np.where(mask[5], ' - '.join(intervals[5]),
                                                                           np.where(mask[6], ' - '.join(intervals[6]),
                                                                                    np.where(mask[7], ' - '.join(intervals[7]),
                                                                                             np.where(mask[8], ' - '.join(intervals[8]),
                                                                                                      np.where(mask[9], ' - '.join(intervals[9]),
                                                                                                               np.where(mask[10], ' - '.join(intervals[10]),
                                                                                                                        np.where(mask[11], ' - '.join(intervals[11]),
                                                                                                                                 np.where(mask[12], ' - '.join(intervals[12]),
                                                                                                                                          np.where(mask[13], ' - '.join(intervals[13]),
                                                                                                                                                   np.where(mask[14], ' - '.join(intervals[14]),
                                                                                                                                                            np.where(mask[15], ' - '.join(intervals[15]),
                                                                                                                                                                     np.where(mask[16], ' - '.join(intervals[16]),
                                                                                                                                                                              np.where(mask[17], ' - '.join(intervals[17]),
                                                                                                                                                                                       np.where(mask[18], ' - '.join(intervals[18]),
                                                                                                                                                                                                np.where(mask[19], ' - '.join(intervals[19]),
                                                                                                                                                                                                         np.where(mask[20], ' - '.join(intervals[20]),
                                                                                                                                                                                                                  np.where(mask[21], ' - '.join(intervals[21]),
                                                                                                                                                                                                                           np.where(mask[22], ' - '.join(intervals[22]),
                                                                                                                                                                                                                                np.where(mask[23], ' - '.join(intervals[23]),
                                                                                                                                                                                                                                        'BUG! No time interval found'))))))))))))))))))))))))

    # Sort by district, all days and all months
    all_freqs = df.groupby(['district']).size().reset_index(name='counts')
    # Percent of all frequencies
    all_freqs['%'] = round(100 * all_freqs['counts'] / all_freqs['counts'].sum(), 2)
    all_freqs['percentile'] = pd.qcut(all_freqs['%'], q=100, labels=False, duplicates='drop')
    all_freqs.sort_values(by='%', inplace=True, ascending=False)

    def calculate_grouped_percentage_and_centile(d: pd.DataFrame, group_by: List[str]) -> pd.DataFrame:
        d_pct = d.groupby(group_by).agg({'counts': 'sum'})\
            .groupby(level=0).apply(lambda g: round(100*g/g.sum(), 2))\
            .rename(columns={'counts': '%'})\
            .reset_index()
        d = d.merge(d_pct, how='inner', on=group_by)
        d['percentile'] = pd.qcut(d['%'], q=100, labels=False, duplicates='drop')
        return d

    by_day = df.groupby(['district', 'day']).size().reset_index(name='counts')
    # Percent of each district for each day, calculated by the total of all districts for that day
    by_day = calculate_grouped_percentage_and_centile(by_day, group_by=['day', 'district'])
    # Create a day ordering list so that the first day is today. 
    def _reorder(lst: List, idx: int) -> List:
        n = len(lst)
        if idx > n:
            raise RuntimeError(f'Index {idx} out of range (0-{n-1})')
        if idx == 0:
            return lst
        return lst[idx:] + lst[0:idx]

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Make day a categorical variable and set order so that we can show results sorted from Monday to Sunday
    by_day['day'] = pd.Categorical(by_day['day'], _reorder(days, now.weekday()))
    by_day.sort_values(by=['day', '%'], ascending=[True, False], inplace=True)

    by_time = df.groupby(['district', 'interval']).size().reset_index(name='counts')
    # Percent of each district for each time interval, calculated by the total of all districts for that time interval
    by_time = calculate_grouped_percentage_and_centile(by_time, group_by=['interval', 'district'])
    # Same as above, make current interval the first interval
    intervals_str = [i[0] + ' - ' + i[1] for i in intervals]
    by_time['interval'] = pd.Categorical(by_time['interval'], _reorder(intervals_str, intervals_str.index(interval_now)))
    by_time.sort_values(by=['interval', '%'], ascending=[True, False], inplace=True)

    by_time_and_day = df.groupby(['district', 'interval', 'day']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    by_time_and_day['interval'] = pd.Categorical(by_time_and_day['interval'], _reorder(intervals_str, intervals_str.index(interval_now)))
    by_time_and_day['day'] = pd.Categorical(by_time_and_day['day'], _reorder(days, now.weekday()))
    by_time_and_day.sort_values(by=['day', 'interval', 'counts'], ascending=[True, True, False], inplace=True)

    by_month_and_day = df.groupby(['district', 'month', 'day']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    by_month_and_day['month'] = pd.Categorical(by_month_and_day['month'], _reorder(months, now.month-1))
    by_month_and_day['day'] = pd.Categorical(by_month_and_day['day'], _reorder(days, now.weekday()))
    by_month_and_day.sort_values(by=['month', 'day', 'counts'], ascending=[True, True, False], inplace=True)

    month = calendar.month_name[datetime.now().month]
    weekday = calendar.day_name[datetime.now().weekday()]

    data = {
        'by_day': by_day,
        'by_time': by_time,
        'by_time_and_day': by_time_and_day,
        'by_month_and_day': by_month_and_day,
        'all_freqs': all_freqs
    }

    return render_template('results.html', data=data, month=month, weekday=weekday, top_n=TOP_N_RESULTS, district=district)


@app.route('/results_for_district', methods=['POST'])
@auth.login_required
def results_for_district():
    district = request.form['district']
    return redirect(f'/results?d={district}')


if __name__ == "__main__":
    # To run in dev mode:
    # export FLASK_ENV=development
    # flask run --cert=ssl/cert.pem --key=ssl/key.pem
    app.run(ssl_context=('secrets/ssl/cert.pem', 'secrets/ssl/key.pem'))
