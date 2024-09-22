#include <Arduino.h>
#include "tcp_client.h"
#include <WiFi.h>
#include "stepper.h"
#include <AccelStepper.h>
#include <Adafruit_NeoPixel.h>

// Include your data decode functions
#include "task.h"
#include "utils.h"

// Define the pins for the stepper motors
#define STEP_PIN1 2
#define DIR_PIN1 3
#define STEP_PIN2 4
#define DIR_PIN2 5
#define STEP_PIN3 6
#define DIR_PIN3 7

// Define the pins for RGB LED
#define RGB 48
typedef enum {
  RED = (255 << 16) | (0 << 8) | 0,
  GREEN = (0 << 16) | (255 << 8) | 0,
  BLUE = (0 << 16) | (0 << 8) | 255,
  YELLOW = (255 << 16) | (255 << 8) | 0,
  PURPLE = (255 << 16) | (0 << 8) | 255,
  CYAN = (0 << 16) | (255 << 8) | 255,
  WHITE = (255 << 16) | (255 << 8) | 255,
  OFF = (0 << 16) | (0 << 8) | 0
} RGBColor;


// Define the pins for Servo
#define SERVO 38
#define FREQUENCY 50
#define RESOLUTION 10
#define CHANNEL 0

// WiFi credentials
const char* ssid = "chat.openai.com";
const char* password = "31415926";

// Server details
const char* IP = "192.168.5.2";
const uint16_t PORT = 80;

// data
std::vector<std::string> data;

// Create an instance of your ESP32TCPClient
ESP32TCPClient client(IP, PORT);

// Create an instance of the stepper class
AccelStepper stepper1(
  AccelStepper::DRIVER,  // Driver type
  STEP_PIN1,              // Step pin
  DIR_PIN1                // Direction pin
);

// Create an instance of the Servo class
// Servo servo;

// Create an instance of the Adafruit_NeoPixel class
Adafruit_NeoPixel rgb(1, RGB, NEO_GRB + NEO_KHZ800);

// Function declarations
void SerialSetup();
void WiFiSetup();
void connectAndSendMessage();
// void Task_TCPClient(void *pvParameters);
void ServoSetup();
void RGBSetup();
void setRGB(RGBColor color);

void setup() {
  // Setup serial communication and WiFi
  RGBSetup();
  ServoSetup();
  SerialSetup();
  WiFiSetup();
  setRGB(GREEN);
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

void ServoSetup() {
  // Check if the channel is available before setting it up
  if (ledcSetup(SERVO, FREQUENCY, RESOLUTION) == 0) {
    Serial.println("Failed to setup LEDC channel for Servo");
    return;
  }
  ledcAttachPin(SERVO, CHANNEL);
}

void RGBSetup() {
  rgb.begin();
  rgb.setBrightness(10);
  rgb.setPixelColor(0, 255, 0, 0);
  rgb.show();
}

void setRGB(RGBColor color) {
  rgb.setPixelColor(0, color);
  rgb.show();
}




// ==================== FreeRTOS Tasks ====================
