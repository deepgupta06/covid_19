#include <SPI.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define WLAN_SSID       "--Your SSID--"
#define WLAN_PASS       "--Your Wifi Password--"

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883               
#define AIO_USERNAME    "yobots"
#define AIO_KEY         "83a80786ecc642919bcff59eb15548c2"
#define delay_time 2500
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
Adafruit_MQTT_Subscribe covid_19 = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/covid-19");
void MQTT_connect();
Adafruit_PCD8544 display = Adafruit_PCD8544(D5, D7, D6, D1, D2);

String intro = "COVID-19";
String country1[9],country2[9],country3[9],country4[9],country5[9],country6[9],country7[9],country8[9],country9[9],country10[9],global[9],custome_country[9];


void setup() 
{
  Serial.begin(9600);
  display.begin();
  display.setContrast(50);
  display.clearDisplay();
  display.setTextWrap(false);
  display.display();
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: "); 
  Serial.println(WiFi.localIP());
  mqtt.subscribe(&covid_19);

}

uint32_t x=0;

void loop() 
{
  String country_data;
  MQTT_connect();
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) 
  {
    if (subscription == &covid_19) 
    {
      country_data = ((char *)covid_19.lastread);
      
      Serial.println((char *)covid_19.lastread);
      int underscore_position[9];
      underscore_position[0]=0;
      int underscore = 0;
      String data[9];
      
      for (int i=1; i<=8; i++)
      {
        underscore_position[i] = country_data.indexOf("_", underscore+1)+1;
        underscore = underscore_position[i];
        Serial.println(underscore_position[i]);
      }
      for (int i=0; i<=8; i++)
      {
        int country_index = country_data.substring(underscore_position[0],underscore_position[1]-1).toInt();
        
        switch (country_index)
        {
          case 1:
          country1[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country1[i]);
          break;
          case 2:
          country2[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country2[i]);
          break;
          case 3:
          country3[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country3[i]);
          break;
          case 4:
          country4[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country4[i]);
          break;
          case 5:
          country5[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country5[i]);
          break;
          case 6:
          country6[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country6[i]);
          break;
          case 7:
          country7[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country7[i]);
          break;
          case 8:
          country8[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country8[i]);
          break;
          case 9:
          country9[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country9[i]);
          break;
          case 10:
          country10[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(country10[i]);
          break;
          case 11:
          global[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(global[i]);
          break;
          case 12:
          custome_country[i]= country_data.substring(underscore_position[i],underscore_position[i+1]-1);
          Serial.println(custome_country[i]);
          break;
        }
      }
      display_text(global);
      delay(delay_time);
      display_text(custome_country);
      delay(delay_time);
    }
  
  }
  display_text(global);
  delay(delay_time);
  display_text(custome_country);
  delay(delay_time);
  display_text(country1);
  delay(delay_time);
  display_text(country2);
   delay(delay_time);
  display_text(country3);
   delay(delay_time);
  display_text(country4);
   delay(delay_time);
  display_text(country5);
   delay(delay_time);
  display_text(country6);
   delay(delay_time);
  display_text(country7);
   delay(delay_time);
  display_text(country8);
   delay(delay_time);
  display_text(country9);
   delay(delay_time);
  display_text(country10);

}

void textscroll(String text)
{
  int textWidth = text.length()*17+90;
  for(int i=0; i<textWidth; i+=1) 
  {
    display.clearDisplay();
    display.drawRect(0, 0, 84, 48, BLACK);
    display.fillRect(0, 0, 84, 48, BLACK);
    for(int j=0; j<text.length(); j++) 
    {
      display.drawChar((j*17)+90-i,map(j,-100,100,20,20), text[j], WHITE, WHITE, 3);
    }
    display.display();
    delay(20);    
  }  
}

void MQTT_connect() 
{
  int8_t ret;
  if (mqtt.connected()) 
  {
    return;
  }
  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) 
  { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
  }

  void display_text(String data[9])
  {
    display.clearDisplay();
    display.drawRect(0, 0, 84, 48, BLACK);
    //display.drawLine(38,10,38,48, BLACK);
    display.drawLine(0,10,84,10, BLACK);
    display.setTextSize(1);
    display.setCursor(10,2);
    display.println(data[1]);
    display.setCursor(2,12);
    display.println("Total="+data[2]);
    display.setCursor(2,21);
    display.println("Active=" + data[7]);
    display.setCursor(2,30);
    display.println("Rcvrd=" + data[6]);
    display.setCursor(2,39);
    display.println("Death="+data[3]);
    display.display();
    delay(delay_time);
    display.clearDisplay();
    display.drawRect(0, 0, 84, 48, BLACK);
    //display.drawLine(38,10,38,48, BLACK);
    display.drawLine(0,10,84,10, BLACK);
    display.setTextSize(1);
    display.setCursor(10,2);
    display.println(data[1]);
    display.setCursor(2,12);
    display.println("NW cases="+data[3]);
    display.setCursor(2,21);
    display.println("NW Death=" + data[5]);
    display.setCursor(2,30);
    display.println("Death Rate=" + data[5]+"%");
    display.display();
  }
