#include <AccelStepper.h>

#define STEP_PIN 8
#define DIR_PIN 9

AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input.startsWith("M")) {
      long steps = input.substring(1).toInt();
      stepper.move(steps);
      stepper.runToPosition();
    }
  }
}
