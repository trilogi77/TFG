#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
const char* ssid     = "#####";
const char* password = "#####";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;
char incomingPacket[256];
char replyPacket[] = "Hi there! Got the message :-)";
int total;





//https://arduino-esp8266.readthedocs.io/en/latest/esp8266wifi/udp-examples.html




void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(10);
  total=0
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Conectando a:\t");
  Serial.println(ssid);

  // Esperar a que nos conectemos
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(200);
   Serial.print('.');
  }

  // Mostrar mensaje de exito y dirección IP asignada
  Serial.println();
  Serial.print("Conectado a:\t");
  Serial.println(WiFi.SSID());
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
  Udp.begin(localUdpPort);

  Serial.println("Sending pacages to 192.168.1.37");
}

void loop() {
  // put your main code here, to run repeatedly:

  //String ip = "192.168.1.37"; // the remote IP address
  Udp.beginPacket("192.168.1.37", 8554);
  total=total+1;
  Udp.write(replyPacket);
  Udp.endPacket();
  Serial.println(total);
}
