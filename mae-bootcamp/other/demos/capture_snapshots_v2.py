"""
Capture snapshots of warehouse_robot_v2.py at different states
Shows Sensor Fusion Panel with real-time data
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import sys
sys.path.insert(0, 'demos')

import pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Import v2 demo's draw function
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
drop_zone = pygame.Rect(420, 550, 120, 80)
agent = WarehouseAgent(arm_controller, packages, drop_zone)

os.makedirs('/tmp/agent_v2_snapshots', exist_ok=True)
os.makedirs('/app/data-intelligence-architect/ire-bootcamp/demos/snapshots_v2', exist_ok=True)

target_states = ['moving_to_pkg', 'grabbing', 'moving_to_drop', 'dropping', 'idle']
states_captured = set()
frame_count = 0
snapshot_per_state = 1  # take 1 snapshot per state

while len(states_captured) < len(target_states) and frame_count < 3000:
    agent.step()
    if agent.state in target_states and agent.state not in states_captured:
        filename = f'/tmp/agent_v2_snapshots/state_{agent.state}.png'
        frame = draw_frame(arm, arm_controller, agent, packages, drop_zone, frame_count)
        pygame.image.save(frame, filename)
        # Also copy to repo
        repo_path = f'/app/data-intelligence-architect/ire-bootcamp/demos/snapshots_v2/state_{agent.state}.png'
        pygame.image.save(frame, repo_path)
        states_captured.add(agent.state)
        print(f'📸 {agent.state} (frame {frame_count}, delivered={agent.packages_delivered})')
    frame_count += 1

# Fallback: if some states were missed, force-capture by manually driving
# through one complete cycle with state-pinned snapshots
if len(states_captured) < 5:
    print(f'\n⚠️ Only {len(states_captured)}/5 states captured via natural run.')
    print('Restarting with manual state forcing...')
    # Reset agent
    agent2 = WarehouseAgent(arm_controller, packages, drop_zone)
    for target in target_states:
        if target not in states_captured:
            # Force the state and capture
            old_state = agent2.state
            agent2.state = target
            # Run a few steps to populate sensor data
            for _ in range(5):
                agent2.step()
            # Restore
            agent2.state = old_state
            filename = f'/tmp/agent_v2_snapshots/state_{target}.png'
            frame = draw_frame(arm, arm_controller, agent2, packages, drop_zone, 0)
            pygame.image.save(frame, filename)
            repo_path = f'/app/data-intelligence-architect/ire-bootcamp/demos/snapshots_v2/state_{target}.png'
            pygame.image.save(frame, repo_path)
            states_captured.add(target)
            print(f'📸 {target} (forced)')

print(f'\n=== Final ===')
print(f'Frames: {frame_count}')
print(f'Packages delivered: {agent.packages_delivered}')
print(f'Cycles: {agent.cycle_count}')
print(f'Snapshots: {len(states_captured)}')
