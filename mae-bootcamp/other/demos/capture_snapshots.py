"""
Headless capture of warehouse robot demo at different states
Generates PNG snapshots of agent at each state
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import sys
sys.path.insert(0, 'demos')
import pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

from warehouse_robot import Arm, Agent
from arm_controller import ArmController
import math

# Replicate main() drawing logic
def draw_frame(arm, arm_controller, agent, packages, drop_zone, auto_mode, action_log,
               packages_delivered, cycle_count):
    screen.fill((20, 25, 35))
    font = pygame.font.SysFont("Microsoft YaHei", 18)
    big_font = pygame.font.SysFont("Microsoft YaHei", 26)

    # Shelves
    pygame.draw.rect(screen, (80, 80, 90), (380, 200, 400, 20))
    pygame.draw.rect(screen, (80, 80, 90), (380, 300, 400, 20))
    # Drop Zone
    pygame.draw.rect(screen, (100, 200, 255), drop_zone, 4)
    drop_text = font.render("DROP ZONE", True, (100, 200, 255))
    screen.blit(drop_text, (drop_zone.x + 10, drop_zone.y - 25))

    # Packages
    for pkg in packages:
        if not pkg['grabbed']:
            pygame.draw.rect(screen, pkg['color'],
                             (pkg['pos'][0], pkg['pos'][1], 45, 45))
            screen.blit(font.render(pkg['id'], True, (0, 0, 0)),
                        (pkg['pos'][0]+15, pkg['pos'][1]+12))

    # Arm
    j1, j2, j3 = arm_controller.get_joint_positions()
    end_x, end_y = arm_controller.get_end_effector_position()
    pygame.draw.line(screen, (100, 200, 255), (650, 420), j1, 10)
    pygame.draw.line(screen, (255, 190, 90), j1, j2, 8)
    pygame.draw.line(screen, (120, 255, 140), j2, j3, 6)
    pygame.draw.circle(screen, (255, 80, 80), (int(j1[0]), int(j1[1])), 8)
    pygame.draw.circle(screen, (255, 200, 80), (int(j2[0]), int(j2[1])), 7)
    pygame.draw.circle(screen, (100, 255, 160), (int(j3[0]), int(j3[1])), 9)
    ee_color = (255, 50, 50) if arm_controller.has_package else (220, 220, 220)
    pygame.draw.circle(screen, ee_color, (int(end_x), int(end_y)), 10)

    # HUD
    state = arm_controller.get_state()
    mode = "🤖 AGENT LOOP" if auto_mode else "🖱️  MANUAL"
    status = f"{mode} | State: {agent.get_state_text()} | Held: {'Yes' if state['has_package'] else 'No'} | End: ({state['end_x']:.0f}, {state['end_y']:.0f})"
    screen.blit(font.render(status, True, (220, 220, 220)), (30, 25))

    remaining = sum(1 for p in packages if not p['grabbed'])
    stats = f"Packages delivered: {packages_delivered} | Cycles: {cycle_count} | Remaining: {remaining}"
    screen.blit(font.render(stats, True, (180, 180, 180)), (30, 50))

    help_text = "SPACE = Toggle Auto/Manual | G = Grab | R = Release | Mouse = Drag (Manual)"
    screen.blit(font.render(help_text, True, (140, 140, 140)), (30, HEIGHT - 30))

    if action_log:
        for i, msg in enumerate(action_log):
            screen.blit(font.render(msg, True, (200, 200, 200)), (30, 80 + i * 22))

    title = big_font.render("Gary Warehouse Robot — Perception-Action Loop Demo",
                            True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT - 65))

    return screen


# Setup
arm = Arm()
arm_controller = ArmController(arm, base_pos=(650, 420))
packages = [
    {"pos": (450, 300), "color": (50, 220, 50), "id": "A", "grabbed": False},
    {"pos": (550, 280), "color": (50, 220, 50), "id": "B", "grabbed": False},
    {"pos": (650, 320), "color": (50, 220, 50), "id": "C", "grabbed": False},
]
drop_zone = pygame.Rect(420, 550, 120, 80)
agent = Agent(arm_controller, packages, drop_zone)

# Capture states by stepping until we reach each interesting state
import os
os.makedirs('/tmp/agent_snapshots', exist_ok=True)

states_captured = set()
snapshots_taken = 0

for i in range(3000):
    agent.step()
    state = agent.state

    if state in ('idle', 'moving_to_pkg', 'grabbing', 'moving_to_drop', 'dropping') and state not in states_captured:
        filename = f'/tmp/agent_snapshots/state_{state}.png'
        frame = draw_frame(arm, arm_controller, agent, packages, drop_zone,
                          True, agent.action_log[-6:],
                          agent.packages_delivered, agent.cycle_count)
        pygame.image.save(frame, filename)
        states_captured.add(state)
        snapshots_taken += 1
        print(f'📸 Captured: {state} (step {i}) -> {filename}')
        if snapshots_taken >= 5:
            break

print(f'\n✅ Total snapshots: {snapshots_taken}')
print(f'Files:')
for f in sorted(os.listdir('/tmp/agent_snapshots')):
    path = f'/tmp/agent_snapshots/{f}'
    size = os.path.getsize(path)
    print(f'  {f} ({size} bytes)')
