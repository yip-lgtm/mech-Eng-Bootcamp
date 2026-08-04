"""
Capture grab success flash + high force warning
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import sys
sys.path.insert(0, 'demos')

import pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

from warehouse_robot_v2 import draw_frame
from warehouse_robot import Arm
from arm_controller import ArmController
from sensor_fusion import WarehouseAgent

arm = Arm()
arm_controller = ArmController(arm, base_pos=(650, 420))
packages = [
    {"pos": (450, 300), "color": (50, 220, 50), "id": "A", "grabbed": False},
    {"pos": (550, 280), "color": (50, 220, 50), "id": "B", "grabbed": False},
    {"pos": (650, 320), "color": (50, 220, 50), "id": "C", "grabbed": False},
]
arm_controller.set_packages(packages)
drop_zone = pygame.Rect(420, 550, 120, 80)
agent = WarehouseAgent(arm_controller, packages, drop_zone)

# Move to package and grab
arm_controller.set_target(672, 342)  # Package C
for _ in range(200):
    arm_controller.update()
arm_controller.grab()
# Populate sensor log
for _ in range(20):
    agent.perceive()

# Snapshot 1: right after grab (✓ GRABBED! flash)
print('=== Grab success flash ===')
filename = '/tmp/agent_v3_snapshots/grab_success.png'
frame = draw_frame(arm, arm_controller, agent, packages, drop_zone, 100)
pygame.image.save(frame, filename)
repo_path = '/app/data-intelligence-architect/ire-bootcamp/demos/snapshots_v3/grab_success.png'
pygame.image.save(frame, repo_path)
state = arm_controller.get_state()
print(f'   ✓ GRABBED! visible, Held: {state["has_package"]}')

# Snapshot 2: high force warning (manually inject high force)
print('=== High force warning ===')
# Force multiple updates to accumulate PID integral
for _ in range(50):
    arm_controller.update()
# Manually inject high force in sensor log (simulate jammed package)
if agent.sensor_log:
    agent.sensor_log[-1]["force"] = 2.6  # Above 2.5N danger threshold
    # Also add a couple more entries with high force
    for _ in range(5):
        agent.sensor_log.append({
            "encoders": [0.5, -1.0, 0.0],
            "gyro": [0.0, 0.0],
            "accel": (0.0, 0.0),
            "force": 2.6,
            "pid_estimate": 8.5,
        })

filename = '/tmp/agent_v3_snapshots/high_force_warning.png'
frame = draw_frame(arm, arm_controller, agent, packages, drop_zone, 200)
pygame.image.save(frame, filename)
repo_path = '/app/data-intelligence-architect/ire-bootcamp/demos/snapshots_v3/high_force_warning.png'
pygame.image.save(frame, repo_path)
print(f'   🔴 Arm red (force > 2.5N), latest force: {agent.sensor_log[-1]["force"]}N')

print('Done!')
