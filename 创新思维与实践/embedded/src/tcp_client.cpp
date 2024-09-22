#include "tcp_client.h"

// Remove the class definition here and keep only the method implementations

ESP32TCPClient::ESP32TCPClient(const char* serverAddress, uint16_t serverPort)
    : server(serverAddress), port(serverPort), connected(false) {}

bool ESP32TCPClient::connect() {
    if (connected) {
        return true;
    }
    if (client.connect(server, port)) {
        connected = true;
        return true;
    }
    return false;
}

void ESP32TCPClient::disconnect() {
    if (connected) {
        client.stop();
        connected = false;
    }
}

bool ESP32TCPClient::isConnected() {
    return connected && client.connected();
}

bool ESP32TCPClient::send(const char* data) {
    if (!isConnected()) {
        return false;
    }
    return client.print(data) > 0;
}

String ESP32TCPClient::receive() {
    if (!isConnected()) {
        return "";
    }
    String receivedData = "";
    while (client.available()) {
        char c = client.read();
        receivedData += c;
    }
    return receivedData;
}

