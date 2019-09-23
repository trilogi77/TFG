#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266Ping.h>

const char* ssid     = "######";
const char* password = "#######";

const char* host = "192.168.1.38";
int total;

void setup()
{
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  total=0;
  Serial.println(" connected");
}


void loop()
{
  //Ping.ping(host);
  WiFiClient client;
  total=total +1;
  client.connect(host, 80);
  Serial.println(total);
}
