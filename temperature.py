# -*- coding: utf-8 -*-

import csv
import datetime
import os
import pickle
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import colorlover as cl
import pandas as pd
import plotly.graph_objs as go
from bottle import route, run, template, post, request
from pathlib import Path
from plotly.offline import plot

FILENAME = 'temperature.csv'
COLUNAS = ['Sensor', 'Temperatura', 'Horario']

PALETA = cl.scales['5']['seq']['YlGn'][1:]


@route('/t/<sensor>/<temperatura>')
def get_temperature(sensor, temperatura):
    if not Path('temperature.csv').is_file():
        with open(FILENAME, 'a') as csvfile:
            csvfile.write('Sensor,Temperatura,Horario\n')

    with open(FILENAME, 'a') as csvfile:
        if csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=COLUNAS)
            writer.writerow({'Sensor': sensor, 'Temperatura': temperatura, 'Horario': str(datetime.datetime.now())})

        else:
            writer = csv.DictWriter(csvfile, fieldnames=COLUNAS)
            writer.writerow({'Sensor': 'Sensor', 'Temperatura': 'Temperatura', 'Horario': 'Horario'})

        check_temperature(sensor=check_exist(p=sensor, default=sensor), temperatura=int(temperatura))


@route('/table_plot')
def do_table_plot():
    df_temperature = pd.read_csv('temperature.csv') if Path('temperature.csv').is_file() else []

    df_last = pd.DataFrame(columns=COLUNAS)

    if len(df_temperature) == 0:
        return u'<p>Nenhum sensor encontrado</p>'

    for record in df_temperature["Sensor"].unique():
        df = df_temperature[df_temperature["Sensor"] == record]
        horario = df_temperature[df_temperature["Sensor"] == record].Horario.max()
        df_last.loc[len(df_last)] = df[df["Horario"] == horario].values.tolist()[0]

    rgb_list = []

    df_last.set_index('Sensor', inplace=True)

    for i in df_last.index:
        minimo = int(check_exist(p='min_'+str(i), default='min_geral'))
        maximo = int(check_exist(p='max_'+str(i), default='max_geral'))
        rgb_list.append(convert_to_rgb(t=df_last.loc[i]['Temperatura'], minimo=minimo, maximo=maximo))

    rgb_list = slice_list(rgb_list)

    sensor_list = slice_list(
        [check_exist(str(i), 'S'+str(i)) + '<br />' +
         str(df_last.loc[i]['Temperatura']) + ' ºC' for i in df_last.index])

    trace1 = go.Table({
        'cells': {
            'align': 'center',
            'fill': {'color': rgb_list},
            'font': {'color': 'white', 'size': 15},
            'height': 20,
            'line': {'color': "#fff"},
            'values': sensor_list,
        },
        "header": {
            "align": "center",
            "fill": {"color": "white"},
            "font": {"color": "black", "size": 12},
            "line": {"color": "white"},
            "values": ['']
        },
        "columnwidth":100,
        "type": "table"
    })

    plot([trace1], auto_open=False)

    html = open('temp-plot.html', 'r')
    return template(html.read())


@route('/')
def do_index():
    return template('views/index')


@post('/save-config')
def do_save_config():
    save_obj(request.forms.dict, 'config')
    return do_configuracoes(save=True)


@route('/config')
def do_configuracoes(save=False):
    df_temperature = pd.read_csv('temperature.csv')

    min_geral = int(check_exist(p='min_geral', default=20))
    max_geral = int(check_exist(p='max_geral', default=25))

    smtp_server = str(check_exist(p='smtp_server', default=''))
    smtp_port = str(check_exist(p='smtp_port', default=''))
    smtp_email = str(check_exist(p='smtp_email', default=''))
    smtp_password = str(check_exist(p='smtp_password', default=''))
    send_emails = str(check_exist(p='send_emails', default=''))

    list_sensores = []

    for s in df_temperature['Sensor'].unique():
        s = str(s)
        list_sensores.append([s, str(check_exist(p='label_'+s, default=str('S'+s))),
                              str(check_exist(p='min_'+s, default='min_geral')),
                              str(check_exist(p='max_'+s, default='max_geral')), ])

    return template('views/config', s=save, min_geral=min_geral, max_geral=max_geral, smtp_server=smtp_server,
                    smtp_port=smtp_port, smtp_email=smtp_email, smtp_password=smtp_password, send_emails=send_emails,
                    list_sensores=list_sensores)


def check_exist(p, default=''):
    param = load_obj('config')
    p = str(param.get(p)[0]) if p in param else False
    default = str(param.get(default)[0]) if default in param else default

    return p or default


def send_email(sensor, temperatura):
    temperatura = str(temperatura)

    fromaddr = check_exist(p='smtp_email')
    toaddr = check_exist('send_emails')
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Sensor: "+sensor+" | Temperatura: "+temperatura

    body = 'Sensor: ' + sensor + ' | Temperatura: ' + temperatura
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(check_exist(p='smtp_server'), check_exist(p='smtp_port'))
    server.ehlo()
    server.starttls()
    server.login(fromaddr, check_exist('smtp_password'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def check_temperature(sensor, temperatura):
    minima = int(check_exist('min_'+str(sensor), 'min_geral'))
    maxima = int(check_exist('max_'+str(sensor), 'max_geral'))

    if temperatura <= minima or temperatura >= maxima:
        send_email(sensor=sensor, temperatura=temperatura)


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    if not Path('obj/' + name + '.pkl').is_file():
        save_obj({'min_geral': ['20'], 'max_geral': ['25'], }, 'config')

    with open('obj/' + name + '.pkl', 'rw') as f:
        return pickle.load(f)


def slice_list(l, maxcols=5):
    splited = []
    len_l = len(l)
    n = max([i if len_l % i is 0 else 0 for i in range(1, maxcols)])
    for i in range(n):
        start = int(i * len_l / n)
        end = int((i + 1) * len_l / n)
        splited.append(l[start:end])

    return splited


def convert_to_rgb(t, minimo, maximo):
    if t < minimo or t > maximo:
        return 'rgb(255,0,0)'

    if t == minimo or t == maximo:
        return 'rgb(255,128,0)'

    max_min = int(maximo) - int(minimo) or 1
    paleta = ((int(t) - int(minimo)) * len(PALETA)) / max_min
    paleta = len(PALETA) - 1 if paleta >= (len(PALETA) - 1) else paleta
    paleta = 0 if paleta <= 0 else paleta

    return PALETA[paleta]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
