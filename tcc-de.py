# -*- coding: utf-8 -*-

import os
from bottle import route, run, template
from plotly.offline import plot
import sqlite3

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

    datas = exec_query("SELECT distinct strftime('%d-%m-%Y %H:%M', "
                       "create_date) FROM tb_afericao")

    sensores = exec_query("SELECT distinct sensor FROM tb_afericao")

    y = [data[0] for data in datas]

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
