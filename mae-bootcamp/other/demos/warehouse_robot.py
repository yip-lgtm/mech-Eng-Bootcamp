"""
Gary Warehouse Robot - 3R Arm + Agent Loop (Perception-Action Loop)
Week 1 Embodied AI Demo - Autonomous Mode
"""

import pygame
import numpy as np
import sys
import math
from arm_controller import ArmController

# ==================== Arm (3R Planar) ====================
class Arm:
    def __init__(self):
        self.l1, self.l2, self.l3 = 160, 130, 100
        self.theta1 = np.deg2rad(20)
        self.theta2 = np.deg2rad(60)
        self.theta3 = np.deg2rad(-30)

    def get_end_effector_position(self):
        x1 = self.l1 * np.cos(self.theta1)
        y1 = self.l1 * np.sin(self.theta1)
        x2 = x1 + self.l2 * np.cos(self.theta1 + self.theta2)
        y2 = y1 + self.l2 * np.sin(self.theta1 + self.theta2)
        x3 = x2 + self.l3 * np.cos(self.theta1 + self.theta2 + self.theta3)
        y3 = y2 + self.l3 * np.sin(self.theta1 + self.theta2 + self.theta3)
        return x3, y3

    def get_joint_positions(self):
        x1 = self.l1 * np.cos(self.theta1)
        y1 = self.l1 * np.sin(self.theta1)
        x2 = x1 + self.l2 * np.cos(self.theta1 + self.theta2)
        y2 = y1 + self.l2 * np.sin(self.theta1 + self.theta2)
        x3 = x2 + self.l3 * np.cos(self.theta1 + self.theta2 + self.theta3)
        y3 = y2 + self.l3 * np.sin(self.theta1 + self.theta2 + self.theta3)
        return (x1, y1), (x2, y2), (x3, y3)


# ==================== Agent (Perception-Action Loop) ====================
class Agent:
    """
    Embodied AI Agent running Perception-Action Loop.
    States: IDLE -> SEEKING -> GRABBING -> MOVING_TO_DROP -> DROPPING -> IDLE
    """
    IDLE = 'idle'
    MOVING_TO_PKG = 'moving_to_pkg'
    GRABBING = 'grabbing'
    MOVING_TO_DROP = 'moving_to_drop'
    DROPPING = 'dropping'

    def __init__(self, arm_controller, packages, drop_zone):
        self.arm = arm_controller
        self.packages = packages
        self.drop_zone = drop_zone
        self.state = self.IDLE
        self.target_package = None
        self.action_log = []
        self.packages_delivered = 0
        self.cycle_count = 0

    def perceive(self):
        """PERCEPTION: Find nearest ungrabbed package"""
        end_x, end_y = self.arm.get_end_effector_position()
        candidates = [p for p in self.packages if not p['grabbed']]

        if not candidates:
            return None

        # Find nearest by Euclidean distance
        nearest = min(candidates, key=lambda p: math.hypot(
            end_x - p['pos'][0] - 22,  # +22 for package center
            end_y - p['pos'][1] - 22
        ))
        return nearest

    def think(self):
        """THINKING: Decide next action based on state"""
        end_x, end_y = self.arm.get_end_effector_position()

        if self.state == self.IDLE:
            # Look for a new package
            self.target_package = self.perceive()
            if self.target_package:
                self.state = self.MOVING_TO_PKG
                self.log(f"🎯 Target package {self.target_package['id']}")

        elif self.state == self.MOVING_TO_PKG:
            # Move toward target package
            assert self.target_package is not None
            pkg = self.target_package
            target_x = pkg['pos'][0] + 22
            target_y = pkg['pos'][1] + 22
            self.arm.set_target(target_x, target_y)

            # Check if close enough to grab
            dist = math.hypot(end_x - target_x, end_y - target_y)
            if dist < 30:
                self.state = self.GRABBING

        elif self.state == self.GRABBING:
            self.arm.grab()
            pkg = self.target_package
            pkg['grabbed'] = True
            self.log(f"✊ Grabbed package {pkg['id']}")
            self.state = self.MOVING_TO_DROP

        elif self.state == self.MOVING_TO_DROP:
            # Move to drop zone
            drop_x = self.drop_zone.x + self.drop_zone.width / 2
            drop_y = self.drop_zone.y + self.drop_zone.height / 2
            self.arm.set_target(drop_x, drop_y)

            dist = math.hypot(end_x - drop_x, end_y - drop_y)
            if dist < 30:
                self.state = self.DROPPING

        elif self.state == self.DROPPING:
            self.arm.release()
            pkg = self.target_package
            pkg['grabbed'] = False
            # Reset for next cycle
            self.packages_delivered += 1
            self.cycle_count += 1
            self.log(f"📦 Delivered package {pkg['id']} (Total: {self.packages_delivered})")
            self.target_package = None
            self.state = self.IDLE

    def log(self, msg):
        self.action_log.append(msg)
        if len(self.action_log) > 6:
            self.action_log.pop(0)
        print(msg)

    def step(self):
        """Single Perception-Action cycle"""
        self.think()
        self.arm.update()

    def get_state_text(self):
        return f"{self.state.upper().replace('_', ' ')}"


