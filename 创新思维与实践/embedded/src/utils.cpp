#include "utils.h"
#include <Arduino.h>
#include <vector>
#include <string>

std::vector<std::string> Data_decode_fun(char *data) {
    std::vector<std::string> result;
    
    // 跳过第一个字符
    data++;
    
    // 分割字符串
    char *p = strtok(data, ",");
    while (p != NULL) {
        result.push_back(std::string(p));
        p = strtok(NULL, ",");
    }
    
    Serial.println("Data decode function is done");
    Serial.println("================================================");
    
    return result;
}


