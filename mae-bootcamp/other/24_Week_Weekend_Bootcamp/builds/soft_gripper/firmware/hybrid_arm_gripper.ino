/*
 * ============================================================
 * HYBRID 3R ARM + SOFT GRIPPER — COMPLETE ARDUINO FIRMWARE
 * ============================================================
 *
 * Week 3 Soft Robotics Deliverable
 * Engineer: KANG YIP SZE 施耿業
 * Date: 13 June 2026
 *
 * HARDWARE:
 *   - Arduino Uno
 *   - 3x Servos (3R arm: shoulder, elbow, wrist)
 *   - 2x 12V Solenoid Valves (via MOSFETs, finger 1 + 2)
 *   - 1x 12V Diaphragm Pump (via MOSFET)
 *   - 1x Pressure Sensor (0-100 kPa, analog)
 *   - 1x Force Sensor (FSR402, analog)
 *   - 1x Emergency Stop Button
 *   - 2x Status LEDs (Green = OK, Red = Error)
 *
 * WIRING:
 *   D2 -> Servo 1 (Shoulder) signal
 *   D3 -> Servo 2 (Elbow) signal
 *   D4 -> Servo 3 (Wrist) signal
 *   D5 -> LED Green (OK)
 *   D6 -> LED Red (Error)
 *   D7 -> Emergency Stop Button (INPUT_PULLUP)
 *   D8 -> MOSFET gate for Pump
 *   D9 -> MOSFET gate for Valve 1 (Finger 1)
 *   D10 -> MOSFET gate for Valve 2 (Finger 2)
 *   A0 -> Pressure Sensor signal
 *   A1 -> Force Sensor signal
 *   5V -> Sensor VCC
 *   GND -> Common ground
 *   External 12V PSU -> Valves + Pump
 *
 * USAGE:
 *   1. Upload to Arduino Uno
 *   2. Open Serial Monitor (9600 baud)
 *   3. Send commands:
 *        'A' = Start APPROACH
 *        'G' = GRIP cycle
 *        'H' = HOLD
 *        'L' = LIFT
 *        'R' = RELEASE
 *        'E' = Emergency stop
 *        'P' = Print PID tuning info
 *        '+' = Increase target pressure
 *        '-' = Decrease target pressure
 *        'Z' = Reset all to defaults
 *
 * ============================================================
 */

#include <Servo.h>

// ==================== PIN DEFINITIONS ====================
const int SERVO_SHOULDER = 2;
const int SERVO_ELBOW = 3;
const int SERVO_WRIST = 4;
const int LED_OK = 5;
const int LED_ERROR = 6;
const int ESTOP_BTN = 7;
const int PUMP_PIN = 8;
const int VALVE_1_PIN = 9;      // Finger 1
const int VALVE_2_PIN = 10;     // Finger 2
const int PRESSURE_SENSOR = A0;
const int FORCE_SENSOR = A1;

// ==================== SERVO OBJECTS ====================
Servo shoulder, elbow, wrist;

// ==================== STATE MACHINE ====================
enum State {
  IDLE,
  APPROACH,
  SOFT_CONTACT,
  GRIP,
  HOLD,
  LIFT,
  RELEASE
};

State currentState = IDLE;
unsigned long stateStartTime = 0;
unsigned long stateTimeIn() { return millis() - stateStartTime; }

// ==================== TUNABLE PARAMETERS ====================
// State machine thresholds
const float FORCE_CONTACT_THRESHOLD = 0.5;   // N, transition to SOFT_CONTACT
const float FORCE_GRIP_THRESHOLD = 2.0;      // N, transition to GRIP
const float FORCE_LIFT_MIN = 1.5;            // N, MIN force required before LIFT
const unsigned long GRIP_HOLD_TIME = 1000;   // ms, time in GRIP before HOLD
const unsigned long HOLD_STABLE_TIME = 800;  // ms, force must be stable this long
const float FORCE_STABILITY_TOLERANCE = 0.3; // N, max force variation for "stable"

