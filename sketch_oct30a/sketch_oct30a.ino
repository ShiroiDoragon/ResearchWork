#include<ESP8266WiFi.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>
#define WIFI_SSID "Net" // название WiFi
#define WIFI_PASS "8B9" //пароль от WiFi
#define code 3772784863 //кодовый сигнал 

IRrecv irrecv(5);
decode_results results;
//byte num = 0;
char* host = "192.168.1.45"; //ip сервера
uint16_t port = 3030; //порт для подключения к серверу
int num = 0;
int nummax = 18; //количество позиций камеры

void setup() {
  Serial.begin(9600);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  delay(3000);
  
  pinMode(LED_BUILTIN, OUTPUT);
  irrecv.enableIRIn();
}

void loop() {
  WiFiClient client;
  if (client.connect(host, port))
      {
        delay(1000);
        Serial.println("connect");
      }
  if (client.connected())
      {
        String str = "";
        client.print(str+num);
        delay(5000);
        if (Check())
        {
          digitalWrite( LED_BUILTIN, LOW );
          while (Check())
          {    
            Serial.println("Wait");      
            delay(20000);
            irrecv.resume();
          }          
        }
        else
          digitalWrite( LED_BUILTIN, HIGH );
        if (num!=nummax)
          num += 1; 
        else
          num = 0;   
        delay(2000);
        //client.stop();
        
      }
  delay(100);
}

bool Check()//проверка сигнала
{
  int N=50; //количество проверок сигнала
  bool checkConnect = false;
  for (int i=0; i<N; i++)
  {
    if (irrecv.decode( &results ))
        if (results.value == code)
        {
          Serial.println(results.value);
          checkConnect = true;
          break;
        }        
      delay(10);
      Serial.println("check");
  }
  return checkConnect;
}
