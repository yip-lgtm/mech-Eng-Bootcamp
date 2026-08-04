"""
Week 3 Soft Robotics — 1-DOF Soft Bending Actuator Simulation
A simple Python simulation of a pneumatic bending actuator
using Piecewise Constant Curvature (PCC) model.

Usage:
  python3 soft_actuator_sim.py
"""

import numpy as np
import matplotlib.pyplot as plt


def pcc_model(length, pressure, radius=0):
    """
    Piecewise Constant Curvature (PCC) model for a soft bending actuator.

    Args:
        length: actuator length (mm)
        pressure: input pressure (kPa)
        radius: initial radius of curvature (mm), 0 = straight

    Returns:
        tip_x, tip_y: end-effector position (mm)
        arc_length: actual arc length (mm)
    """
    # Empirical pressure-curvature relationship (calibrated for Ecoflex 00-30)
    # k = 1/r (curvature) increases linearly with pressure
    max_pressure = 100  # kPa
    max_curvature = 0.05  # 1/mm (radius 20mm at max pressure)

    if pressure <= 0:
        return length, 0.0, length

    pressure = min(pressure, max_pressure)
    curvature = (pressure / max_pressure) * max_curvature

    if curvature == 0:
        return length, 0.0, length

    # PCC kinematics
    arc_length = length  # Assumes inextensible
    radius = 1 / curvature
    theta = arc_length * curvature  # bending angle (radians)

    # Tip position in 2D
    tip_x = radius * np.sin(theta)
    tip_y = radius * (1 - np.cos(theta))

    return tip_x, tip_y, arc_length


def simulate_pressure_sweep(actuator_length=80):
    """Sweep pressure 0-100 kPa, plot tip trajectory."""
    pressures = np.linspace(0, 100, 50)
    tip_x_list = []
    tip_y_list = []

    for p in pressures:
        x, y, _ = pcc_model(actuator_length, p)
        tip_x_list.append(x)
        tip_y_list.append(y)

    return pressures, tip_x_list, tip_y_list


def simulate_actuator_shape(actuator_length=80, pressure=50, n_points=20):
    """Generate the shape of the actuator at a given pressure."""
    x, y, _ = pcc_model(actuator_length, pressure)
    curvature = (pressure / 100) * 0.05

    if curvature == 0:
        # Straight line
        s = np.linspace(0, actuator_length, n_points)
        return s, np.zeros(n_points)

    radius = 1 / curvature
    theta_max = actuator_length * curvature
    theta = np.linspace(0, theta_max, n_points)
    xs = radius * np.sin(theta)
    ys = radius * (1 - np.cos(theta))
    return xs, ys


def plot_results(actuator_length=80):
    """Plot 1) pressure vs tip position, 2) actuator shape at 3 pressures, 3) hysteresis demo."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Plot 1: Pressure vs Tip Position
    pressures, tip_x, tip_y = simulate_pressure_sweep(actuator_length)
    axes[0].plot(pressures, tip_x, 'b-', label='Tip X')
    axes[0].plot(pressures, tip_y, 'r-', label='Tip Y')
    axes[0].set_xlabel('Pressure (kPa)')
    axes[0].set_ylabel('Tip Position (mm)')
    axes[0].set_title('1-DOF Soft Actuator: Pressure vs Tip Position')
    axes[0].legend()
    axes[0].grid(True)

    # Plot 2: Actuator shape at 3 pressures
    colors = ['b-', 'g-', 'r-']
    pressures_to_show = [0, 50, 100]
    for p, color in zip(pressures_to_show, colors):
        xs, ys = simulate_actuator_shape(actuator_length, p)
        axes[1].plot(xs, ys, color, linewidth=2, label=f'P = {p} kPa')
    axes[1].set_xlabel('X (mm)')
    axes[1].set_ylabel('Y (mm)')
    axes[1].set_title('Actuator Shape (PCC Model)')
    axes[1].set_aspect('equal')
    axes[1].legend()
    axes[1].grid(True)

    # Plot 3: Hysteresis (real soft actuators have hysteresis)
    p_up = np.linspace(0, 100, 30)
    p_down = np.linspace(100, 0, 30)

    # Forward path
    _, tip_x_up, _ = simulate_pressure_sweep(actuator_length)
    # Backward path (with hysteresis: 5% lag)
    _, tip_x_down_raw, _ = simulate_pressure_sweep(actuator_length)
    tip_x_down = [x * 0.95 for x in reversed(tip_x_down_raw)]  # 5% lag

    axes[2].plot(p_up, tip_x_up[:len(p_up)], 'b-', label='Forward (pressurising)')
    axes[2].plot(p_down, tip_x_down, 'r--', label='Backward (depressurising)')
    axes[2].set_xlabel('Pressure (kPa)')
    axes[2].set_ylabel('Tip X (mm)')
    axes[2].set_title('Hysteresis (Realistic Behaviour)')
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig('soft_actuator_simulation.png', dpi=100, bbox_inches='tight')
    print("✅ Plot saved to: soft_actuator_simulation.png")

    # Print summary table
    print("\n=== Tip Position vs Pressure ===")
    print(f"{'Pressure (kPa)':<15} {'Tip X (mm)':<12} {'Tip Y (mm)':<12} {'Angle (°)':<10}")
    print("-" * 50)
    for p in [0, 20, 40, 60, 80, 100]:
        x, y, _ = pcc_model(actuator_length, p)
        curvature = (p / 100) * 0.05
        angle = np.degrees(actuator_length * curvature) if curvature > 0 else 0
        print(f"{p:<15} {x:<12.2f} {y:<12.2f} {angle:<10.1f}")


def demo_gripper_workspace():
    """Demo: 2-finger soft gripper workspace."""
    print("\n=== 2-Finger Soft Gripper Workspace ===")
    finger_length = 60  # mm each
    pressures = [0, 25, 50, 75, 100]

    print(f"{'Pressure (kPa)':<15} {'Gap (mm)':<12} {'Grip Force (N)':<15}")
    print("-" * 45)

    for p in pressures:
        # Each finger bends by half the gap
        x_each, _, _ = pcc_model(finger_length, p)
        gap = 2 * (finger_length - x_each)  # Gap = total closed distance
        # Empirical: grip force proportional to pressure
        grip_force = p * 0.5  # N (rough estimate)
        print(f"{p:<15} {gap:<12.2f} {grip_force:<15.2f}")

    print("\n💡 Grip an egg (40mm diameter): Need gap ~40mm at contact")
    print("   Adjust pressure to 50-70 kPa for safe grip")


if __name__ == "__main__":
    print("🦑 Week 3 Soft Robotics — PCC Simulation\n")
    print("Simulating 1-DOF pneumatic bending actuator (Ecoflex 00-30)...")

    # Run main simulation
    plot_results(actuator_length=80)

    # Run gripper demo
    demo_gripper_workspace()

    print("\n✅ Done! Open soft_actuator_simulation.png to see plots.")
    print("📚 Next: Try different lengths, add hysteresis model, or simulate closed-loop control.")
