#include <Arduino.h>
#include "tcp_client.h"

// put function declarations here:
void TCPClientSetup();



void setup() {
  // put your setup code here, to run once:
  TCPClientSetup();

}

void loop() {
  // put your main code here, to run repeatedly:
}

// put function definitions here:
void TCPClientSetup() {
  TCPClient client("127.0.0.1", 8080);

  if (!client.connectToServer()) {
    Serial.println("Connection to server failed");
    return;
  }

  if (!client.sendMessage("Hello from Arduino")) {
    Serial.println("Sending message failed");
    return;
  }

  std::string response = client.receiveMessage();
  Serial.print("Server: ");
  Serial.println(response.c_str());
}
