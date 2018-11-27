# -*- coding: utf-8 -*-

import csv
import datetime
import os
import pickle
from pathlib import Path

import pandas as pd
import colorlover as cl
import plotly.graph_objs as go
from bottle import route, run, template, post, request
from plotly.offline import plot

FILENAME = 'temperature.csv'
COLUNAS = ['Sensor', 'Temperatura', 'Horario']

PALETA = cl.scales['11']['div']['RdYlGn']
for x in range(0, 2):
    PALETA.remove(PALETA[4])
PALETA.reverse()


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


@route('/')
def do_index():
    return u'<a href="chart">Sensores</a> | <a href="config">Configurações</a>'


@route('/chart')
def do_chart():
    df_temperature = pd.read_csv('temperature.csv') if Path('temperature.csv').is_file() else []

    df_last = pd.DataFrame(columns=COLUNAS)

    param = load_obj('config')

    if len(df_temperature) == 0:
        return u'<p>Nenhum sensor encontrado</p>'

    for record in df_temperature['Sensor'].unique():
        df = df_temperature[df_temperature['Sensor'] == record]
        horario = df_temperature[df_temperature['Sensor'] == record].Horario.max()
        df_last.loc[len(df_last)] = df[df['Horario'] == horario].values.tolist()[0]

    rgb_list = slice_list(
        [convert_to_rgb(
            int(df_last.loc[i]['Temperatura']),
            int(param.get('minimo')[0]),
            int(param.get('maximo')[0])) for i in df_last.index])

    sensor_list = slice_list(
        [param.get(str(i+1))[0] + ': ' + str(df_last.loc[i]['Temperatura']) + ' ºC' for i in df_last.index])

    trace1 = go.Table({
        'cells': {
            'align': 'center',
            'fill': {'color': rgb_list},
            'font': {'color': 'white', 'size': 40},
            'height': 50,
            'line': {'color': rgb_list},
            'values': sensor_list,
        },
        "header": {
            "align": "center",
            "fill": {"color": "white"},
            "font": {"color": "black", "size": 12},
            "line": {"color": "white"},
            "values": ['']
        },
        "type": "table"
    })

    plot([trace1], auto_open=False)

    html = open('temp-plot.html', 'r')
    return template(html.read())


@post('/save-config')
def do_save_config():
    save_obj(request.forms.dict, 'config')
    return do_chart()


@route('/config')
def do_configuracoes():
    df_temperature = pd.read_csv('temperature.csv')

    response = '''
    <html>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" 
integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" 
integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous">
</script>


<body> 
<div class="center-block" style="width:50%;">
<p class='h1'>Configurações</p>
<p class='h3'>Temperatura mínima e máxima para alerta</p>
<form action="/save-config" method="post">
    <div class="form-group row">
        <label for="minimo" class="col-sm-2 col-form-label">Minimo</label>
        <div class="col-sm-10">
            <input type="number" value="20" class="form-control" id="minimo" name="minimo"/>
        </div>
    </div>

    <div class="form-group row">
        <label for="maximo" class="col-sm-2 col-form-label">Máximo</label>
        <div class="col-sm-10">
            <input type="number" value="25" class="form-control" id="maximo" name="maximo"/>
        </div>
    </div>
    
    <p class='h3'>Emails para alerta</p>
    <div class="form-group row">
        <label for="email1" class="col-sm-2 col-form-label">Email 1</label>
        <div class="col-sm-10">
            <input type="email" class="form-control" id="email1" name="email1"/>
        </div>
    </div>

    <div class="form-group row">
        <label for="email2" class="col-sm-2 col-form-label">Email 2</label>
        <div class="col-sm-10">
            <input type="email" class="form-control" id="email2" name="email2"/>
        </div>
    </div>

    <div class="form-group row">
        <label for="email3" class="col-sm-2 col-form-label">Email 3</label>
        <div class="col-sm-10">
            <input type="email" class="form-control" id="email3" name="email3"/>
        </div>
    </div>
    
    <p class='h3'>Trocar Label do Sensor</p>
'''

    for record in df_temperature['Sensor'].unique():
        response = response+'''
        
    <div class="form-group row">
        <label for="'''+str(record)+'''" class="col-sm-2 col-form-label">Sensor '''+str(record)+'''</label>
        <div class="col-sm-10">
            <input type="text" class="form-control" id="'''+str(record)+'''" name="'''+str(record)+'''" 
                    value="Sensor '''+str(record)+'''"/>
        </div>
    </div>'''

    response = response + '''
    <input class="btn btn-default" value="Atualizar" type="submit" />
</div>
</form>
</body>
</html>'''
    return response


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def slice_list(l, n=3):
    splited = []
    len_l = len(l)
    for i in range(n):
        start = int(i * len_l / n)
        end = int((i + 1) * len_l / n)
        splited.append(l[start:end])

    return splited


def convert_to_rgb(t, minimo, maximo):
    paleta = ((t - int(minimo)) * len(PALETA)) / (int(maximo)-int(minimo))
    paleta = len(PALETA)-1 if paleta >= (len(PALETA)-1) else paleta
    paleta = 0 if paleta <= 0 else paleta

    return PALETA[paleta]


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