# ==================== Main ====================
def main():
    pygame.init()
    WIDTH, HEIGHT = 1200, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gary Warehouse Robot - 3R Arm + Agent Loop")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Microsoft YaHei", 18)
    big_font = pygame.font.SysFont("Microsoft YaHei", 26)

    arm = Arm()
    arm_controller = ArmController(arm, base_pos=(650, 420))

    # 3 packages on shelf (all within arm reach from base 650,420)
    packages = [
        {"pos": (450, 300), "color": (50, 220, 50), "id": "A", "grabbed": False},
        {"pos": (550, 280), "color": (50, 220, 50), "id": "B", "grabbed": False},
        {"pos": (650, 320), "color": (50, 220, 50), "id": "C", "grabbed": False},
    ]
    # Drop zone placed within arm's max reach (390px from base)
    drop_zone = pygame.Rect(420, 550, 120, 80)
    agent = Agent(arm_controller, packages, drop_zone)

    auto_mode = False  # Toggle with SPACE

    running = True
    while running:
        screen.fill((20, 25, 35))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    auto_mode = not auto_mode
                    print(f"[{'ON' if auto_mode else 'OFF'}] Auto Mode (Agent Loop)")
                if event.key == pygame.K_g:
                    arm_controller.grab()
                if event.key == pygame.K_r:
                    arm_controller.release()

        # Agent Loop or Manual Control
        if auto_mode:
            agent.step()
        else:
            arm_controller.update()

        # ==================== Draw Warehouse ====================
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

        # ==================== Draw Arm ====================
        j1, j2, j3 = arm_controller.get_joint_positions()
        end_x, end_y = arm_controller.get_end_effector_position()

        # Links
        pygame.draw.line(screen, (100, 200, 255), (650, 420), j1, 10)
        pygame.draw.line(screen, (255, 190, 90), j1, j2, 8)
        pygame.draw.line(screen, (120, 255, 140), j2, j3, 6)

        # Joints
        pygame.draw.circle(screen, (255, 80, 80), (int(j1[0]), int(j1[1])), 8)
        pygame.draw.circle(screen, (255, 200, 80), (int(j2[0]), int(j2[1])), 7)
        pygame.draw.circle(screen, (100, 255, 160), (int(j3[0]), int(j3[1])), 9)

        # End effector
        ee_color = (255, 50, 50) if arm_controller.has_package else (220, 220, 220)
        pygame.draw.circle(screen, ee_color, (int(end_x), int(end_y)), 10)

        # ==================== HUD ====================
        state = arm_controller.get_state()
        # Status line
        mode = "🤖 AGENT LOOP" if auto_mode else "🖱️  MANUAL"
        status = f"{mode} | State: {agent.get_state_text()} | Held: {'Yes' if state['has_package'] else 'No'} | End: ({state['end_x']:.0f}, {state['end_y']:.0f})"
        screen.blit(font.render(status, True, (220, 220, 220)), (30, 25))

        # Stats
        stats = f"Packages delivered: {agent.packages_delivered} | Cycles: {agent.cycle_count} | Remaining: {sum(1 for p in packages if not p['grabbed'])}"
        screen.blit(font.render(stats, True, (180, 180, 180)), (30, 50))

        # Controls help
        help_text = "SPACE = Toggle Auto/Manual | G = Grab | R = Release | Mouse = Drag (Manual)"
        screen.blit(font.render(help_text, True, (140, 140, 140)), (30, HEIGHT - 30))

        # Agent log
        if auto_mode and agent.action_log:
            for i, msg in enumerate(agent.action_log):
                screen.blit(font.render(msg, True, (200, 200, 200)),
                            (30, 80 + i * 22))

        # Title
        title = big_font.render("Gary Warehouse Robot — Perception-Action Loop Demo",
                                True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT - 65))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
