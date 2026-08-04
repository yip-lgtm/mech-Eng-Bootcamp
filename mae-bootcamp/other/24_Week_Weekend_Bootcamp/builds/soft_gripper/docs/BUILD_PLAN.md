# 🛠️ BUILD PLAN: 2-Finger Pneumatic Soft Gripper

> **Project**: Week 3 Soft Robotics Deliverable
> **Engineer**: KANG YIP SZE 施耿業
> **Target**: Functional pneumatic gripper integrated with 3R arm
> **Estimated Time**: 14-20 hours (2 weekends)
> **Budget**: ~HK$1,685

---

## 🎯 Build Goals

1. ✅ Build a working 2-finger pneumatic soft gripper
2. ✅ Integrate with existing 3R arm
3. ✅ Implement state machine control
4. ✅ Test grasping (egg test)
5. ✅ Document + push to GitHub

---

## 📋 Pre-Build Checklist

### Skills Required
- [ ] Basic 3D printing (have a printer or access to one)
- [ ] Soldering (basic through-hole)
- [ ] Arduino programming (have done before)
- [ ] Molding and casting (first time — watch YouTube tutorials first)

### Tools Required
- [ ] 3D printer OR access to print service
- [ ] Soldering iron + solder
- [ ] Wire strippers / cutters
- [ ] Multimeter
- [ ] Tweezers
- [ ] Mixing cups (for Ecoflex)
- [ ] Stir sticks
- [ ] Safety glasses
- [ ] Nitrile gloves
- [ ] Vacuum chamber (optional, for degassing Ecoflex)
- [ ] Compressed air supply (small 12V pump OR syringe)

### Workspace
- [ ] Clean, flat, well-ventilated surface
- [ ] Cover with plastic sheet (Ecoflex is messy)
- [ ] Access to sink for cleanup
- [ ] Good lighting

---

## 🗓️ Build Schedule (2 Weekends)

### **Weekend 1: Mold + Silicone (Saturday-Sunday, 8-10h)**

#### Saturday Morning (3-4h): Design + Print Mold
- [ ] Open Fusion 360 (or TinkerCAD)
- [ ] Design 2-finger mold (3 chambers each, 60mm long)
- [ ] Save as STL
- [ ] Slice with Cura (0.2mm layer, 20% infill, PLA)
- [ ] Print mold (~4-6 hours)
- [ ] Meanwhile: order missing components from AliExpress

**Mold Design Specs**:
- Outer dimensions: 80mm × 30mm × 15mm
- 2 finger cavities, each with:
  - 3 cylindrical chambers (Ø 4mm, 8mm pitch)
  - 1 main channel (Ø 6mm) for air supply
  - Strain-limiting layer slot (1mm deep, 10mm wide, on bottom)
- Material: PLA (easy to print, easy to demold)

**Fusion 360 Sketch (ASCII)**:
```
   ┌──────────────────────────┐
   │ ┌────┐  ┌────┐  ┌────┐   │  ← Chamber 1, 2, 3 (cylindrical)
   │ │ Ø4 │  │ Ø4 │  │ Ø4 │   │     (4mm dia, 8mm pitch)
   │ │    │  │    │  │    │   │
   │ ├────┤  ├────┤  ├────┤   │
   │ │ Ø6 │  │ Ø6 │  │ Ø6 │   │  ← Air channel (6mm dia)
   │ └────┘  └────┘  └────┘   │
   │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │  ← Strain limit slot
   └──────────────────────────┘
        ↑
   Inlet (Ø 4mm) for tubing
```

#### Saturday Afternoon (2h): Prepare Ecoflex
- [ ] Order Ecoflex 00-30 from local Smooth-On distributor
- [ ] If not arrived: use Dragon Skin 10 (similar properties)
- [ ] Watch YouTube: "Ecoflex silicone mixing tutorial"
- [ ] Prepare work area (cover, gloves, ventilation)

#### Sunday (4-5h): Pour + Cure
- [ ] Mix Ecoflex Part A + Part B (1:1 ratio by weight)
- [ ] Stir slowly for 3 minutes (avoid air bubbles)
- [ ] (Optional) Vacuum degas for 5 minutes
- [ ] Pour slowly into mold (one corner, let it flow)
- [ ] Tap mold gently to release bubbles
- [ ] Place strain-limiting fabric layer (1mm thick)
- [ ] Pour second layer if needed
- [ ] Cure 4-6 hours at room temperature (or 1h at 60°C)
- [ ] Demold carefully
- [ ] Inspect: any defects? Air bubbles? Re-pour if needed.

---

### **Weekend 2: Electronics + Integration (Saturday-Sunday, 6-10h)**

