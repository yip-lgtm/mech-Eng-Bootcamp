"""
Sensor Module — Simulates real robot sensors with noise/drift
+ Complementary Filter for IMU fusion (Gyro + Accel)

This module demonstrates how real robots would handle sensor uncertainty:
- Encoders: precise joint angles (small noise)
- Gyroscope: angular velocity (drifts over time)
- Accelerometer: linear acceleration (noisy)
- Force sensor: 0 when idle, >0 when grasping

Real robots would NEVER trust a single sensor. This module shows the
Perception → Sensor Fusion → Decision pipeline that production robots use.
"""
import math
import random


class SensorModule:
    """
    Simulates noisy sensors on a robot arm.
    Encoders + Gyro + Accel + Force sensor.
    Apply Complementary Filter to fuse Gyro + Accel into a single estimate.
    """

    def __init__(self, arm, noise_level=0.01, drift_rate=0.001):
        self.arm = arm
        self.noise = noise_level
        self.drift = drift_rate
        self.time = 0.0
        self.dt = 1.0 / 60.0  # assume 60 fps simulation

        # History for velocity/accel calculation
        self.prev_angles = [arm.theta1, arm.theta2, arm.theta3]
        self.prev_end = (0, 0)
        self.prev_vel = (0.0, 0.0)

        # Fusion state
        self.fused_angle = 0.0
        self.fused_position = (0.0, 0.0)

    def read_encoders(self):
        """Joint encoders: precise angle + small Gaussian noise"""
        return [
            self.arm.theta1 + random.gauss(0, self.noise * 0.1),
            self.arm.theta2 + random.gauss(0, self.noise * 0.1),
            self.arm.theta3 + random.gauss(0, self.noise * 0.1),
        ]

    def read_gyro(self):
        """
        Gyroscope: angular velocity (rad/s) + drift + noise.
        Drift accumulates over time — that's why we need fusion.
        """
        angles = [self.arm.theta1, self.arm.theta2, self.arm.theta3]
        angular_vel = [
            (a - p) / self.dt for a, p in zip(angles, self.prev_angles)
        ]
        self.prev_angles = angles
        # Add drift (proportional to time) + Gaussian noise
        return [
            av + self.drift * self.time + random.gauss(0, self.noise)
            for av in angular_vel
        ]

    def read_accel(self):
        """
        Accelerometer: linear acceleration of end effector (m/s²) + noise.
        Integrate twice to get position, but noise accumulates.
        """
        end_x, end_y = self.arm.get_end_effector_position()
        end = (end_x, end_y)
        vel = (
            (end[0] - self.prev_end[0]) / self.dt,
            (end[1] - self.prev_end[1]) / self.dt,
        )
        accel = (
            (vel[0] - self.prev_vel[0]) / self.dt,
            (vel[1] - self.prev_vel[1]) / self.dt,
        )
        self.prev_end = end
        self.prev_vel = vel
        return (
            accel[0] + random.gauss(0, self.noise * 10),
            accel[1] + random.gauss(0, self.noise * 10),
        )

    def read_force(self, has_package, pid_estimate=0.0):
        """
        Force sensor: 0 when idle, ~1.5 N when grasping.
        Now uses PID-based force estimate + real sensor noise fusion.
        Real production robots use actual F/T sensors at the wrist.
        """
        if has_package:
            # Combine real sensor (1.5N nominal) + PID estimate
            # This simulates the 'sensor fusion' between physical sensor
            # and model-based estimate (digital twin)
            real_sensor = 1.5 + random.gauss(0, 0.05)
            # Weighted fusion: 70% real sensor, 30% PID estimate
            fused = 0.7 * real_sensor + 0.3 * pid_estimate
            return fused
        return 0.0

    def complementary_filter(self, gyro_angle, accel_angle, alpha=0.98):
        """
        Fuse Gyro (high-pass, drifts) + Accel-derived angle (low-pass, noisy).
        alpha=0.98 means 98% gyro + 2% accel (typical for IMU).
        """
        return alpha * gyro_angle + (1 - alpha) * accel_angle

    def update(self, has_package=False, pid_estimate=0.0):
        """Run one sensor cycle, return fused state."""
        self.time += self.dt
        encoders = self.read_encoders()
        gyro = self.read_gyro()
        accel = self.read_accel()
        force = self.read_force(has_package, pid_estimate)

        # Derive angle from accelerometer (atan2 of gravity vector)
        # For a planar arm, "gravity" is just the y-acceleration
        accel_angle = math.atan2(accel[1], max(abs(accel[0]), 1e-3))
        # Integrate gyro to get angle (with drift)
        gyro_angle = self.fused_angle + gyro[0] * self.dt

        # Fuse
        self.fused_angle = self.complementary_filter(gyro_angle, accel_angle)
        self.fused_position = (encoders[0], encoders[1])

        return {
            "encoders": encoders,
            "gyro": gyro,
            "accel": accel,
            "force": force,
            "fused_angle": self.fused_angle,
            "fused_position": self.fused_position,
        }


