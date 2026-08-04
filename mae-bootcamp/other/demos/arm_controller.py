"""
ArmController for Gary Warehouse Robot
3R Planar Arm with Inverse Kinematics + Smooth Movement + PID Closed-Loop

Mechatronics features:
- PID position control (per joint, with anti-windup)
- Speed/acceleration limits (simulates real Servo torque/speed limits)
- Force feedback for grab/release (distance-based)
- Auto grab/release on reaching target
- IK treats 3R arm as 2-link (effective L2 = l2 + l3) for stability
"""

import math
import pygame


class PIDController:
    """
    PID controller for one joint.
    Used to simulate closed-loop position control of a Servo motor.
    """
    def __init__(self, kp=1.5, ki=0.1, kd=0.3, max_output=10.0, max_integral=1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_output = max_output
        self.max_integral = max_integral
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, target, current, dt=1.0 / 60.0):
        error = target - current
        self.integral += error * dt
        # Anti-windup
        self.integral = max(-self.max_integral, min(self.max_integral, self.integral))
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        output = (
            self.kp * error
            + self.ki * self.integral
            + self.kd * derivative
        )
        return max(-self.max_output, min(self.max_output, output))

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0


class ArmController:
    """
    Closed-loop position controller for 3R planar arm.
    Simulates a real Servo with:
    - Position feedback (joint encoders)
    - Speed limit (max angular velocity)
    - Torque limit (max angular acceleration)
    - PID control per joint
    - Force feedback (distance-based grab check)
    - Auto grab/release on reach
    """
    def __init__(self, arm, base_pos=(650, 420), max_speed=2.0, max_accel=8.0):
        self.arm = arm
        self.base_x, self.base_y = base_pos
        self.target_x = None
        self.target_y = None
        self.smooth_speed = 0.08  # Legacy interpolation factor (unused)
        self.has_package = False
        self.grab_radius = 35  # Distance threshold for grab
        self.current_package = None
        self.packages = []  # Set externally via set_packages()
        self.frame_count = 0  # Internal frame counter for grab flash

        # Servo parameters (closed-loop simulation)
        self.max_speed = max_speed      # rad/s
        self.max_accel = max_accel      # rad/s²
        self.dt = 1.0 / 60.0            # Control loop period (60 Hz)
        self.is_moving = False

        # PID per joint (different gains because each joint has different load)
        self.pid1 = PIDController(kp=2.0, ki=0.05, kd=0.4, max_output=max_accel)
        self.pid2 = PIDController(kp=2.0, ki=0.05, kd=0.4, max_output=max_accel)
        self.pid3 = PIDController(kp=2.5, ki=0.08, kd=0.5, max_output=max_accel)

        # Joint angle state (smooth IK)
        self.target_theta1 = arm.theta1
        self.target_theta2 = arm.theta2
        self.target_theta3 = arm.theta3

        # Telemetry
        self.torque_log = [[], [], []]
        self.speed_log = [[], [], []]
        self.angle_error_log = [[], [], []]
        # Grab success tracking (for visualization flash)
        self.last_grab_frame = -1000  # Long ago, so no flash on start

    def set_packages(self, packages):
        """Inject package list for auto-grab distance check"""
        self.packages = packages

    def get_end_effector_position(self):
        """Get current end effector in world coords"""
        local_x, local_y = self.arm.get_end_effector_position()
        return self.base_x + local_x, self.base_y - local_y

    def get_joint_positions(self):
        """Get joint positions in world coords"""
        j1, j2, j3 = self.arm.get_joint_positions()
        return (
            (self.base_x + j1[0], self.base_y - j1[1]),
            (self.base_x + j2[0], self.base_y - j2[1]),
            (self.base_x + j3[0], self.base_y - j3[1]),
        )

    def inverse_kinematics(self, target_x, target_y):
        """
        Compute joint angles to reach target (x, y) in world coords.
        Treats the 3R arm as 2-link with effective L2 = l2 + l3.
        Wrist joint (theta3) is set to 0 (straight) for stability.
        """
        # Convert world to local (flip y for screen coords)
        lx = target_x - self.base_x
        ly = self.base_y - target_y

        # 2-link IK with effective second link (l2 + l3)
        L1 = self.arm.l1
        L2 = self.arm.l2 + self.arm.l3

        r = math.sqrt(lx**2 + ly**2)
        r = max(min(r, L1 + L2 - 1), abs(L1 - L2) + 1)

        # Elbow angle
        cos_t2 = (r**2 - L1**2 - L2**2) / (2 * L1 * L2)
        cos_t2 = max(-1, min(1, cos_t2))

        # Elbow-down (negative) for typical reaching posture
        theta2 = -math.acos(cos_t2)

        # Shoulder angle
        theta1 = math.atan2(ly, lx) - math.atan2(
            L2 * math.sin(theta2),
            L1 + L2 * math.cos(theta2)
        )

        # Wrist kept straight (visually still 3R, but IK treats as 2-link)
        theta3 = 0.0

        return theta1, theta2, theta3

    def set_target(self, x, y):
        """Set target position for smooth movement"""
        self.target_x = x
        self.target_y = y
        # Compute IK target
        self.target_theta1, self.target_theta2, self.target_theta3 = \
            self.inverse_kinematics(x, y)
        self.is_moving = True

    def update(self):
        """
        Closed-loop PID control of each joint.
        Applies speed and acceleration limits.
        Then auto-checks for grab/release conditions.
        """
        self.frame_count += 1
        targets = [self.target_theta1, self.target_theta2, self.target_theta3]
        currents = [self.arm.theta1, self.arm.theta2, self.arm.theta3]
        pids = [self.pid1, self.pid2, self.pid3]
        torques = []

        for i, (tgt, cur, pid) in enumerate(zip(targets, currents, pids)):
            error = tgt - cur
            self.angle_error_log[i].append(abs(error))
            if len(self.angle_error_log[i]) > 100:
                self.angle_error_log[i].pop(0)

            # PID output = torque command
            torque = pid.compute(tgt, cur, self.dt)
            # Limit torque (acceleration)
            torque = max(-self.max_accel, min(self.max_accel, torque))
            self.torque_log[i].append(torque)
            if len(self.torque_log[i]) > 100:
                self.torque_log[i].pop(0)

            # Apply torque as velocity change
            velocity = torque * self.dt
            # Limit speed
            velocity = max(-self.max_speed * self.dt,
                          min(self.max_speed * self.dt, velocity))
            self.speed_log[i].append(velocity)
            if len(self.speed_log[i]) > 100:
                self.speed_log[i].pop(0)

            torques.append(torque)
            # Update joint angle
            if i == 0:
                self.arm.theta1 += velocity
            elif i == 1:
                self.arm.theta2 += velocity
            else:
                self.arm.theta3 += velocity

        # Check if reached target
        max_error = max(abs(t - c) for t, c in zip(targets, currents))
        if max_error < 0.05:  # Tighter threshold so is_moving=True is meaningful
            self.is_moving = False

    def grab(self):
        """
        Force-feedback based grab.
        Checks distance to each package; grabs nearest if within grab_radius.
        Returns True if grab succeeded.
        """
        if self.has_package:
            return False

        end_x, end_y = self.get_end_effector_position()
        for pkg in self.packages:
            if pkg.get('grabbed', False):
                continue
            px, py = pkg['pos'][0] + 22, pkg['pos'][1] + 22
            distance = math.hypot(end_x - px, end_y - py)
            if distance < self.grab_radius:
                pkg['grabbed'] = True
                self.has_package = True
                self.current_package = pkg
                # Track grab success for visualization (using internal frame counter)
                self.last_grab_frame = self.frame_count
                return True
        return False

    def get_pid_force_estimate(self):
        """
        Estimate contact force from PID output.
        Real robots have force/torque sensors, but PID integral term
        approximates the steady-state error force needed to maintain position.
        """
        if not self.torque_log[0]:
            return 0.0
        # Sum of absolute torques across joints (rough proxy for force)
        total_torque = (
            abs(self.torque_log[0][-1]) +
            abs(self.torque_log[1][-1]) +
            abs(self.torque_log[2][-1])
        )
        # Convert torque to force (rough: 0.3 N per N·m)
        return total_torque * 0.3

    def release(self):
        """Release any held package"""
        if self.has_package and self.current_package:
            self.current_package['grabbed'] = False
            self.current_package = None
        self.has_package = False
        return True

    def can_reach(self, x, y):
        """Check if (x, y) is within reach"""
        lx = x - self.base_x
        ly = self.base_y - y
        r = math.sqrt(lx**2 + ly**2)
        return abs(self.arm.l1 - self.arm.l2) < r < (self.arm.l1 + self.arm.l2)

    def get_state(self):
        """Get current state for external monitoring"""
        end_x, end_y = self.get_end_effector_position()
        return {
            'has_package': self.has_package,
            'end_x': end_x,
            'end_y': end_y,
            'theta1': math.degrees(self.arm.theta1),
            'theta2': math.degrees(self.arm.theta2),
            'theta3': math.degrees(self.arm.theta3),
            'is_moving': self.is_moving,
            'current_package': (self.current_package['id']
                               if self.current_package else None),
        }


