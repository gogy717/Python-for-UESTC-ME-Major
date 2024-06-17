#include </Users/luozhufeng/.platformio/packages/framework-arduinoespressif32/cores/esp32/Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <AccelStepper.h>
#include <FreeRTOS.h>
#include <SPI.h>
#include <MultiStepper.h>

#define RGB_PIN 48 
#define YAW_STEP_PIN 4
#define YAW_DIR_PIN 5
#define PITCH_STEP_PIN 6
#define PITCH_DIR_PIN 7
#define LASER 38

#define YAW_LIM_PIN 35
#define PITCH_LIM_PIN 36

// define global variables
volatile bool is_initialized = false;

volatile bool Pid_mode = false;

// create objects
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, RGB_PIN, NEO_GRB + NEO_KHZ800);
AccelStepper yawStepper(AccelStepper::DRIVER, YAW_STEP_PIN, YAW_DIR_PIN);
AccelStepper pitchStepper(AccelStepper::DRIVER, PITCH_STEP_PIN, PITCH_DIR_PIN);
MultiStepper steppers;


// put Task declarations here:
void Task_Yaw(void *pvParameters);
void Task_Pitch(void *pvParameters);
void Task_Serial(void *pvParameters);
void Task_LIM_PIN(void *pvParameters);

// put function declarations here:
void PID_YAW(int target, int current);
void PID_PITCH(int target, int current);
void Data_decode_fun(const char* cmd);
void Pos_decode_fun(const char* cmd);

void setup() {
  Serial.begin(9600);
  // define pin modes
  pinMode(LASER,OUTPUT);
  pinMode(YAW_LIM_PIN, INPUT_PULLUP);
  pinMode(PITCH_LIM_PIN, INPUT_PULLUP);
  
  digitalWrite(LASER, LOW); // 打开LASER引脚
  strip.begin();
  strip.show();  // Clear any residual data in the LED strip
  delay(2000);   // Initial delay for system stabilization is good practice
  digitalWrite(LASER,HIGH);

  Serial.println("System Initialized");
  yawStepper.setMaxSpeed(200);   // Set maximum speeds
  pitchStepper.setMaxSpeed(200);
  yawStepper.setAcceleration(5000); // Set accelerations
  pitchStepper.setAcceleration(5000);

  // yawStepper.moveTo(6400);        // Move to initial positions
  // pitchStepper.moveTo(-6400);
  steppers.addStepper(yawStepper);
  steppers.addStepper(pitchStepper);
  long pos_init[2] = {6400, -6400};
  steppers.moveTo(pos_init);
  Serial.println("Steppers Initialized");

  xTaskCreatePinnedToCore(
    Task_Yaw,   /* 任务函数 */
    "Task_Yaw", /* 任务名称 */
    10000,       /* 栈大小 */
    NULL,       /* 任务输入参数 */
    3,          /* 任务优先级 */
    NULL,       /* 任务句柄 */
    0);         /* 核心编号 */

  xTaskCreatePinnedToCore(
    Task_Pitch,   /* 任务函数 */
    "Task_Pitch", /* 任务名称 */
    10000,         /* 栈大小 */
    NULL,         /* 任务输入参数 */
    2,            /* 任务优先级 */
    NULL,         /* 任务句柄 */
    1);           /* 核心编号 */
  xTaskCreatePinnedToCore(
    Task_Serial,   /* 任务函数 */
    "Task_Serial", /* 任务名称 */
    10000,         /* 栈大小 */
    NULL,         /* 任务输入参数 */
    1,            /* 任务优先级 */
    NULL,         /* 任务句柄 */
    1);           /* 核心编号 */
  xTaskCreatePinnedToCore(
    Task_LIM_PIN,   /* 任务函数 */
    "Task_LIM_PIN", /* 任务名称 */
    10000,         /* 栈大小 */
    NULL,         /* 任务输入参数 */
    1,            /* 任务优先级 */
    NULL,         /* 任务句柄 */
    1);           /* 核心编号 */
}


void loop() {
  // // put your main code here, to run repeatedly:
  // Serial.println("RED");
  // strip.setPixelColor(0, strip.Color(1, 0, 0));
  // yawStepper.moveTo(1000);
  // pitchStepper.moveTo(1000);
  // strip.show();
  // delay(1000);
  // Serial.println("GREEN");

  // strip.setPixelColor(0, strip.Color(0, 1, 0));
  // strip.show();
  // delay(1000);
  // Serial.println("BLUE");
  // strip.setPixelColor(0, strip.Color(0, 0, 1));
  // strip.show();
  // delay(1000);
  // create data buffer
  char data[128];
  // fill data buffer
  sprintf(data, "YawPitch: %d,%d,%f,%d,%d,%f\n", yawStepper.currentPosition(),yawStepper.targetPosition(),yawStepper.speed(), pitchStepper.currentPosition(),pitchStepper.targetPosition(),pitchStepper.speed());
  // sprintf(data,"spd1: %f, spd2: %f\n",yawStepper.speed(), pitchStepper.speed());
  Serial.println(data);
  delay(5);
}
void Data_decode_fun(const char* cmd){
  // 声明两个变量用于存储解析后的角度值
  int ang1, ang2;
  int spd1, spd2;
  int acc1, acc2;
  
  // 使用 sscanf 函数从 cmd 字符串中解析出角度值
  // 格式化字符串 "a%d,%d" 对应您的数据格式 "a<ang1>,<ang2>\n"
  if (sscanf(cmd, "a%d,%d,%d,%d", &ang1, &spd1, &ang2, &spd2) == 4) {
    // 如果成功解析出两个角度值
    acc1 = (ang1-yawStepper.currentPosition());
    acc2 = (ang2-pitchStepper.currentPosition());
    yawStepper.setMaxSpeed(spd1);   // Set maximum speeds
    pitchStepper.setMaxSpeed(spd2);
    yawStepper.setAcceleration(acc1); // Set accelerations
    pitchStepper.setAcceleration(acc2);
    yawStepper.moveTo(ang1);        // Move to target positions
    pitchStepper.moveTo(ang2);    
  } else {
    // 如果解析失败，输出错误信息
    Serial.println("Error: Invalid command format");
  }
}
void Pos_decode_fun(const char* cmd){
  int target_x, target_y;
  int pos_now_x, pos_now_y;
  if (sscanf(cmd, "p%d,%d,%d,%d", &target_x, &target_y, &pos_now_x, &pos_now_y) == 4) {
    
  } else {
    // 如果解析失败，输出错误信息
    Serial.println("Error: Invalid command format");
  }
  PID_YAW(target_x, pos_now_x);
  PID_PITCH(target_y, pos_now_y);

}