#### Saturday (4-5h): Electronics + Wiring
- [ ] Solder MOSFET drivers (IRF540N) on perfboard
- [ ] Add flyback diodes (1N4007) across each valve
- [ ] Wire up pressure sensor (3-wire: VCC/GND/SIG)
- [ ] Wire up force sensor (FSR402 with voltage divider)
- [ ] Connect 2x 12V solenoid valves
- [ ] Connect emergency stop button
- [ ] Connect status LEDs
- [ ] Test all connections with multimeter
- [ ] Upload Arduino code (from Section 15.4)
- [ ] Test serial monitor output
- [ ] Calibrate sensors (force = 0, pressure = 0)

**Wiring Checklist**:
- [ ] 12V PSU → valves (with MOSFET switching)
- [ ] Arduino D9 → MOSFET gate 1
- [ ] Arduino D10 → MOSFET gate 2
- [ ] Arduino A0 → pressure sensor signal
- [ ] Arduino A1 → force sensor signal
- [ ] Arduino D7 → emergency stop button
- [ ] Arduino D5 → green LED
- [ ] Arduino D6 → red LED
- [ ] Common GND connected throughout

#### Sunday (3-5h): Integration + Testing
- [ ] Mount gripper to 3R arm end-effector (3D-printed mount)
- [ ] Connect pneumatic tubing
- [ ] Test pressure build-up (should reach 60 kPa in 2-3 seconds)
- [ ] Test grip cycle:
  1. Power on (LED green)
  2. Open serial monitor (9600 baud)
  3. Send 'A' to start APPROACH state
  4. Watch arm move, gripper approach
  5. Verify state transitions in serial monitor
  6. Test GRIP cycle (valve opens, pressure ramps)
  7. Test RELEASE (valve closes, pressure drops)
- [ ] **Egg test**: Try to grip a hard-boiled egg
  - [ ] Egg intact after 5 grip-release cycles? ✅
  - [ ] Grip force 2-5N? ✅
  - [ ] No slipping when held? ✅
- [ ] If egg breaks: reduce max pressure, recalibrate
- [ ] If no grip: increase max pressure, check seals
- [ ] Document with photos at each step

---

## 🧪 Test Procedures

### Test 1: Pneumatic Seal Test
**Goal**: Verify no leaks in the pneumatic system
1. Pressurise to 60 kPa
2. Close valve
3. Wait 30 seconds
4. Measure pressure drop
5. **Pass criteria**: <5% pressure drop in 30s
6. If fail: check tubing connections, retighten

### Test 2: Grip Force Calibration
**Goal**: Verify grip force is safe for delicate objects
1. Place force gauge between gripper fingers
2. Pressurise to 20, 40, 60, 80, 100 kPa
3. Record force at each pressure
4. **Expected**: ~10N at 60 kPa (per our sim)
5. Build calibration table for Arduino

### Test 3: Egg Test
**Goal**: Verify gentle grasping
1. Hard-boiled egg at room temperature
2. 5 grip-release cycles
3. **Pass criteria**: Egg intact, no cracks
4. Document with before/after photos

### Test 4: Response Time
**Goal**: Measure actuation speed
1. Send GRIP command
2. Time from command to grip complete
3. **Expected**: 1-2 seconds (60 kPa in 2s with small pump)
4. If too slow: check pump capacity, tubing diameter

### Test 5: State Machine Integration
**Goal**: Verify all 6 states work
1. Power on → APPROACH (LED blue)
2. Move arm manually to object
3. Contact detected → SOFT_CONTACT (LED yellow)
4. Force > 2N → GRIP (LED orange)
5. Pressure stable → HOLD (LED green)
6. Send 'L' → LIFT (LED green)
7. Send 'R' → RELEASE (LED gray)
8. Verify serial output for each state

### Test 6: Emergency Stop
**Goal**: Verify E-stop cuts power
1. Press E-stop button during grip
2. **Expected**: Valves close immediately, red LED, system halts
3. **Pass criteria**: Pressure drops to 0 in <1s

---

## 🐛 Troubleshooting Guide

| Problem | Cause | Solution |
|---------|-------|----------|
| Silicone sticks to mold | No release agent | Spray mold release (or use cornstarch) |
| Silicone has bubbles | Mixed too fast | Mix slowly, degas if possible |
| Gripper doesn't bend | Strain layer too thick | Use thinner fabric (0.3mm) |
| Gripper bends too much | Strain layer too thin | Use thicker fabric (0.5mm) |
| Valve doesn't open | Wiring wrong / no power | Check 12V supply, MOSFET gate signal |
| Pressure doesn't build | Leak in tubing | Re-seat tubing, use clamps |
| Pressure sensor reads 0 | Wrong wiring | Check VCC/GND/SIG |
| Force sensor reads 0 | Voltage divider wrong | Check resistor value (10kΩ) |
| Arduino doesn't respond | Wrong baud rate | Set Serial Monitor to 9600 |
| Egg breaks during grip | Pressure too high | Reduce max pressure to 50 kPa |
| Grip slips | Pressure too low / smooth surface | Increase pressure, add texture to fingers |
| Arm doesn't move | Servo power issue | Check 5V/6V supply to servos |

