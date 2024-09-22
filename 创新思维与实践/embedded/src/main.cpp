#include <Arduino.h>
#include "tcp_client.h"
#include <WiFi.h>

// Include your data decode functions
#include "task.h"
#include "utils.h"

// WiFi credentials
const char* ssid = "chat.openai.com";
const char* password = "31415926";

// Server details
const char* IP = "192.168.5.2";
const uint16_t PORT = 80;

// Create an instance of your ESP32TCPClient
ESP32TCPClient client(IP, PORT);

// Function declarations
void SerialSetup();
void WiFiSetup();
void connectAndSendMessage();
void Task_TCPClient(void *pvParameters);

void setup() {
  // Setup serial communication and WiFi
  SerialSetup();
  WiFiSetup();

  // Connect to the server and send an initial message if needed
  connectAndSendMessage();

  // Start the TCP client task
  xTaskCreatePinnedToCore(
    Task_TCPClient,     // Task function
    "TCP Client Task",  // Name of the task
    4096,               // Stack size
    NULL,               // Parameters
    1,                  // Priority
    NULL,               // Task handle
    1                   // Core
  );
}

void loop() {
  // Your main loop code
}

// Function definitions
void SerialSetup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  Serial.println("Serial port is open");
}

void WiFiSetup() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void connectAndSendMessage() {
  if (client.connect()) {
    Serial.println("Connected to server");
    
    // Send a message to the server
    const char* message = "Hello from ESP32!";
    if (client.send(message)) {
      Serial.println("Message sent successfully");
      
      // Wait for a response (optional)
      delay(1000);
      
      // Receive and print the response
      String response = client.receive();
      if (response.length() > 0) {
        Serial.println("Received response:");
        Serial.println(response);
      } else {
        Serial.println("No response received");
      }
    } else {
      Serial.println("Failed to send message");
    }
  } else {
    Serial.println("Connection to server failed");
  }
}



// ==================== FreeRTOS Tasks ====================

// // TCP Client Task
// void Task_TCPClient(void *pvParameters) {
//   // Define the buffer and its maximum size
//   char buffer[128];
//   int bufIndex = 0; // Buffer index

//   for (;;) {
//     // Check if connected, if not, try to connect
//     if (!client.isConnected()) {
//       if (client.connect()) {
//         Serial.println("Connected to server");
//       } else {
//         Serial.println("Connection failed, retrying...");
//         vTaskDelay(1000 / portTICK_PERIOD_MS); // Wait before retrying
//         continue;
//       }
//     }

//     // If connected, read data
//     if (client.isConnected()) {
//       // Use client.receive() to get all available data
//       String receivedData = client.receive();

//       // Process received data character by character
//       for (size_t i = 0; i < receivedData.length(); i++) {
//         char inChar = receivedData[i];

//         // Check for newline character which indicates the end of a command
//         if (inChar == '\n' && bufIndex > 0) {
//           buffer[bufIndex] = '\0'; // Null-terminate the string
//           // Handle the complete command here
//           if (buffer[0] == 'a') { // Confirm it's the correct command
//             Data_decode_fun(buffer); // Parse and handle the command
//           } else if (buffer[0] == 'p') { // Confirm it's the correct command
//             Pos_decode_fun(buffer); // Parse and handle the command
//           }
//           bufIndex = 0; // Reset buffer index
//           memset(buffer, 0, sizeof(buffer)); // Clear the buffer
//         } else if (bufIndex < sizeof(buffer) - 1) {
//           buffer[bufIndex++] = inChar; // Store character and increment index
//         }
//       }
//     } else {
//       // If disconnected, reset the buffer
//       bufIndex = 0;
//       memset(buffer, 0, sizeof(buffer));
//     }

//     vTaskDelay(1); // Yield to other tasks
//   }
// }
