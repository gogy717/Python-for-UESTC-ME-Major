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

/**
 * @brief Constructs a new TCPClient object.
 * 
 * This constructor initializes a TCP client with the specified server address and port.
 * It sets up the socket and server address structure, and attempts to create a socket
 * and convert the provided address to a network address.
 * 
 * @param address The server address to connect to.
 * @param port The port number on the server to connect to.
 * 
 * @note If socket creation fails or the address is invalid, an error message is printed to std::cerr.
 */
TCPClient::TCPClient(const std::string& address, int port) {
    sock = 0;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        std::cerr << "Socket creation error" << std::endl;
    }

    if (inet_pton(AF_INET, address.c_str(), &serv_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address/ Address not supported" << std::endl;
    }
}

TCPClient::~TCPClient() {
    close(sock);
}

bool TCPClient::connectToServer() {
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "Connection Failed" << std::endl;
        return false;
    }
    return true;
}

bool TCPClient::sendMessage(const std::string& message) {
    if (send(sock, message.c_str(), message.length(), 0) < 0) {
        std::cerr << "Send message failed" << std::endl;
        return false;
    }
    std::cout << "Message sent" << std::endl;
    return true;
}

std::string TCPClient::receiveMessage() {
    char buffer[1024] = {0};
    int valread = read(sock, buffer, 1024);
    if (valread < 0) {
        std::cerr << "Receive message failed" << std::endl;
        return "";
    }
    return std::string(buffer);
}

int main() {
    TCPClient client("127.0.0.1", 8080);

    if (!client.connectToServer()) {
        return -1;
    }

    if (!client.sendMessage("Hello from client")) {
        return -1;
    }

    std::string response = client.receiveMessage();
    std::cout << "Server: " << response << std::endl;

    return 0;
}