# 🧪 Week 3 — Complete Test Procedure

> **Goal**: Verify soft gripper works end-to-end with Arduino + 3R arm
> **Time**: 2-3 hours for full test suite
> **Tools needed**: Arduino IDE + Serial Monitor, hard-boiled egg, ruler, phone (for video)

---

## 🟢 Pre-Test Checklist

Print this page and check off each item before starting:

### Hardware
- [ ] Arduino Uno uploaded with `hybrid_arm_gripper.ino`
- [ ] All wiring matches Section 15.4 pin assignment
- [ ] 12V power supply connected to valves + pump
- [ ] Common GND connected (Arduino GND ↔ 12V PSU GND)
- [ ] USB cable connected (for serial + power)
- [ ] E-stop button accessible
- [ ] Gripper mounted on 3R arm end-effector
- [ ] Pneumatic tubing connections tight (no kinks)

### Software
- [ ] Serial Monitor open at **9600 baud**
- [ ] Status line shows "System ready. State: IDLE"
- [ ] Both LEDs: green ON, red OFF
- [ ] Initial sensor readings: P ≈ 0 kPa, F ≈ 0 N
- [ ] Servo positions match IDLE (shoulder=90°, elbow=90°, wrist=90°)

### Safety
- [ ] E-stop button tested (press → red LED, valves close)
- [ ] Pressure sensor calibrated (0 kPa at atmospheric)
- [ ] Force sensor shows 0 N when nothing touching
- [ ] Workspace clear (no water, no flammable materials)
- [ ] First aid kit nearby (sharp tools + hot glue)

---

## 🧪 Test 1: Pneumatic Seal Test (5 min)

**Goal**: Verify no leaks in the pneumatic system

### Procedure
1. **Block the air outlet** (clamp the tubing near the gripper, or pinch with fingers)
2. **Send GRIP command** in Serial Monitor: type `G` + Enter
3. **Watch pressure rise** — should reach 60 kPa within 3-5 seconds
4. **Wait 30 seconds**
5. **Check pressure drop**

### Expected Results
| Parameter | Expected | Pass | Fail |
|-----------|----------|------|------|
| Time to reach 60 kPa | 3-5 sec | ☐ | ☐ |
| Pressure after 30 sec | 55-60 kPa (< 5% drop) | ☐ | ☐ |
| Pressure after 60 sec | 50-60 kPa (< 17% drop) | ☐ | ☐ |

### If FAIL
- Check tubing connections (push firmly, use zip ties)
- Check gripper inlet seal (re-apply hot glue + heat shrink)
- Check valve seats (replace if worn)
- Use soapy water on connections — bubbles indicate leaks

### Test Log
```
Time to 60 kPa: ___ sec
Pressure after 30s: ___ kPa
Pressure after 60s: ___ kPa
Result: ☐ PASS  ☐ FAIL
```

---

## 🧪 Test 2: Gripper Bending Test (5 min)

**Goal**: Verify fingers bend in correct direction