// Pressure control
const float TARGET_PRESSURE = 60.0;          // kPa, target for GRIP
const float MAX_PRESSURE = 100.0;            // kPa, hard safety limit
const float PRESSURE_TOLERANCE = 5.0;        // kPa, acceptable error
const unsigned long GRIP_TIMEOUT = 5000;     // ms, max time in GRIP state

// Force safety
const float MAX_FORCE = 15.0;                // N, hard safety limit

// Slip detection
const float SLIP_THRESHOLD = 0.5;            // N, if force < this, slip detected
const unsigned long SLIP_REGRIP_DELAY = 500; // ms, wait before re-grip

// Arm positions (degrees)
const int POS_APPROACH[] = {60, 90, 90};     // Default approach
const int POS_SOFT_CONTACT[] = {45, 70, 80}; // Slow down near object
const int POS_GRIP[] = {40, 65, 80};
const int POS_HOLD[] = {40, 65, 80};
const int POS_LIFT[] = {30, 50, 90};         // Move up
const int POS_RELEASE[] = {70, 100, 100};    // Move away
const int POS_IDLE[] = {90, 90, 90};         // Neutral

// PID gains for pressure control
float Kp = 2.0;    // Proportional
float Ki = 0.5;    // Integral
float Kd = 0.1;    // Derivative
float pidIntegral = 0;
float pidLastError = 0;

// ==================== SENSOR READINGS ====================
float currentPressure = 0;  // kPa
float currentForce = 0;     // N
float targetPressure = TARGET_PRESSURE;

// ==================== SAFETY FLAGS ====================
bool eStopActive = false;
bool pressureOverload = false;
bool forceOverload = false;
unsigned long lastReGripTime = 0;

// ==================== TIMING ====================
unsigned long lastSensorRead = 0;
unsigned long lastStatusPrint = 0;
const unsigned long SENSOR_INTERVAL = 50;    // ms (20 Hz)
const unsigned long PRINT_INTERVAL = 300;    // ms (3.3 Hz)

// Grip stability tracking (for LIFT gate)
float forceHistory[10] = {0};      // Last 10 force readings
int forceHistoryIdx = 0;
unsigned long stableStartTime = 0;
bool forceStable = false;

// ==================== SETUP ====================
void setup() {
  Serial.begin(9600);
  Serial.println(F("=== Hybrid 3R Arm + Soft Gripper ==="));
  Serial.println(F("Commands: A=Approach, G=Grip, H=Hold, L=Lift, R=Release, E=E-Stop"));
  Serial.println(F("           +=Pressure, -=Pressure, P=PID info, Z=Reset"));
  Serial.println();

  // Pin modes
  pinMode(LED_OK, OUTPUT);
  pinMode(LED_ERROR, OUTPUT);
  pinMode(ESTOP_BTN, INPUT_PULLUP);
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(VALVE_1_PIN, OUTPUT);
  pinMode(VALVE_2_PIN, OUTPUT);

  // Attach servos
  shoulder.attach(SERVO_SHOULDER);
  elbow.attach(SERVO_ELBOW);
  wrist.attach(SERVO_WRIST);

  // Initial positions
  moveToPosition(POS_IDLE);
  setPump(false);
  setValves(false, false);
  digitalWrite(LED_OK, HIGH);
  digitalWrite(LED_ERROR, LOW);

  Serial.println(F("System ready. State: IDLE"));
}

// ==================== MAIN LOOP ====================
void loop() {
  // Read sensors at 20 Hz
  if (millis() - lastSensorRead > SENSOR_INTERVAL) {
    currentPressure = readPressureSensor();
    currentForce = readForceSensor();
    lastSensorRead = millis();
  }

  // Safety check (always first)
  checkSafety();
  if (eStopActive) {
    emergencyStop();
    return;
  }

  // Handle serial commands
  handleSerial();

  // Run state machine
  runStateMachine();

  // Print status
  printStatus();
}

