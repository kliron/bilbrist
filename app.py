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

app = Flask(__name__, static_url_path='/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(32))
auth = HTTPBasicAuth()
DATABASE = 'db.sqlite'
QUERY_LIMIT = 50
district_extractor_rgx = re.compile(r'([0-9]{3})\s*[\{\[\(][^0-9.]*?rt', re.MULTILINE)
CSV_SEP = ','
RESULTS_DIR = 'results'
TOP_N_RESULTS = 20

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
    cur = get_db().cursor()
    cur.execute('SELECT COUNT(*) FROM bilbrist')
    total_rows = cur.fetchone()[0]
    total_pages = math.ceil(total_rows / QUERY_LIMIT)

    cur.execute('SELECT MAX(date) FROM bilbrist')
    latest_entry = cur.fetchone()[0]

    page = page if page > 0 else 1
    offset = 0 if page == 1 else (page - 1) * QUERY_LIMIT
    stmt = cur.execute(
        'SELECT time, day, month, district, date, rowid FROM bilbrist ORDER BY rowid DESC LIMIT ? OFFSET ?',
        (QUERY_LIMIT, offset))
    data = []
    for row in stmt:
        data.append(row)
    return render_template('index.html', data=data, page=page, total_pages=total_pages, latest_entry=latest_entry)


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
    cur.execute('SELECT time, day, district, date, rowid FROM bilbrist ORDER BY rowid DESC')
    rows = cur.fetchall()
    csv = '\n'.join([CSV_SEP.join([str(col) for col in row]) for row in rows])
    return Response(csv, mimetype='text/csv')


@app.route('/results', methods=['GET'])
@auth.login_required
def results():
    # Load all data
    con = get_db()
    cur = con.cursor()
    slurp = cur.execute('SELECT time, day, month, district, date, rowid From bilbrist')
    cols = [col[0] for col in slurp.description]
    df = pd.DataFrame.from_records(data=slurp.fetchall(), columns=cols)
    df.date = pd.to_datetime(df.date, format='%Y-%m-%d %H:%M')
    now = datetime.now()
    time_now = now.time()
    intervals = [('08:00', '11:59'), ('12:00', '15:59'), ('16:00', '19:59'), ('20:00', '23:59'), ('00:00', '03:59'), ('04:00', '07:59')]
    interval_now = None
    for interval in intervals:
        if datetime.strptime(interval[0], '%H:%M').time() <= time_now <= datetime.strptime(interval[1], '%H:%M').time():
            interval_now = interval[0] + ' - ' + interval[1]
            break

    # This is to be able to use `between_time()`
    df = df.set_index(['date'])
    eight_twelve = df.index.isin(df.between_time(intervals[0][0], intervals[0][1]).index)
    twelve_sixteen = df.index.isin(df.between_time(intervals[1][0], intervals[1][1]).index)
    sixteen_twenty = df.index.isin(df.between_time(intervals[2][0], intervals[2][1]).index)
    twenty_zero = df.index.isin(df.between_time(intervals[3][0], intervals[3][1]).index)
    zero_four = df.index.isin(df.between_time(intervals[4][0], intervals[4][1]).index)
    four_eight = df.index.isin(df.between_time(intervals[5][0], intervals[5][1]).index)

    df['interval'] = np.where(eight_twelve, '08:00 - 12:00',
                              np.where(twelve_sixteen, '12:00 - 16:00',
                                       np.where(sixteen_twenty, '16:00 - 20:00',
                                                np.where(twenty_zero, '20:00 - 00:00',
                                                         np.where(twenty_zero, '20:00 - 00:00',
                                                                  np.where(zero_four, '00:00 - 04:00',
                                                                           np.where(four_eight, '04:00 - 08:00',
                                                                                    'BUG! No time interval found')))))))

    # Sort by district, all days and all months
    all_freqs = df.groupby(['district']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    by_month = df.groupby(['district', 'month']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    by_day = df.groupby(['district', 'day']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    by_time = df.groupby(['district', 'interval']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    by_time_and_day = df.groupby(['district', 'interval', 'day']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    by_month_and_day = df.groupby(['district', 'month', 'day']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)

    this_month = by_month[by_month['month'] == calendar.month_name[now.month]]
    this_weekday = by_day[by_day['day'] == calendar.day_name[now.weekday()]]
    this_time = by_time[by_time['interval'] == interval_now]
    this_months_weekday = by_month_and_day[(by_month_and_day['month'] == calendar.month_name[now.month]) &
                                           (by_month_and_day['day'] == calendar.day_name[now.weekday()])]

    month = calendar.month_name[datetime.now().month]
    weekday = calendar.day_name[datetime.now().weekday()]

    # Can't get the code below to work
    # all_freqs.style.set_table_attributes("style='display:inline'").set_caption('All frequenices')
    # by_month.style.set_table_attributes("style='display:inline'").set_caption('Frequencies by month')
    # by_day.style.set_table_attributes("style='display:inline'").set_caption('Frequencies by day')
    # by_month_and_day.style.set_table_attributes("style='display:inline'").set_caption('Frequencies by month and day')
    # this_month.style.set_table_attributes("style='display:inline'").set_caption('Frequencies on ' + month)
    # this_weekday.style.set_table_attributes("style='display:inline'").set_caption('Frequencies on ' + weekday + 's')
    # this_months_weekday.style.set_table_attributes("style='display:inline'").set_caption('Frequenices on ' + month + ' ' + weekday + 's')

    data = {
        'all_freqs': all_freqs.head(TOP_N_RESULTS),
        'by_month': by_month.head(TOP_N_RESULTS),
        'by_day': by_day.head(TOP_N_RESULTS),
        'by_time': by_time.head(TOP_N_RESULTS),
        'by_time_and_day': by_time_and_day.head(TOP_N_RESULTS),
        'by_month_and_day': by_month_and_day.head(TOP_N_RESULTS),
        'this_month': this_month.head(TOP_N_RESULTS),
        'this_weekday': this_weekday.head(TOP_N_RESULTS),
        'this_time': this_time.head(TOP_N_RESULTS),
        'this_months_weekday': this_months_weekday.head(TOP_N_RESULTS)
    }

    return render_template('results.html', data=data, month=month, weekday=weekday, top_n=TOP_N_RESULTS)


if __name__ == "__main__":
    # To run in dev mode:
    # export FLASK_ENV=development
    # flask run --cert=ssl/cert.pem --key=ssl/key.pem
    app.run(ssl_context=('secrets/ssl/cert.pem', 'secrets/ssl/key.pem'))
