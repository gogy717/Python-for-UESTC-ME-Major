#ifndef TCP_CLIENT_H
#define TCP_CLIENT_H

#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

class TCPClient {
public:
    TCPClient(const std::string& address, int port);
    ~TCPClient();
    bool connectToServer();
    bool sendMessage(const std::string& message);
    std::string receiveMessage();

private:
    int sock;
    struct sockaddr_in serv_addr;
};

#endif // TCP_CLIENT_H