// put function definitions here:
void Task_Yaw(void *pvParameters) {
  long positions[2]; // 用于存储两个步进电机的目标位置
  for (;;) {
    // 运行两个步进电机的run方法
    if (Pid_mode) {
      yawStepper.runSpeed();
    }
    else{
      yawStepper.run();
      }
    // 移除或减小任务延迟
    vTaskDelay(1);  
  }
}


void Task_Pitch(void *pvParameters) {
  for (;;) {
    if (Pid_mode) {
      pitchStepper.runSpeed();
    }
    else{
      pitchStepper.run();
    }
    vTaskDelay(1); // Yield to other tasks
  }
}

void PID_YAW(int target, int current){
  float kp = 10;
  float ki = 0;
  float kd = 1;
  float error = 0;
  float last_error = 0;
  float integral = 0;
  float derivative = 0;
  float output = 0;
  float dt = 0.01;
  float max_output = 100;
  float min_output = -100;
  float max_integral = 100;
  float min_integral = -100;
  float max_error = 100;
  float min_error = -100;
  float max_derivative = 100;
  float min_derivative = -100;
  error = target - current;
  integral += error * dt;
  derivative = (error - last_error) / dt;
  output = kp * error + ki * integral + kd * derivative;
  if (output > max_output) {
    output = max_output;
  } else if (output < min_output) {
    output = min_output;
  }
  if (integral > max_integral) {
    integral = max_integral;
  } else if (integral < min_integral) {
    integral = min_integral;
  }
  if (error > max_error) {
    error = max_error;
  } else if (error < min_error) {
    error = min_error;
  }
  if (derivative > max_derivative) {
    derivative = max_derivative;
  } else if (derivative < min_derivative) {
    derivative = min_derivative;
  }
  last_error = error;
  // return output;
  yawStepper.setSpeed(-output);
  Pid_mode = true;
}

void PID_PITCH(int target, int current){
  float kp = 10;
  float ki = 0;
  float kd = 1;
  float error = 0;
  float last_error = 0;
  float integral = 0;
  float derivative = 0;
  float output = 0;
  float dt = 0.01;
  float max_output = 100;
  float min_output = -100;
  float max_integral = 100;
  float min_integral = -100;
  float max_error = 100;
  float min_error = -100;
  float max_derivative = 100;
  float min_derivative = -100;
  
  error = target - current;
  integral += error * dt;
  derivative = (error - last_error) / dt;
  output = kp * error + ki * integral + kd * derivative;
  if (output > max_output) {
    output = max_output;
  } else if (output < min_output) {
    output = min_output;
  }
  if (integral > max_integral) {
    integral = max_integral;
  } else if (integral < min_integral) {
    integral = min_integral;
  }
  if (error > max_error) {
    error = max_error;
  } else if (error < min_error) {
    error = min_error;
  }
  if (derivative > max_derivative) {
    derivative = max_derivative;
  } else if (derivative < min_derivative) {
    derivative = min_derivative;
  }
  last_error = error;
  // return output;
  pitchStepper.setSpeed(output);
  Pid_mode = true;
}

void Task_Serial(void *pvParameters) {
  // Define the buffer and its maximum size
  char buffer[128];
  int bufIndex = 0; // Buffer index
  volatile bool received = false;
  for (;;) {
    // Check if there is serial data available
  
    if (Serial.available() > 0) {
      char inChar = (char)Serial.read(); // Read the next character
      
      // Check for newline character which indicates the end of a command
      if (inChar == '\n' && bufIndex > 0) {
        buffer[bufIndex] = '\0'; // Null-terminate the string
        // Handle the complete command here
        if (buffer[0] == 'a') { // Confirm it's the correct command
          Data_decode_fun(buffer); // Parse and handle the command
        }
        if (buffer[0] == 'p') { // Confirm it's the correct command
          Pos_decode_fun(buffer); 
           // Parse and handle the command
        }
        bufIndex = 0; // Reset buffer index
        memset(buffer, 0, sizeof(buffer)); // Clear the buffer
      } else if (bufIndex < sizeof(buffer) - 1) {
        buffer[bufIndex++] = inChar; // Store character and increment index
      }
    }
    vTaskDelay(1); // Yield to other tasks
  }
}

void Task_LIM_PIN(void *pvParameters) {
  for (;;) {
    if (digitalRead(YAW_LIM_PIN) == LOW) {
      yawStepper.setCurrentPosition(0);
      yawStepper.moveTo(-280);//fu
      
    }
    if (digitalRead(PITCH_LIM_PIN) == LOW) {
      pitchStepper.setCurrentPosition(0);
      pitchStepper.moveTo(470);//zheng
    }
    delay(1);
  }
}