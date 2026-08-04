"""
Soft Gripper Arduino Firmware
- Standalone version of the Week 3 gripper controller
- Upload to Arduino Uno
- See builds/soft_gripper/docs/BUILD_PLAN.md for wiring

Usage:
  1. Open in Arduino IDE
  2. Select Board: Arduino Uno
  3. Upload
  4. Open Serial Monitor (9600 baud)
  5. Send commands:
     - 'A' = Start APPROACH
     - 'G' = Force GRIP (manual override)
     - 'R' = RELEASE
     - 'L' = LIFT
     - 'E' = Emergency stop (or press button)
*/

#include <Servo.h>

// Pin Definitions
const int VALVE_1 = 9;        // Finger 1 (PWM)
const int VALVE_2 = 10;       // Finger 2 (PWM)
const int PRESSURE_SENSOR = A0;
const int FORCE_SENSOR = A1;
const int SERVO_SHOULDER = 2;
const int SERVO_ELBOW = 3;
const int SERVO_WRIST = 4;
const int LED_OK = 5;
const int LED_ERROR = 6;
const int ESTOP_BTN = 7;

Servo shoulder, elbow, wrist;

enum State { APPROACH, SOFT_CONTACT, GRIP, HOLD, LIFT, RELEASE };
State currentState = APPROACH;

const float FORCE_CONTACT_THRESHOLD = 0.5;
const float FORCE_GRIP_THRESHOLD = 2.0;
const float PRESSURE_TARGET = 60.0;
const float PRESSURE_TOLERANCE = 5.0;
const unsigned long GRIP_HOLD_TIME = 1000;

unsigned long stateEntryTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(VALVE_1, OUTPUT);
  pinMode(VALVE_2, OUTPUT);
  pinMode(LED_OK, OUTPUT);
  pinMode(LED_ERROR, OUTPUT);
  pinMode(ESTOP_BTN, INPUT_PULLUP);

  shoulder.attach(SERVO_SHOULDER);
  elbow.attach(SERVO_ELBOW);
  wrist.attach(SERVO_WRIST);

  digitalWrite(VALVE_1, LOW);
  digitalWrite(VALVE_2, LOW);
  digitalWrite(LED_OK, HIGH);

  Serial.println("=== Soft Gripper Ready ===");
  Serial.println("Commands: A=Approach, G=Grip, R=Release, L=Lift, E=E-Stop");
}

void loop() {
  if (digitalRead(ESTOP_BTN) == LOW) {
    emergencyStop();
    return;
  }

  // Read sensors
  float force = readForceSensor();
  float pressure = readPressureSensor();

  // Handle serial commands
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'A' || cmd == 'a') transitionTo(APPROACH);
    else if (cmd == 'G' || cmd == 'g') transitionTo(GRIP);
    else if (cmd == 'R' || cmd == 'r') transitionTo(RELEASE);
    else if (cmd == 'L' || cmd == 'l') transitionTo(LIFT);
    else if (cmd == 'E' || cmd == 'e') emergencyStop();
  }

  // State machine
  switch (currentState) {
    case APPROACH:
      // Move to default position
      shoulder.write(90); elbow.write(45); wrist.write(90);
      if (force > FORCE_CONTACT_THRESHOLD) transitionTo(SOFT_CONTACT);
      break;

    case SOFT_CONTACT:
      if (force > FORCE_GRIP_THRESHOLD) transitionTo(GRIP);
      break;

    case GRIP:
      analogWrite(VALVE_1, 200);  // ~80% duty
      analogWrite(VALVE_2, 200);
      if (abs(pressure - PRESSURE_TARGET) < PRESSURE_TOLERANCE &&
          millis() - stateEntryTime > GRIP_HOLD_TIME) {
        transitionTo(HOLD);
      }
      break;

    case HOLD:
      // Maintain pressure, check for slip
      if (force < FORCE_GRIP_THRESHOLD * 0.5) {
        Serial.println("Slip detected, re-gripping");
        transitionTo(GRIP);
      }
      break;

    case LIFT:
      shoulder.write(120); elbow.write(90); wrist.write(90);
      break;

    case RELEASE:
      analogWrite(VALVE_1, 0);
      analogWrite(VALVE_2, 0);
      break;
  }

  // Print status
  Serial.print("State: ");
  Serial.print(stateName(currentState));
  Serial.print(" | F: ");
  Serial.print(force, 1);
  Serial.print("N | P: ");
  Serial.print(pressure, 1);
  Serial.println(" kPa");

  delay(50);
}

void transitionTo(State s) {
  currentState = s;
  stateEntryTime = millis();
  Serial.print("→ ");
  Serial.println(stateName(s));
}

void emergencyStop() {
  analogWrite(VALVE_1, 0);
  analogWrite(VALVE_2, 0);
  digitalWrite(LED_OK, LOW);
  digitalWrite(LED_ERROR, HIGH);
  Serial.println("!!! EMERGENCY STOP !!!");
  while (true) {}
}

float readForceSensor() {
  int raw = analogRead(FORCE_SENSOR);
  float voltage = raw * 5.0 / 1023.0;
  if (voltage < 0.1) return 0;
  float force = 20.0 * pow(voltage / 5.0, -1.5);
  return constrain(force, 0, 20);
}

float readPressureSensor() {
  int raw = analogRead(PRESSURE_SENSOR);
  float voltage = raw * 5.0 / 1023.0;
  float pressure = (voltage - 0.5) * 100.0 / 4.0;
  return constrain(pressure, 0, 100);
}

const char* stateName(State s) {
  switch (s) {
    case APPROACH: return "APPROACH";
    case SOFT_CONTACT: return "SOFT_CONTACT";
    case GRIP: return "GRIP";
    case HOLD: return "HOLD";
    case LIFT: return "LIFT";
    case RELEASE: return "RELEASE";
    default: return "?";
  }
}
