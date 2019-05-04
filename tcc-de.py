# -*- coding: utf-8 -*-

import os
from bottle import route, run, template
from plotly.offline import plot
import sqlite3
from datetime import datetime, timedelta

import plotly.graph_objs as go

DATABASE = 'database.db'


def get_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS tb_afericao("
              "id INTEGER PRIMARY KEY, "
              "sensor INTEGER NOT NULL, val FLOAT NOT NULL, "
              "create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    return c, conn


def exec_query(query):
    c, conn = get_db()
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result


@route('/t/<sensor>/<val>')
def set_val(sensor, val):
    exec_query("INSERT INTO tb_afericao(sensor, val) VALUES({}, {})".
               format(sensor, val))


@route('/table_plot')
def do_table_plot():
    def get_val_sensor(h, s):
        query = "SELECT val FROM tb_afericao WHERE " \
                "strftime('%d-%m-%Y %H:%M', create_date) = \"{}\" " \
                "AND sensor = {}".format(h, s)
        val = exec_query(query)

        return val[0][0] if val else 0

    query = "SELECT strftime('%Y-%m-%d %H', create_date), max(id) " \
            "FROM tb_afericao"
    ult_hora = exec_query(query=query)

    penult_hora = str(23) if int(ult_hora[0][0][-2:]) == 0 \
        else str(int(ult_hora[0][0][-2:])-1).zfill(2)

    penult_data = "{} {}".format(
        (datetime.strptime(ult_hora[0][0][0:10], "%Y-%m-%d") -
         timedelta(days=1)).strftime("%Y-%m-%d"), penult_hora)

    query = "SELECT distinct strftime('%d-%m-%Y %H:%M', create_date) " \
            "FROM tb_afericao WHERE strftime('%Y-%m-%d %H',create_date) like "\
            "'%{}%' OR strftime('%Y-%m-%d %H',create_date) like '%{}%'".format(
        ult_hora[0][0], penult_data)

    datas = exec_query(query=query)

    sensores = exec_query("SELECT distinct sensor FROM tb_afericao")

    y = [data[0][-5:] for data in datas]

    sens = []

    for sensor in sensores:
        sens.append(go.Scatter(
            name='Sensor {}'.format(sensor[0]),
            x=y,
            y=[get_val_sensor(data[0], sensor[0]) for data in datas],
        ))

    plot(figure_or_data=go.Figure(data=sens),
         auto_open=False)

    html = open('temp-plot.html', 'r')

    return template(html.read())


@route('/')
def do_index():
    return template('views/index')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
