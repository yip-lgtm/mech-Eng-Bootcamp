# 2-Finger Pneumatic Soft Gripper — Build

**Project**: Week 3 IRE Bootcamp deliverable
**Engineer**: KANG YIP SZE 施耿業
**Started**: 13 June 2026

## Status: 🟡 Planning (Ready to build)

## Quick Links
- [Build Plan](docs/BUILD_PLAN.md)
- [Arduino Firmware](firmware/soft_gripper_control.ino)
- [BOM](docs/BOM.md) (in BUILD_PLAN.md)
- [Tests](tests/)

## Folder Structure
```
soft_gripper/
├── mold/          # 3D print files for mold
├── electronics/   # Wiring diagrams, schematics
├── firmware/      # Arduino code
├── tests/         # Test results
├── docs/          # Build plan, lessons learnt
└── photos/        # Build photos
```

## Quick Start
1. Read [BUILD_PLAN.md](docs/BUILD_PLAN.md) for full instructions
2. Print mold (mold/gripper_mold_v1.stl)
3. Mix and pour Ecoflex 00-30
4. Wire up electronics per Section 15
5. Upload Arduino firmware
6. Test with egg

## Time & Cost
- **Time**: 14-20 hours (2 weekends)
- **Cost**: ~HK$1,535 (with contingency)

## Success Criteria
✅ Egg test passed (5 grip-release cycles, no damage)
✅ All 6 state machine states working
✅ Force + pressure closed-loop working
✅ Emergency stop functional
