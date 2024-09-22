#include "task.h"
#include "tcp_client.h"
#include<Arduino.h>
#include "utils.h"
#include <vector>
#include <string>

extern ESP32TCPClient client;  
extern std::vector<std::string> data;

// TCP Client Task
void Task_TCPClient(void *pvParameters) {
  // Define the buffer and its maximum size
  char buffer[128];
  int bufIndex = 0; // Buffer index

  for (;;) {
    // Check if connected, if not, try to connect
    if (!client.isConnected()) {
      if (client.connect()) {
        Serial.println("Connected to server");
      } else {
        Serial.println("Connection failed, retrying...");
        vTaskDelay(1000 / portTICK_PERIOD_MS); // Wait before retrying
        continue;
      }
    }

    // If connected, read data
    if (client.isConnected()) {
        // Use client.receive() to get all available data
        String receivedData = client.receive();
        // Serial.println(receivedData);

        // Process received data character by character
        for (size_t i = 0; i < receivedData.length(); i++) {
            char inChar = receivedData[i];
            
            // Check for newline character which indicates the end of a command
            if (inChar == '\n' && bufIndex > 0) {
            buffer[bufIndex] = '\0'; // Null-terminate the string
            // Handle the complete command here
            if (buffer[0] == 'a') { // Confirm it's the correct command
                data = Data_decode_fun(buffer); // Parse and handle the command
                Serial.println(data[0].c_str());
                Serial.println(data[1].c_str());
                Serial.println(data[2].c_str());
            }
            bufIndex = 0; // Reset buffer index
            memset(buffer, 0, sizeof(buffer)); // Clear the buffer
            } else if (bufIndex < sizeof(buffer) - 1) {
            buffer[bufIndex++] = inChar; // Store character and increment index
            // Serial.print(buffer[bufIndex-1]);
            // Serial.print(": ");
            // Serial.println(bufIndex);
            }
        }
    } else {
      // If disconnected, reset the buffer
      bufIndex = 0;
      memset(buffer, 0, sizeof(buffer));
    }

    vTaskDelay(1); // Yield to other tasks
  }
}
