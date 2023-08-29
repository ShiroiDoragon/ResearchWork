#define WIFI_SSID "ShiroiDoragon" // название WiFi
#define WIFI_PASS "ADEK951753159357" //пароль от WiFi
#define IR_1    0x807F08F7 //кодовая последовательность
char* host = "192.168.0.44"; //ip сервера
uint16_t port = 9515; //порт для подключения к серверу

#include<ESP8266WiFi.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>

#define code1 18446744073709551615

IRrecv irrecv(5);
decode_results results;
//byte num = 0;

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
        {
          digitalWrite( LED_BUILTIN, HIGH );
          irrecv.resume();
        }
        String str = "";
        client.print(str+num);
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
  int N=100; //количество проверок сигнала
  bool checkIR = false;
  for (int i=0; i<N; i++)
  {
    if (irrecv.decode( &results ))
    {
      Serial.println(results.value);
        if (results.value == IR_1)
        {
          Serial.println(results.value);
          checkIR = true;
          break;
        }  
      irrecv.resume();
    }     
    results.value = NULL ;
    delay(50);
    Serial.println("check");
  }
  return checkIR;
}
