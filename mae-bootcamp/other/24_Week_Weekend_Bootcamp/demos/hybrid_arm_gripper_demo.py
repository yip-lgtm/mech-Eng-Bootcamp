"""
Week 3 Soft Robotics — Hybrid Demo
3R Rigid Arm + 2-Finger Soft Pneumatic Gripper + State Machine

Combines:
- Simple 3R arm forward kinematics (3 revolute joints, planar)
- Soft pneumatic gripper (PCC model from soft_actuator_sim.py)
- 6-state state machine (APPROACH → SOFT_CONTACT → GRIP → HOLD → LIFT → RELEASE)
- Visualisation (matplotlib)

Usage:
  python3 hybrid_arm_gripper_demo.py
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from enum import Enum


# ============================================================================
# 3R Rigid Arm (Planar, simplified)
# ============================================================================

class ThreeRArm:
    """Simple planar 3R arm with link lengths L1, L2, L3."""

    def __init__(self, L1=80, L2=80, L3=50):
        """All lengths in mm."""
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.theta1 = 0.0  # Shoulder (rad)
        self.theta2 = 0.0  # Elbow (rad)
        self.theta3 = 0.0  # Wrist (rad)

    def forward_kinematics(self):
        """Compute end-effector position (x, y) in 2D."""
        x1 = self.L1 * math.cos(self.theta1)
        y1 = self.L1 * math.sin(self.theta1)

        x2 = x1 + self.L2 * math.cos(self.theta1 + self.theta2)
        y2 = y1 + self.L2 * math.sin(self.theta1 + self.theta2)

        x3 = x2 + self.L3 * math.cos(self.theta1 + self.theta2 + self.theta3)
        y3 = y2 + self.L3 * math.sin(self.theta1 + self.theta2 + self.theta3)

        return (x3, y3), [(0, 0), (x1, y1), (x2, y2), (x3, y3)]

    def move_towards(self, target_x, target_y, step=0.05):
        """Simple gradient-descent IK: move angles towards target."""
        _, current_pts = self.forward_kinematics()
        cur_x, cur_y = current_pts[-1]

        # Simple heuristic: adjust each joint slightly towards target direction
        dx = target_x - cur_x
        dy = target_y - cur_y
        dist = math.sqrt(dx**2 + dy**2)
        if dist < 1.0:
            return True  # Reached

        # Normalize direction
        if dist > 0:
            dx /= dist
            dy /= dist

        # Move joints (heuristic: theta1 follows overall direction, theta2 + theta3 for reach)
        target_angle = math.atan2(dy, dx)
        self.theta1 += (target_angle - self.theta1) * step
        self.theta2 += (math.pi/4 - self.theta2) * step  # Elbow bent
        self.theta3 += (math.pi/4 - self.theta3) * step  # Wrist straight

        # Clamp angles
        self.theta1 = max(-math.pi/2, min(math.pi/2, self.theta1))
        self.theta2 = max(-math.pi/2, min(math.pi, self.theta2))
        self.theta3 = max(-math.pi/2, min(math.pi/2, self.theta3))
        return False


# ============================================================================
# Soft Pneumatic Gripper (PCC model, 2 fingers)
# ============================================================================

class SoftGripper:
    """2-finger soft pneumatic gripper using PCC model."""

    def __init__(self, finger_length=60, max_pressure=100):
        self.finger_length = finger_length  # mm
        self.max_pressure = max_pressure  # kPa
        self.pressure = 0  # Current pressure (kPa)

    def set_pressure(self, pressure):
        """Set pneumatic pressure (0-max_pressure kPa)."""
        self.pressure = max(0, min(self.max_pressure, pressure))

    def get_gap(self):
        """Compute current gripper gap (mm) based on pressure."""
        if self.pressure == 0:
            return 2 * self.finger_length  # Fully open
        curvature = (self.pressure / self.max_pressure) * 0.05
        radius = 1 / curvature
        theta = self.finger_length * curvature
        tip_x = radius * math.sin(theta)
        # Gap = 2 * (finger_length - tip_x)
        gap = 2 * (self.finger_length - tip_x)
        return gap

    def get_grip_force(self):
        """Estimate grip force (N) at current pressure."""
        # Empirical: F ≈ 0.5 * pressure (linear)
        return self.pressure * 0.5

    def is_grasping(self, object_width):
        """Check if gripper is grasping an object of given width."""
        gap = self.get_gap()
        return abs(gap - object_width) < 5.0  # 5mm tolerance


# ============================================================================
# State Machine
# ============================================================================

class GripperState(Enum):
    APPROACH = 1
    SOFT_CONTACT = 2
    GRIP = 3
    HOLD = 4
    LIFT = 5
    RELEASE = 6


class HybridController:
    """Integrates 3R arm + soft gripper with state machine."""

    def __init__(self, object_pos=(150, 80), object_width=40):
        self.arm = ThreeRArm()
        self.gripper = SoftGripper()
        self.state = GripperState.APPROACH
        self.object_pos = object_pos
        self.object_width = object_width
        self.contact_force = 0.0
        self.state_time = 0

    def simulate_step(self, dt=0.1):
        """Run one simulation step."""
        self.state_time += dt
        ee_pos, _ = self.arm.forward_kinematics()

        if self.state == GripperState.APPROACH:
            # Move arm to object position
            reached = self.arm.move_towards(self.object_pos[0], self.object_pos[1])
            # Simulate contact force increasing as we get close
            dist_to_obj = math.sqrt((ee_pos[0] - self.object_pos[0])**2 +
                                     (ee_pos[1] - self.object_pos[1])**2)
            self.contact_force = max(0, (50 - dist_to_obj) * 0.1)  # 0-5N
            if self.contact_force > 0.5:
                self._transition(GripperState.SOFT_CONTACT)

        elif self.state == GripperState.SOFT_CONTACT:
            # Slow down, monitor force
            self.contact_force = min(5.0, self.contact_force + 0.3)
            if self.contact_force > 2.0:
                self._transition(GripperState.GRIP)

        elif self.state == GripperState.GRIP:
            # Ramp up pressure
            target_pressure = 60  # kPa
            self.gripper.set_pressure(self.gripper.pressure + 5)
            self.contact_force = min(8.0, self.contact_force + 0.1)
            if self.gripper.pressure >= target_pressure and self.state_time > 1.0:
                self._transition(GripperState.HOLD)

        elif self.state == GripperState.HOLD:
            # Maintain pressure, check for slip
            if self.contact_force < 1.0:
                # Slip detected
                self.gripper.set_pressure(self.gripper.pressure + 5)
            if self.state_time > 2.0:
                self._transition(GripperState.LIFT)

        elif self.state == GripperState.LIFT:
            # Move arm up
            target_pos = (self.object_pos[0], self.object_pos[1] + 30)
            self.arm.move_towards(*target_pos)
            if self.state_time > 2.0:
                self._transition(GripperState.RELEASE)

        elif self.state == GripperState.RELEASE:
            # Depressurise
            self.gripper.set_pressure(self.gripper.pressure - 5)
            if self.gripper.pressure <= 0:
                self.state = GripperState.APPROACH  # Reset
                self.state_time = 0

    def _transition(self, new_state):
        self.state = new_state
        self.state_time = 0

    def status_string(self):
        ee_pos, _ = self.arm.forward_kinematics()
        return (f"State: {self.state.name:<12} | "
                f"EE: ({ee_pos[0]:6.1f}, {ee_pos[1]:6.1f}) mm | "
                f"Pressure: {self.gripper.pressure:5.1f} kPa | "
                f"Gap: {self.gripper.get_gap():5.1f} mm | "
                f"Force: {self.gripper.get_grip_force():4.1f} N | "
                f"Contact: {self.contact_force:4.1f} N")


# ============================================================================
# Visualisation
# ============================================================================

def run_simulation():
    """Run full hybrid simulation with visualisation."""
    print("🦑 Hybrid Arm-Gripper Demo")
    print("=" * 80)

    controller = HybridController(object_pos=(150, 60), object_width=40)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-50, 300)
    ax.set_ylim(-50, 200)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_title('3R Rigid Arm + 2-Finger Soft Gripper — Hybrid Demo')

    # Plot object (egg-shaped, 40mm wide)
    obj = patches.Ellipse(controller.object_pos, controller.object_width, 50,
                          facecolor='lightyellow', edgecolor='orange', linewidth=2)
    ax.add_patch(obj)
    ax.text(controller.object_pos[0], controller.object_pos[1] - 40,
            'Object\n(egg)', ha='center', fontsize=9, color='darkorange')

    # Storage for state traces
    ee_trace_x = []
    ee_trace_y = []

    # Run simulation
    n_steps = 200
    for step in range(n_steps):
        controller.simulate_step(dt=0.1)

        # Update plot every 5 steps
        if step % 5 == 0:
            ax.clear()
            ax.set_xlim(-50, 300)
            ax.set_ylim(-50, 200)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('X (mm)')
            ax.set_ylabel('Y (mm)')
            ax.set_title(f'3R Arm + Soft Gripper — Step {step} | {controller.status_string()[:60]}')

            # Plot object
            ax.add_patch(patches.Ellipse(controller.object_pos,
                                         controller.object_width, 50,
                                         facecolor='lightyellow',
                                         edgecolor='orange', linewidth=2))

            # Plot arm
            ee_pos, arm_pts = controller.arm.forward_kinematics()
            xs = [p[0] for p in arm_pts]
            ys = [p[1] for p in arm_pts]
            ax.plot(xs, ys, 'b-o', linewidth=3, markersize=8, label='Rigid Arm')

            # Plot gripper (2 fingers)
            grip_x, grip_y = ee_pos
            gap = controller.gripper.get_gap()
            finger_offset = gap / 2

            # Finger 1 (top)
            ax.plot([grip_x, grip_x - finger_offset * 0.3],
                    [grip_y, grip_y + finger_offset * 0.5],
                    'g-', linewidth=4, alpha=0.7, label='Soft Finger 1')
            # Finger 2 (bottom)
            ax.plot([grip_x, grip_x - finger_offset * 0.3],
                    [grip_y, grip_y - finger_offset * 0.5],
                    'g-', linewidth=4, alpha=0.7, label='Soft Finger 2')

            # Highlight grasped object if gripper is grasping
            if controller.gripper.is_grasping(controller.object_width):
                ax.add_patch(patches.Circle(controller.object_pos, 22,
                                            facecolor='gold', alpha=0.5))

            # State indicator
            state_color = {
                GripperState.APPROACH: 'lightblue',
                GripperState.SOFT_CONTACT: 'lightyellow',
                GripperState.GRIP: 'orange',
                GripperState.HOLD: 'lightgreen',
                GripperState.LIFT: 'lightgreen',
                GripperState.RELEASE: 'lightgray',
            }
            ax.text(0.02, 0.98, f'STATE: {controller.state.name}',
                    transform=ax.transAxes, fontsize=14, fontweight='bold',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor=state_color[controller.state], alpha=0.8))

            ax.legend(loc='upper right', fontsize=8)
            plt.pause(0.05)

    # Final summary
    print("\n=== Simulation Summary ===")
    print(controller.status_string())
    print("\n✅ Demo complete. Close plot window to exit.")
    plt.show()


def run_text_simulation():
    """Run text-only simulation (no plot, for quick testing)."""
    print("🦑 Hybrid Arm-Gripper Demo (Text Mode)")
    print("=" * 80)

    controller = HybridController(object_pos=(150, 60), object_width=40)

    for step in range(150):
        controller.simulate_step(dt=0.1)
        if step % 10 == 0:
            print(f"Step {step:3d} | {controller.status_string()}")

    print("\n=== Final State ===")
    print(controller.status_string())


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "text":
        run_text_simulation()
    else:
        run_simulation()
