#define IR_code    0x807F08F7 //кодовая последовательность

#include <Arduino.h>
#include "PinDefinitionsAndMore.h" // Define macros for input and output pin etc.
#include <IRremote.hpp>

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(9600);
    IrSender.begin(); // Start with IR_SEND_PIN as send pin and if NO_LED_FEEDBACK_CODE is NOT defined, enable feedback LED at default feedback LED pin
}

void loop() {
    for (int i = 0; i < 3; i++) {
      IrSender.sendNEC(IR_code, 32);
      delay(200);
    }
    delay(900); 
}