class WarehouseAgent:
    """
    Full Perception → Sensor Fusion → Decision → Action loop.
    Uses SensorModule to perceive the world with realistic uncertainty.
    """

    def __init__(self, arm_controller, packages, drop_zone):
        self.arm = arm_controller
        self.sensors = SensorModule(arm_controller.arm)
        self.packages = packages
        self.drop_zone = drop_zone

        # Agent state
        self.state = "IDLE"
        self.target_package = None
        self.packages_delivered = 0
        self.cycle_count = 0

        # Logs
        self.action_log = []
        self.sensor_log = []
        self.fusion_log = []

    def perceive(self):
        """
        PERCEPTION: Read all sensors, fuse data, return state estimate.
        Now uses PID-based force estimate + real sensor fusion.
        Returns (end_x, end_y, packages, has_package) — fused estimate.
        """
        # Get PID-based force estimate from arm controller
        pid_force = self.arm.get_pid_force_estimate()
        sensor_data = self.sensors.update(self.arm.has_package, pid_force)
        # Log sensor readings (for debugging / visualization)
        self.sensor_log.append({
            "encoders": sensor_data["encoders"],
            "gyro": sensor_data["gyro"],
            "accel": sensor_data["accel"],
            "force": sensor_data["force"],
            "pid_estimate": pid_force,
        })
        # For end effector position, use direct kinematics (in production,
        # this would also be fused with vision)
        end_x, end_y = self.arm.get_end_effector_position()
        return end_x, end_y, self.packages, self.arm.has_package, sensor_data

    def think(self, perception):
        """
        THINKING: State machine + simple fusion-aware decision.
        The 'fusion_log' demonstrates how sensor data drives decisions.
        """
        end_x, end_y, packages, has_package, sensor_data = perception
        import math

        if self.state == "IDLE":
            # Find nearest ungrabbed package
            candidates = [p for p in packages if not p['grabbed']]
            if candidates:
                self.target_package = min(
                    candidates,
                    key=lambda p: math.hypot(
                        end_x - p['pos'][0] - 22,
                        end_y - p['pos'][1] - 22,
                    ),
                )
                self.state = "MOVING_TO_PKG"
                self._log(f"🎯 Target package {self.target_package['id']}")
                # Record sensor snapshot
                self.fusion_log.append({
                    "phase": "select_target",
                    "force": sensor_data["force"],
                    "fused_angle": sensor_data["fused_angle"],
                })

        elif self.state == "MOVING_TO_PKG":
            pkg = self.target_package
            self.arm.set_target(pkg['pos'][0] + 22, pkg['pos'][1] + 22)
            dist = math.hypot(
                end_x - pkg['pos'][0] - 22,
                end_y - pkg['pos'][1] - 22,
            )
            # Sensor-aware: check force to detect obstacles
            if sensor_data["force"] > 0.5 and not self.arm.has_package:
                self._log("⚠️ Force spike — possible obstacle")
            if dist < 30:
                self.state = "GRABBING"
                self.fusion_log.append({
                    "phase": "reached_pkg",
                    "force": sensor_data["force"],
                    "fused_angle": sensor_data["fused_angle"],
                })

        elif self.state == "GRABBING":
            self.arm.grab()
            self.target_package['grabbed'] = True
            self._log(f"✊ Grabbed package {self.target_package['id']}")
            self.state = "MOVING_TO_DROP"

        elif self.state == "MOVING_TO_DROP":
            cx = self.drop_zone.x + self.drop_zone.width / 2
            cy = self.drop_zone.y + self.drop_zone.height / 2
            self.arm.set_target(cx, cy)
            dist = math.hypot(end_x - cx, end_y - cy)
            # Verify force sensor confirms package still held
            if sensor_data["force"] < 0.3 and self.arm.has_package:
                self._log("⚠️ Force lost — package dropped!")
                self.target_package['grabbed'] = False
                self.arm.release()
                self.state = "IDLE"
                return
            if dist < 30:
                self.state = "DROPPING"
                self.fusion_log.append({
                    "phase": "reached_drop",
                    "force": sensor_data["force"],
                    "fused_angle": sensor_data["fused_angle"],
                })

        elif self.state == "DROPPING":
            self.arm.release()
            self.target_package['grabbed'] = False
            self.packages_delivered += 1
            self.cycle_count += 1
            self._log(
                f"📦 Delivered package {self.target_package['id']} "
                f"(Total: {self.packages_delivered})"
            )
            self.target_package = None
            self.state = "IDLE"

    def step(self):
        """Single Perception-Action cycle with sensor fusion."""
        perception = self.perceive()
        self.think(perception)
        self.arm.update()

    def _log(self, msg):
        self.action_log.append(msg)
        if len(self.action_log) > 10:
            self.action_log.pop(0)

    def get_state_text(self):
        return self.state.replace("_", " ").title()