### Procedure
1. **Orient gripper horizontally** (fingers pointing up)
2. **Hold gripper firmly** (so the arm doesn't move)
3. **In Serial Monitor, type**: `+` + Enter 5 times (target pressure = +25 kPa)
4. **Watch fingers bend**
5. **Measure tip displacement** with ruler (or visually estimate)

### Expected Results
| Pressure | Expected bend | Pass |
|----------|---------------|------|
| 0 kPa | 0° (straight) | ☐ |
| 20 kPa | ~30° bend | ☐ |
| 40 kPa | ~60° bend | ☐ |
| 60 kPa | ~90° bend | ☐ |
| 80 kPa | ~120° bend (max) | ☐ |

### Symmetry Check
- Both fingers should bend at **similar angle** (within 10°)
- If asymmetric: check strain-limiting layer is on correct side
- If one finger doesn't bend: check tubing for blockage

### Test Log
```
Pressure: 0 kPa → Bend: ___° (each finger: L=___°, R=___°)
Pressure: 20 kPa → Bend: ___° (L=___°, R=___°)
Pressure: 40 kPa → Bend: ___° (L=___°, R=___°)
Pressure: 60 kPa → Bend: ___° (L=___°, R=___°)
Result: ☐ PASS  ☐ FAIL
```

---

## 🧪 Test 3: Force Sensor Calibration (10 min)

**Goal**: Calibrate force sensor to known weights

### Procedure
1. **Hang gripper vertically** (or place on table with finger pointing up)
2. **Apply known weights** to one finger:
   - 0g (nothing): should read ~0 N
   - 50g (small object): should read ~0.5 N
   - 100g (apple): should read ~1.0 N
   - 200g (cup of water): should read ~2.0 N
3. **Send GRIP command** (`G`) to grip each weight
4. **Read force value** from Serial Monitor

### Calibration Table (Fill in your values)
| Weight (g) | Expected Force (N) | Measured Force (N) | Error (%) |
|------------|-------------------:|-------------------:|----------:|
| 0 | 0.0 | ___ | ___ |
| 50 | 0.5 | ___ | ___ |
| 100 | 1.0 | ___ | ___ |
| 200 | 2.0 | ___ | ___ |
| 500 | 5.0 | ___ | ___ |

### If readings are off
- **All zeros**: check wiring (VCC, GND, SIG)
- **Always max**: voltage divider resistor wrong value
- **Inverted**: swap A1 input wires
- **Recalibrate** the formula in `readForceSensor()`:
  ```cpp
  float force = FORCE_CAL_A * pow(voltage, FORCE_CAL_B);
  // Adjust A and B to match your FSR's datasheet
  ```

### Result
☐ PASS (all values within ±15%)  ☐ FAIL (needs recalibration)

---

## 🧪 Test 4: Egg Test (CRITICAL — 10 min)

**Goal**: Verify gentle grasping on a real delicate object

### Setup
- 1 hard-boiled egg (room temperature)
- Place on table, 100mm in front of gripper
- Gripper at IDLE position

### Procedure
1. **Send APPROACH command** (`A`)
2. **Watch state transitions in Serial Monitor**:
   ```
   State: IDLE -> APPROACH
   State: APPROACH -> SOFT_CONTACT  (force > 0.5 N)
   State: SOFT_CONTACT -> GRIP      (force > 2.0 N)
   State: GRIP -> HOLD              (pressure stable)
   ```
3. **Wait for "GRIP CONFIRMED"** log (1-2 seconds)
4. **Watch LIFT state** triggered automatically (stability gate)
5. **Verify state**: 
   ```
   State: HOLD -> LIFT  ✓ GRIP CONFIRMED
   ```
6. **Manually lift object** (or wait for arm to lift)
7. **Hold for 10 seconds** (verify no slip)
8. **Send RELEASE command** (`R`)
9. **Inspect egg** for cracks
10. **Repeat 5 times** with same egg (or new one each time)

### Expected Results

| Test Cycle | Egg Status | Grip Force | Pressure |
|------------|-----------|-----------:|---------:|
| 1 | ☐ intact ☐ cracked | ___ N | ___ kPa |
| 2 | ☐ intact ☐ cracked | ___ N | ___ kPa |
| 3 | ☐ intact ☐ cracked | ___ N | ___ kPa |
| 4 | ☐ intact ☐ cracked | ___ N | ___ kPa |
| 5 | ☐ intact ☐ cracked | ___ N | ___ kPa |

### Pass Criteria
✅ All 5 cycles: egg intact, no cracks
✅ Grip force stays between 1.5-5 N (no over-grip)
✅ Pressure stable at 55-65 kPa (target = 60)

### If Egg Breaks
- **Cycle 1-2 breaks**: pressure too high — lower `TARGET_PRESSURE` to 50 kPa
- **Cycle 3+ breaks**: fingers losing elasticity — re-pour with fresh Ecoflex
- **Cracks visible**: take photo, stop test, re-tune PID

### Test Log
```
Cycles passed: ___ / 5
Average grip force: ___ N
Average pressure: ___ kPa
Egg condition after 5 cycles: ☐ Pristine  ☐ Cracked  ☐ Crushed
Result: ☐ PASS  ☐ FAIL
```

---

## 🧪 Test 5: Slip Detection Test (5 min)

**Goal**: Verify the gripper detects and corrects slip

### Procedure
1. **Grip an egg** (or similar object) successfully
2. **Hold for 5 seconds** (let it settle)
3. **Slowly pull the egg down** (simulate weight increase)
4. **Watch Serial Monitor** for slip detection
5. **Verify re-grip behavior**:
   ```
   "Slip detected! Re-gripping..."
   ```

### Expected Behavior
- Force < 0.5 N for > 500ms → log "Slip detected"
- Target pressure increases by +10 kPa (auto re-grip)
- Force recovers to > 1.5 N
- No state change to GRIP (should stay in HOLD with auto re-grip)

### Test Log
```
Slip detected? ☐ YES  ☐ NO
Re-grip successful? ☐ YES  ☐ NO
Time to recover: ___ sec
Final force: ___ N
Result: ☐ PASS  ☐ FAIL
```

---

## 🧪 Test 6: State Machine Full Cycle (10 min)

**Goal**: Verify all 7 states work in sequence

### Procedure
1. **Start at IDLE** (after power-on or `Z` command)
2. **Run through each state**:
   - Send `A` → APPROACH (no contact, just move)
   - Wait 3 sec → manually touch gripper to verify SOFT_CONTACT
   - Continue → GRIP (pressure ramps up)
   - Wait → HOLD (grip confirmed)
   - Wait → LIFT (arm moves up, [CMD] LIFT_START)
   - Send `R` → RELEASE (pressure drops)
   - Auto-return to IDLE
3. **Verify state transitions** match expected sequence
4. **Time the full cycle** (should be 8-15 seconds)

### Expected Sequence
```
IDLE 
  ↓ 'A' (auto)
APPROACH
  ↓ force > 0.5N (auto)
SOFT_CONTACT
  ↓ force > 2.0N (auto)
GRIP
  ↓ pressure stable (auto)
HOLD
  ↓ force stable 800ms (auto)
LIFT
  ↓ 'R' (manual)
RELEASE
  ↓ pressure < 5 kPa (auto)
IDLE
```

### Test Log
```
Full cycle time: ___ sec
State transitions correct? ☐ YES  ☐ NO
Any errors logged? ☐ YES  ☐ NO
Result: ☐ PASS  ☐ FAIL
```

---

## 🧪 Test 7: Emergency Stop Test (CRITICAL — 2 min)

**Goal**: Verify E-stop cuts power immediately

### Procedure
1. **Press E-stop button** WHILE in GRIP or HOLD state
2. **Watch immediate response**:
   - Red LED ON
   - All valves close
   - Pump stops
   - Serial: "!!! EMERGENCY STOP — Waiting for reset !!!"
3. **Verify pressure drops to 0 within 1 second**
4. **Release E-stop button**
5. **Send `Z` (reset)** + Enter in Serial Monitor
6. **Verify system returns to IDLE**

### Pass Criteria
✅ Pressure drops to 0 in < 1 second
✅ Red LED turns on
✅ Serial logs E-stop message
✅ Reset works (return to IDLE)

### Test Log
```
E-stop response time: ___ ms
Pressure dropped to 0? ☐ YES  ☐ NO
Reset successful? ☐ YES  ☐ NO
Result: ☐ PASS  ☐ FAIL
```

---

## 🧪 Test 8: 3R Arm Integration Test (15 min)

**Goal**: Verify soft gripper works with the 3R arm

### Procedure
1. **Mount gripper** to 3R arm end-effector (modular mount)
2. **Connect all wiring** (servo signals from arm to Arduino)
3. **Position egg** 150mm in front of base, 50mm above table
4. **Send `A` (APPROACH)**
5. **Watch arm move + gripper open** (serial logs)
6. **Allow auto state transitions** (force-based)
7. **Verify LIFT state moves arm up**:
   - Shoulder should rotate from 60° to 30°
   - Elbow should rotate from 90° to 50°
   - Wrist stays at 90°
8. **Send `R` (RELEASE)**
9. **Watch arm return to home**:
   - Shoulder back to 60°
   - Elbow back to 90°
10. **Inspect egg** after each cycle

### Expected Servo Movements
| State | Shoulder | Elbow | Wrist |
|-------|---------:|------:|------:|
| APPROACH | 60° | 90° | 90° |
| GRIP | 40° | 65° | 80° |
| HOLD | 40° | 65° | 80° |
| LIFT | 30° | 50° | 90° |
| RELEASE | 70° | 100° | 100° |

### Pass Criteria
✅ Arm moves smoothly between states (no jitter)
✅ Gripper maintains hold during LIFT
✅ Egg survives 3 full cycles
✅ Servos return to IDLE position after RELEASE

### Test Log
```
Full integration cycles: ___ / 3
Egg intact after 3 cycles: ☐ YES  ☐ NO
Arm movement smooth: ☐ YES  ☐ NO
Result: ☐ PASS  ☐ FAIL
```

---

## 📊 Test Results Summary

| Test | Description | Result | Notes |
|------|-------------|:------:|-------|
| 1 | Pneumatic Seal | ☐ | |
| 2 | Gripper Bending | ☐ | |
| 3 | Force Calibration | ☐ | |
| 4 | Egg Test (5 cycles) | ☐ | |
| 5 | Slip Detection | ☐ | |
| 6 | State Machine Cycle | ☐ | |
| 7 | Emergency Stop | ☐ | |
| 8 | 3R Arm Integration | ☐ | |

### Final Result
☐ **ALL PASS** — Week 3 complete! Move to Week 4
☐ **SOME FAIL** — Debug using troubleshooting guide
☐ **MAJOR FAIL** — Re-check wiring, recalibrate sensors, re-pour silicone

---

## 🐛 Debugging Quick Reference

### If state machine stuck in GRIP:
- Check pressure sensor wiring
- Verify target pressure is reachable
- Check pump capacity (might be too small)
- Increase `GRIP_TIMEOUT`

### If force readings always 0:
- Check FSR402 wiring (VCC, GND, SIG)
- Verify voltage divider resistor (10 kΩ)
- Test with multimeter (should vary when pressed)
- Recalibrate `readForceSensor()`

### If servos jitter:
- Add 100µF capacitor across servo power
- Use separate power supply for servos (not from Arduino 5V)
- Check ground connections

### If E-stop doesn't work:
- Check button wiring (might be NO instead of NC)
- Verify INPUT_PULLUP is enabled
- Test button with multimeter

### If pressure never reaches target:
- Check pump direction
- Verify valve is normally closed (NC)
- Check for leaks (use Test 1)
- Increase pump duty cycle (PWM)

---

## 📸 Documentation Checklist

Take photos/videos for portfolio:
- [ ] Gripper bending at different pressures (5 photos)
- [ ] Egg test (3 cycles, video)
- [ ] 3R arm full cycle (video)
- [ ] E-stop demo (video)
- [ ] Serial monitor output (screenshot)
- [ ] Wiring closeup (photo)
- [ ] Mold design (Fusion 360 screenshot or STL viewer)

Save all in `builds/soft_gripper/photos/`

---

**Week 3 complete when ALL 8 tests pass!** 🦑💪

— KANG YIP SZE, 13 June 2026
