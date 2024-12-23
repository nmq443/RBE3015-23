#include <Servo.h>

Servo myServo;

const int CLOSE_POSITION = 0;
const int OPEN_POSITION = 90;

void setup() {
  myServo.attach(9);
  myServo.write(CLOSE_POSITION);
  Serial.begin(9600);
  Serial.println("Servo control ready. Waiting for commands...");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "00") {
      myServo.write(CLOSE_POSITION);
      Serial.println("Servo closed.");
    } else if (command == "01") {
      myServo.write(OPEN_POSITION);
      Serial.println("Servo opened.");
    } else {
      Serial.println("Invalid command.");
    }
  }
}
