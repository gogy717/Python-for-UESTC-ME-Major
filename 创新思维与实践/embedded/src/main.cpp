#include <Arduino.h>
#include "tcp_client.h"
#include <Adafruit_NeoPixel.h>

// put function declarations here:
void SerialSetup();

// put definitions here:
#define RGB_PIN 38



void setup() {
  // put your setup code here, to run once:
  SerialSetup();
}

void loop() {
  // put your main code here, to run repeatedly:
}



// put function definitions here:
void SerialSetup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("Serial port is open");
}