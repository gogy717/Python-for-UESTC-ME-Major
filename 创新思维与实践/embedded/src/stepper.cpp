#include "stepper.h"
#include <AccelStepper.h>
#include <Arduino.h>
#include <vector>

// 外部声明步进电机对象
extern AccelStepper stepper1;
extern AccelStepper stepper2;
extern AccelStepper stepper3;

// 将 steppers 定义为指针的向量
extern std::vector<AccelStepper*> steppers;

// PID 参数
float Kp = 0.5;  // 比例系数
float Ki = 0.0;  // 积分系数
float Kd = 0.1;  // 微分系数

// 最大速度和加速度限制
float maxSpeed = 1000.0;       // 最大速度，步/秒
float maxAcceleration = 500.0; // 最大加速度，步/秒^2

// 为每个步进电机定义控制变量
std::vector<long> targetPositions;
std::vector<float> integrals;
std::vector<float> previousErrors;
std::vector<float> lastSpeeds;

// FreeRTOS 任务句柄
TaskHandle_t motorControlTaskHandle = NULL;

// 接口函数：设置目标位置
void setTarget(AccelStepper& stepper, int target) {
    // 在 steppers 向量中找到对应的步进电机
    for (size_t i = 0; i < steppers.size(); ++i) {
        if (steppers[i] == &stepper) {
            targetPositions[i] = target;
            // 重置积分和误差，以避免控制偏差
            integrals[i] = 0.0;
            previousErrors[i] = 0.0;
            return;
        }
    }
    // 如果未找到对应的步进电机，可以添加错误处理
}

// 步进电机控制任务
void motorControlTask(void* pvParameters) {
    const TickType_t xFrequency = pdMS_TO_TICKS(1); // 1ms 周期
    TickType_t xLastWakeTime = xTaskGetTickCount();

    while (true) {
        // 等待下一个周期
        vTaskDelayUntil(&xLastWakeTime, xFrequency);

        // 遍历所有步进电机
        for (size_t i = 0; i < steppers.size(); ++i) {
            AccelStepper* stepper = steppers[i];

            // 获取当前位置
            long currentPos = stepper->currentPosition();

            // 计算误差
            float error = targetPositions[i] - currentPos;

            // 误差累积（积分项）
            integrals[i] += error;

            // 计算误差变化（微分项）
            float derivative = error - previousErrors[i];

            // PID 输出（未限制的速度值）
            float speed = Kp * error + Ki * integrals[i] + Kd * derivative;

            // 限制速度值
            if (speed > maxSpeed) speed = maxSpeed;
            if (speed < -maxSpeed) speed = -maxSpeed;

            // 限制加速度
            float acceleration = speed - lastSpeeds[i];
            if (acceleration > maxAcceleration)
                speed = lastSpeeds[i] + maxAcceleration;
            else if (acceleration < -maxAcceleration)
                speed = lastSpeeds[i] - maxAcceleration;

            // 设置速度并运行电机
            stepper->setSpeed(speed);
            stepper->runSpeed();

            // 保存当前速度和误差
            lastSpeeds[i] = speed;
            previousErrors[i] = error;
        }
    }
}

// 初始化步进电机和创建任务
void StepperSetup() {
    // 设置最大速度（用于限制），并初始化控制变量
    for (auto& stepper : steppers) {
        stepper->setMaxSpeed(maxSpeed);
        // 控制变量初始化
        targetPositions.push_back(stepper->currentPosition());
        integrals.push_back(0.0);
        previousErrors.push_back(0.0);
        lastSpeeds.push_back(0.0);
    }

    // 创建步进电机控制任务，运行在核心 1，优先级为 3
    xTaskCreatePinnedToCore(
        motorControlTask,         // 任务函数
        "MotorControlTask",       // 任务名称
        4096,                     // 堆栈大小（字节）
        NULL,                     // 任务参数
        3,                        // 任务优先级
        &motorControlTaskHandle,  // 任务句柄
        1                         // 运行在核心 1
    );
}