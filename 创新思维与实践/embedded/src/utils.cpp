#include "utils.h"
#include <Arduino.h>

void Data_decode_fun(char *data){
    Serial.println(data);
    Serial.println("Data decode function is called");
    // TODO: handle the processed data
    //delete the first character
    data++;
    //split by comma
    char *p = strtok(data, ",");
    while (p != NULL) {
        Serial.println(p);
        p = strtok(NULL, ",");
    }
    Serial.println("Data decode function is done"); 
}


