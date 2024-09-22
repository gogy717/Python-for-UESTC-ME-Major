#ifndef TCP_CLIENT_H
#define TCP_CLIENT_H

#include <WiFi.h>

class ESP32TCPClient {
private:
    WiFiClient client;
    const char* server;
    uint16_t port;
    bool connected;

public:
    ESP32TCPClient(const char* serverAddress, uint16_t serverPort);
    bool connect();
    void disconnect();
    bool isConnected();
    bool send(const char* data);
    String receive();
};

#endif // TCP_CLIENT_H