class MechatronicsSystem:
    """
    Full closed-loop system integration.
    Wires ArmController + WarehouseAgent + Sensors into one run_step().

    This is the top-level orchestrator. The Agent decides what to do,
    the ArmController executes with PID control, and the Sensors provide
    the Perception data for next iteration.
    """
    def __init__(self, arm_controller, agent, drop_zone):
        self.arm = arm_controller
        self.agent = agent
        self.drop_zone = drop_zone
        self.frame_count = 0
        self.event_log = []

    def run_step(self):
        """
        One full Perception → Think → Action cycle.
        Called once per frame.
        """
        # 1. Perceive
        perception = self.agent.perceive()

        # 2. Think (decide next state)
        self.agent.think(perception)

        # 3. Act (PID control)
        self.arm.update()

        # 4. Auto check: if reached target, try grab/release
        state = self.arm.get_state()
        if not state['is_moving']:
            if not state['has_package'] and self.agent.state == "MOVING_TO_PKG":
                # Just arrived at package
                if self.arm.grab():
                    self._log(f"✊ Auto-grabbed at end effector")
            elif state['has_package'] and self.agent.state == "MOVING_TO_DROP":
                # Just arrived at drop zone
                end_x, end_y = self.arm.get_end_effector_position()
                if self.drop_zone.collidepoint(end_x, end_y):
                    self.arm.release()
                    self._log(f"📦 Auto-released at drop zone")

        self.frame_count += 1

    def _log(self, msg):
        self.event_log.append(msg)
        if len(self.event_log) > 20:
            self.event_log.pop(0)
