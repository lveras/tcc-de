# temperature

Sistema para aferição de temperatura multi pontos.

### Técnico

O temperature utiliza vários projetos de código aberto para funcionar corretamente:

* [bottlepy](https://bottlepy.org) - micro web-framework em python.
* [pandas](https://pandas.pydata.org) - Biblioteca em python para estrutura e analise de dados.
* [plotly](https://plot.ly) - Ferramenta de analise e exibição de dados.
* [arduino](https://www.arduino.cc) - Plataforma de prototipagem eletrônica de hardware livre e de placa única.
    * [arduino - Ethernet Shield](https://www.arduino.cc/en/Reference/Ethernet) - Shield de ethernet para arduino.
    * [arduino - DH11](https://www.mouser.com/ds/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf) Sensor
     de temperatura e humidade.
    


### Instalação

Baixando o programa do repositório
```sh
git clone git@github.com:lveras/temperature.git
```


Criação de virtualenv em python 2.7

```sh
$ cd temperature
$ virtualenv . --python=/usr/bin/python2.7
$ source bin/active
```

Dependências

```sh
$ pip install bottle
$ pip install pandas
$ pip install pickle
$ pip install colorlover
$ pip install pathlib
$ pip install plotly
```


### Arduino
O código do arduino esta dentro do projeto. É necessário alterar parâmentros de acordo com o seu ambiente.