// ==================== STATE MACHINE ====================
void runStateMachine() {
  switch (currentState) {
    case IDLE:
      moveToPosition(POS_IDLE);
      setPump(false);
      setValves(false, false);
      // Reset all one-shot signal flags for next cycle
      // (Note: liftSignalSent and dropSignalSent are static inside
      //  their respective cases, so they're reset on function re-entry)
      break;

    case APPROACH:
      moveToPosition(POS_APPROACH);
      setPump(false);
      setValves(false, false);
      if (currentForce > FORCE_CONTACT_THRESHOLD) {
        changeState(SOFT_CONTACT);
      }
      break;

    case SOFT_CONTACT:
      moveToPosition(POS_SOFT_CONTACT);
      setPump(false);
      setValves(false, false);
      if (currentForce > FORCE_GRIP_THRESHOLD) {
        changeState(GRIP);
      }
      // Timeout: if no contact detected in 10s, go back to IDLE
      if (stateTimeIn() > 10000) {
        Serial.println("Timeout: no contact, returning to IDLE");
        changeState(IDLE);
      }
      break;

    case GRIP:
      moveToPosition(POS_GRIP);
      // PID pressure control
      applyPressurePID();
      // Check for completion
      if (abs(currentPressure - targetPressure) < PRESSURE_TOLERANCE &&
          stateTimeIn() > GRIP_HOLD_TIME) {
        changeState(HOLD);
      }
      // Timeout: if can't reach pressure, release
      if (stateTimeIn() > GRIP_TIMEOUT) {
        Serial.println("Timeout: can't reach pressure, releasing");
        changeState(RELEASE);
      }
      break;

    case HOLD:
      moveToPosition(POS_HOLD);
      // Maintain pressure using PID
      applyPressurePID();
      // Slip detection
      if (currentForce < SLIP_THRESHOLD &&
          millis() - lastReGripTime > SLIP_REGRIP_DELAY) {
        Serial.println("Slip detected! Re-gripping...");
        lastReGripTime = millis();
        // Briefly increase pressure
        targetPressure = min(MAX_PRESSURE, targetPressure + 10);
        forceStable = false;  // Reset stability
        stableStartTime = 0;
      }
      // === LIFT GATE: only allow LIFT if grip is confirmed stable ===
      updateForceStability();
      if (forceStable && currentForce >= FORCE_LIFT_MIN) {
        if (stableStartTime == 0) {
          stableStartTime = millis();
          Serial.println(F("Grip stable. Confirming..."));
        } else if (millis() - stableStartTime > HOLD_STABLE_TIME) {
          // Force has been stable for HOLD_STABLE_TIME → ready to lift
          Serial.println(F("✓ GRIP CONFIRMED — ready for LIFT"));
          changeState(LIFT);
        }
      } else {
        // Force not stable or too low
        stableStartTime = 0;
        forceStable = false;
      }
      break;

    case LIFT:
      moveToPosition(POS_LIFT);
      // Maintain grip
      applyPressurePID();
      // Send LIFT_START signal (one-time)
      static bool liftSignalSent = false;
      if (!liftSignalSent) {
        Serial.println(F("[CMD] LIFT_START"));
        liftSignalSent = false;  // re-arm for next cycle
        // Reset for next cycle
        // Note: liftSignalSent reset in RELEASE
      }
      // Wait for arm to reach lift position
      // (In single-Arduino setup, this is instantaneous;
      //  in dual-Arduino setup, would wait for [ACK] LIFT_DONE)
      break;

    case RELEASE:
      moveToPosition(POS_RELEASE);
      setPump(false);
      setValves(false, false);
      // Send LIFT_DROP signal (for 3R arm to return to home)
      static bool dropSignalSent = false;
      if (!dropSignalSent) {
        Serial.println(F("[CMD] LIFT_DROP"));
        dropSignalSent = true;
      }
      // Wait for pressure to drop, then go to IDLE
      if (currentPressure < 5.0 && stateTimeIn() > 1500) {
        // Reset target pressure + PID + stability tracking
        targetPressure = TARGET_PRESSURE;
        pidIntegral = 0;
        pidLastError = 0;
        forceStable = false;
        stableStartTime = 0;
        // Reset signal flags for next cycle
        // (Re-arm by re-entering RELEASE next time)
        changeState(IDLE);
      }
      break;
  }
}