---

## 📸 Documentation Plan (Required for Portfolio)

### Photos to Take
- [ ] Mold design in Fusion 360
- [ ] Mold during 3D printing
- [ ] Ecoflex before mixing
- [ ] Ecoflex after mixing (clear)
- [ ] Pouring Ecoflex into mold
- [ ] Mold with Ecoflex (before cure)
- [ ] Demolded gripper (both fingers)
- [ ] Gripper with tubing attached
- [ ] Electronics on breadboard
- [ ] Soldered MOSFET drivers
- [ ] Wired gripper + arm
- [ ] Successful grip on egg
- [ ] Failed grip (if any) — also useful for learning!

### Video to Take
- [ ] Grip cycle (10 sec, slow motion)
- [ ] Egg test (full cycle)
- [ ] State machine transitions (with serial monitor overlay)

### Write-up (for portfolio)
- [ ] 1-page summary of build process
- [ ] BOM with actual costs
- [ ] Test results
- [ ] Lessons learnt
- [ ] Future improvements (e.g., 3-finger, ML control)

---

## 💰 Actual Cost Tracking

| Item | Planned (HK$) | Actual (HK$) | Notes |
|------|---------------:|-------------:|-------|
| Ecoflex 00-30 (1kg) | 350 | | Order from Smooth-On HK |
| 3D print mold | 50 | | Use university printer or local |
| Silicone tubing 2m | 40 | | |
| 2x Solenoid valves | 200 | | |
| Arduino Uno | 80 | | Already have? |
| Pressure sensor | 120 | | |
| Force sensor FSR402 | 80 | | |
| MOSFETs + diodes | 25 | | |
| Resistors + LEDs | 20 | | |
| 12V power supply | 80 | | |
| Air pump (12V) | 250 | | Or use syringe for low cost |
| Breadboard + wires | 50 | | |
| Misc (E-stop, connectors) | 20 | | |
| 3D print mount | 30 | | |
| **Subtotal** | **1,395** | | |
| Contingency (10%) | 140 | | |
| **Total budget** | **1,535** | | |

(Original estimate was 1,685 — saved 150 by using syringe instead of pump for initial testing)

---

## 📁 File Structure

```
builds/soft_gripper/
├── mold/
│   ├── gripper_mold_v1.stl          # 3D print file
│   ├── gripper_mold_v1.f3d          # Fusion 360 source
│   └── PRINT_INSTRUCTIONS.md
├── electronics/
│   ├── wiring_diagram.png            # Take photo of wired setup
│   ├── schematic.png                 # Draw schematic
│   └── BOM.md                        # Updated BOM
├── firmware/
│   ├── soft_gripper_control.ino     # Arduino code
│   └── README.md                     # Upload instructions
├── tests/
│   ├── test_results.md               # Test 1-6 results
│   ├── egg_test_photos/              # Photos of egg test
│   └── grip_force_data.csv           # Calibration data
├── docs/
│   ├── BUILD_PLAN.md                 # This file
│   ├── LESSONS_LEARNT.md             # After build
│   └── PORTFOLIO_SUMMARY.md          # 1-page for portfolio
└── photos/
    ├── step_01_mold_design.png
    ├── step_02_silicone_pour.png
    ├── step_03_demolded.png
    ├── step_04_wired.png
    ├── step_05_integrated.png
    └── step_06_egg_test.png
```

---

## 🎯 Success Criteria (Project Complete When)

✅ Mold designed and 3D printed
✅ Ecoflex cast successfully (no major defects)
✅ Electronics wired and tested
✅ Arduino code uploaded and working
✅ State machine transitions verified
✅ Egg test passed (5 cycles, no damage)
✅ Photos + video taken
✅ Build documentation complete
✅ Code pushed to GitHub
✅ 1-page portfolio summary written

**Time budget**: 14-20 hours
**Cost budget**: ≤HK$1,685
**Final result**: Functional hybrid rigid-soft robot gripper

---

## 🚀 Next Steps After Build

1. **Improve**: Add 3rd finger for better stability
2. **Sense**: Add FSR sensors along finger length for tactile feedback
3. **ML**: Train grasp prediction model from successful grasps
4. **FYP**: Use as foundation for MAEG4998/4999 FYP project
5. **Portfolio**: Include in IRE MSc application

---

**祝 build 順利!** 🛠️🦑💪

— KANG YIP SZE, 13 June 2026
