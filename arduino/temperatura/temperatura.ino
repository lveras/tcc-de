#include <Adafruit_Sensor.h>
#include "DHT.h"
#include <SPI.h>
#include <Ethernet.h>

#define DHTPIN A1
#define DHTTYPE DHT11
 
// Conecte pino 1 do sensor (esquerda) ao +5V
// Conecte pino 2 do sensor ao pino de dados definido em seu Arduino
// Conecte pino 4 do sensor ao GND
// Conecte o resistor de 10K entre pin 2 (dados) 
// e ao pino 1 (VCC) do sensor
DHT dht(DHTPIN, DHTTYPE);

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
char server[] = "192.168.12.141";
IPAddress ip(192,168,12,201);
EthernetClient client;
static char outstr[15];
String data;

void setup() 
{
  Serial.begin(9600);
  dht.begin();
  
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Falha ao configurar a ethernet usando DHCP");
    Serial.println("Tentando conectar com o IP Fixo: "+ip);
    Ethernet.begin(mac, ip);
  }
  
  delay(1000);
  Serial.println("connecting...");
}

void enviar()
{
  dtostrf(dht.readTemperature(),2, 0, outstr);
  String data="GET /t/1/";
  data=String(data + String(outstr));
  data=data+" HTTP/1.1";
  
  if (client.connect(server, 8080)) {
    Serial.println(data);
    client.println(data);
    client.println("Host: 192.168.12.141");
    client.println("Connection: close");
    client.println();
    client.stop();
  }
  else {
    Serial.println("connection failed");
  }
}

void loop() 
{
  // A leitura da temperatura e umidade pode levar 250ms!
  // O atraso do sensor pode chegar a 2 segundos.
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(t) || isnan(h)) 
  {
    Serial.println("Falha na leitura(Verifique cabos).");
  }
  else
  {
    enviar(); 
    delay(60000);
  }
}