// ==================== PRESSURE PID CONTROL ====================
void applyPressurePID() {
  if (currentState != GRIP && currentState != HOLD && currentState != LIFT) {
    setPump(false);
    setValves(false, false);
    return;
  }

  // PID calculation
  float error = targetPressure - currentPressure;
  pidIntegral += error;
  pidIntegral = constrain(pidIntegral, -100, 100);  // Anti-windup
  float derivative = error - pidLastError;
  pidLastError = error;

  float output = Kp * error + Ki * pidIntegral + Kd * derivative;
  output = constrain(output, -100, 100);

  // Convert to pump/valve commands
  if (output > 0) {
    // Need more pressure: pump on, valves open
    setPump(true);
    // PWM on valves for proportional control
    int pwm = map((int)output, 0, 100, 0, 255);
    analogWrite(VALVE_1_PIN, pwm);
    analogWrite(VALVE_2_PIN, pwm);
  } else {
    // Pressure is OK or too high
    setPump(false);
    setValves(false, false);
  }
}

// ==================== FORCE STABILITY DETECTION ====================
// Tracks last 10 force readings. If all are within FORCE_STABILITY_TOLERANCE
// of each other, force is considered "stable" (good grip).
void updateForceStability() {
  // Add current force to history
  forceHistory[forceHistoryIdx] = currentForce;
  forceHistoryIdx = (forceHistoryIdx + 1) % 10;

  // Check stability: max - min within tolerance?
  float fMin = forceHistory[0], fMax = forceHistory[0];
  for (int i = 1; i < 10; i++) {
    if (forceHistory[i] < fMin) fMin = forceHistory[i];
    if (forceHistory[i] > fMax) fMax = forceHistory[i];
  }
  forceStable = ((fMax - fMin) < FORCE_STABILITY_TOLERANCE);
}

// ==================== SAFETY CHECKS ====================
void checkSafety() {
  // Emergency stop
  if (digitalRead(ESTOP_BTN) == LOW) {
    eStopActive = true;
  }

  // Pressure overload
  if (currentPressure > MAX_PRESSURE) {
    pressureOverload = true;
    setPump(false);
    setValves(false, false);
    Serial.println("!!! PRESSURE OVERLOAD !!!");
    changeState(RELEASE);
  }

  // Force overload
  if (currentForce > MAX_FORCE) {
    forceOverload = true;
    setValves(false, false);
    Serial.println("!!! FORCE OVERLOAD !!!");
    changeState(RELEASE);
  }
}

void emergencyStop() {
  setPump(false);
  setValves(false, false);
  moveToPosition(POS_IDLE);
  digitalWrite(LED_OK, LOW);
  digitalWrite(LED_ERROR, HIGH);
  Serial.println("!!! EMERGENCY STOP — Waiting for reset !!!");

  // Wait for button release + new press to reset
  while (digitalRead(ESTOP_BTN) == LOW) {
    delay(50);
  }
  delay(500);
  if (Serial.available() && Serial.read() == 'Z') {
    eStopActive = false;
    pressureOverload = false;
    forceOverload = false;
    digitalWrite(LED_ERROR, LOW);
    digitalWrite(LED_OK, HIGH);
    Serial.println("E-Stop reset. Returning to IDLE.");
    changeState(IDLE);
  }
}

// ==================== STATE TRANSITION ====================
void changeState(State newState) {
  if (currentState != newState) {
    Serial.print(F("State: "));
    Serial.print(stateName(currentState));
    Serial.print(F(" -> "));
    Serial.println(stateName(newState));
    currentState = newState;
    stateStartTime = millis();
  }
}

// ==================== SERVO POSITION ====================
void moveToPosition(const int pos[]) {
  shoulder.write(constrain(pos[0], 0, 180));
  elbow.write(constrain(pos[1], 0, 180));
  wrist.write(constrain(pos[2], 0, 180));
}

// ==================== PUMP + VALVE CONTROL ====================
void setPump(bool on) {
  digitalWrite(PUMP_PIN, on ? HIGH : LOW);
}

