#ifndef STEPPER_H
#define STEPPER_H

#include <AccelStepper.h>
#include <Arduino.h>
#include <vector>

// 外部声明步进电机对象
extern AccelStepper stepper1;
extern AccelStepper stepper2;
extern AccelStepper stepper3;

// 外部声明步进电机指针向量
extern std::vector<AccelStepper*> steppers;

// 函数声明
void StepperSetup();
void setTarget(AccelStepper& stepper, int target);

#endif // STEPPER_H