void setValves(bool v1, bool v2) {
  digitalWrite(VALVE_1_PIN, v1 ? HIGH : LOW);
  digitalWrite(VALVE_2_PIN, v2 ? HIGH : LOW);
}

// ==================== SENSOR READING ====================
float readPressureSensor() {
  // Typical 0-100kPa sensor: 0.5V = 0 kPa, 4.5V = 100 kPa
  int raw = analogRead(PRESSURE_SENSOR);
  float voltage = raw * 5.0 / 1023.0;
  float pressure = (voltage - 0.5) * 100.0 / 4.0;
  return constrain(pressure, 0, 150);  // Allow slight over-range for safety
}

float readForceSensor() {
  // FSR402 in voltage divider: V = 5V * R_FSR / (R_FSR + R_fixed)
  int raw = analogRead(FORCE_SENSOR);
  float voltage = raw * 5.0 / 1023.0;
  if (voltage < 0.1) return 0;
  // Empirical: F (N) ≈ 20 * (V / 5V)^-1.5 (calibrate for your FSR)
  float force = 20.0 * pow(voltage / 5.0, -1.5);
  return constrain(force, 0, 25);
}

// ==================== SERIAL COMMAND HANDLER ====================
void handleSerial() {
  if (!Serial.available()) return;

  char cmd = Serial.read();

  switch (cmd) {
    case 'A': case 'a':
      changeState(APPROACH);
      break;
    case 'G': case 'g':
      changeState(GRIP);
      break;
    case 'H': case 'h':
      changeState(HOLD);
      break;
    case 'L': case 'l':
      changeState(LIFT);
      break;
    case 'R': case 'r':
      changeState(RELEASE);
      break;
    case 'E': case 'e':
      eStopActive = true;
      break;
    case '+':
      targetPressure = min(MAX_PRESSURE - 5, targetPressure + 5);
      Serial.print(F("Target pressure: "));
      Serial.print(targetPressure);
      Serial.println(F(" kPa"));
      break;
    case '-':
      targetPressure = max(10.0, targetPressure - 5);
      Serial.print(F("Target pressure: "));
      Serial.print(targetPressure);
      Serial.println(F(" kPa"));
      break;
    case 'P': case 'p':
      Serial.print(F("PID: Kp="));
      Serial.print(Kp); Serial.print(F(" Ki="));
      Serial.print(Ki); Serial.print(F(" Kd="));
      Serial.println(Kd);
      Serial.print(F("Error: "));
      Serial.print(pidLastError);
      Serial.print(F(" | Integral: "));
      Serial.println(pidIntegral);
      break;
    case 'Z': case 'z':
      targetPressure = TARGET_PRESSURE;
      pidIntegral = 0;
      pidLastError = 0;
      pressureOverload = false;
      forceOverload = false;
      Serial.println(F("Reset to defaults."));
      changeState(IDLE);
      break;
  }
}

// ==================== STATUS OUTPUT ====================
void printStatus() {
  if (millis() - lastStatusPrint < PRINT_INTERVAL) return;
  lastStatusPrint = millis();

  Serial.print(F("State: "));
  Serial.print(stateName(currentState));
  Serial.print(F(" | T(ms): "));
  Serial.print(stateTimeIn());
  Serial.print(F(" | P: "));
  Serial.print(currentPressure, 1);
  Serial.print(F(" kPa (target "));
  Serial.print(targetPressure, 0);
  Serial.print(F(") | F: "));
  Serial.print(currentForce, 1);
  Serial.print(F(" N"));
  if (eStopActive) Serial.print(F(" [E-STOP]"));
  if (pressureOverload) Serial.print(F(" [P-OVR]"));
  if (forceOverload) Serial.print(F(" [F-OVR]"));
  Serial.println();
}

const char* stateName(State s) {
  switch (s) {
    case IDLE: return "IDLE";
    case APPROACH: return "APPROACH";
    case SOFT_CONTACT: return "SOFT_CONTACT";
    case GRIP: return "GRIP";
    case HOLD: return "HOLD";
    case LIFT: return "LIFT";
    case RELEASE: return "RELEASE";
    default: return "?";
  }
}
