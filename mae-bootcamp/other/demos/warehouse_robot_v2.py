"""
Warehouse Robot v2 — Agent Loop + Sensor Fusion Demo
Shows Perception → Sensor Fusion → Decision → Action in real-time
"""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import math
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warehouse Robot v2 — Sensor Fusion + Agent Loop")
clock = pygame.time.Clock()


def draw_frame(arm, arm_controller, agent, packages, drop_zone, frame_count):
    screen.fill((20, 25, 35))
    font = pygame.font.SysFont("Consolas", 16)
    title_font = pygame.font.SysFont("Consolas", 22)

    # Shelves
    pygame.draw.rect(screen, (80, 80, 90), (380, 200, 400, 20))
    pygame.draw.rect(screen, (80, 80, 90), (380, 300, 400, 20))

    # Drop Zone
    pygame.draw.rect(screen, (100, 200, 255), drop_zone, 4)
    screen.blit(font.render("DROP ZONE", True, (100, 200, 255)),
                (drop_zone.x + 10, drop_zone.y - 25))

    # Packages
    for pkg in packages:
        if not pkg['grabbed']:
            pygame.draw.rect(screen, pkg['color'],
                             (pkg['pos'][0], pkg['pos'][1], 45, 45))
            screen.blit(font.render(pkg['id'], True, (0, 0, 0)),
                        (pkg['pos'][0] + 15, pkg['pos'][1] + 12))

    # Arm (color may change based on force threshold)
    j1, j2, j3 = arm_controller.get_joint_positions()
    end_x, end_y = arm_controller.get_end_effector_position()
    # Determine arm color based on grip force (visual warning)
    arm_color_1 = (100, 200, 255)  # base
    arm_color_2 = (255, 190, 90)
    arm_color_3 = (120, 255, 140)
    if arm_controller.has_package and agent.sensor_log:
        latest_force = agent.sensor_log[-1]["force"]
        # Thresholds: 1.8N warning, 2.5N danger
        if latest_force > 2.5:
            arm_color_1 = (255, 60, 60)  # Red - danger
            arm_color_2 = (255, 60, 60)
            arm_color_3 = (255, 60, 60)
        elif latest_force > 1.8:
            arm_color_1 = (255, 200, 80)  # Yellow - warning
            arm_color_2 = (255, 200, 80)
            arm_color_3 = (255, 200, 80)
    pygame.draw.line(screen, arm_color_1, (650, 420), j1, 10)
    pygame.draw.line(screen, arm_color_2, j1, j2, 8)
    pygame.draw.line(screen, arm_color_3, j2, j3, 6)
    pygame.draw.circle(screen, (255, 80, 80), (int(j1[0]), int(j1[1])), 8)
    pygame.draw.circle(screen, (255, 200, 80), (int(j2[0]), int(j2[1])), 7)
    pygame.draw.circle(screen, (100, 255, 160), (int(j3[0]), int(j3[1])), 9)
    ee_color = (255, 50, 50) if arm_controller.has_package else (220, 220, 220)
    pygame.draw.circle(screen, ee_color, (int(end_x), int(end_y)), 10)

    # Grab success green flash (1 second highlight)
    if hasattr(arm_controller, 'last_grab_frame'):
        frames_since_grab = arm_controller.frame_count - arm_controller.last_grab_frame
        if 0 <= frames_since_grab < 30:  # 30 frames = 0.5s
            flash_alpha = 200 - frames_since_grab * 6
            # Draw green circle around end effector
            flash_radius = 25 + frames_since_grab // 2
            flash_surf = pygame.Surface((flash_radius * 2, flash_radius * 2),
                                        pygame.SRCALPHA)
            pygame.draw.circle(flash_surf, (100, 255, 100, max(0, flash_alpha)),
                              (flash_radius, flash_radius), flash_radius, 4)
            screen.blit(flash_surf, (int(end_x) - flash_radius, int(end_y) - flash_radius))
            # "✓ GRABBED!" text
            if frames_since_grab < 15:
                success_font = pygame.font.SysFont("Consolas", 20, bold=True)
                success_text = success_font.render("✓ GRABBED!",
                                                  True, (100, 255, 100))
                text_bg = pygame.Surface(
                    (success_text.get_width() + 12, success_text.get_height() + 6)
                )
                text_bg.fill((20, 25, 35))
                text_bg.set_alpha(220)
                screen.blit(text_bg, (int(end_x) - 50, int(end_y) - 50))
                screen.blit(success_text, (int(end_x) - 45, int(end_y) - 47))

    # Proximity-based approach arrow (when not holding, points to nearest package)
    if not arm_controller.has_package:
        nearest_pkg = None
        nearest_dist = float('inf')
        for pkg in packages:
            if not pkg.get('grabbed', False):
                px, py = pkg['pos'][0] + 22, pkg['pos'][1] + 22
                d = math.hypot(end_x - px, end_y - py)
                if d < nearest_dist:
                    nearest_dist = d
                    nearest_pkg = pkg
        if nearest_pkg and nearest_dist < 120:
            # Draw arrow pointing toward nearest package
            px, py = nearest_pkg['pos'][0] + 22, nearest_pkg['pos'][1] + 22
            dx = px - end_x
            dy = py - end_y
            # Normalize
            d = math.hypot(dx, dy) + 1e-6
            ux, uy = dx / d, dy / d
            # Color by proximity: red (close), orange (medium)
            if nearest_dist < 35:
                prox_color = (255, 100, 100)  # Red - in grab range
                prox_status = "READY"
            elif nearest_dist < 70:
                prox_color = (255, 200, 100)  # Orange - close
                prox_status = "NEAR"
            else:
                prox_color = (180, 180, 255)  # Light blue - far
                prox_status = "FAR"
            # Arrow length
            arrow_len = max(25, min(80, 80 - nearest_dist / 2))
            arrow_end_x = int(end_x + ux * arrow_len)
            arrow_end_y = int(end_y + uy * arrow_len)
            # Draw dashed line (proximity, not physical force)
            dash_length = 8
            for i in range(0, int(arrow_len), dash_length * 2):
                start = (int(end_x + ux * i), int(end_y + uy * i))
                end = (int(end_x + ux * (i + dash_length)),
                       int(end_y + uy * (i + dash_length)))
                pygame.draw.line(screen, prox_color, start, end, 3)
            # Arrow head
            import math as m
            angle = m.atan2(uy, ux)
            head_len = 10
            pygame.draw.polygon(screen, prox_color, [
                (arrow_end_x, arrow_end_y),
                (int(arrow_end_x - head_len * m.cos(angle - 0.4)),
                 int(arrow_end_y - head_len * m.sin(angle - 0.4))),
                (int(arrow_end_x - head_len * m.cos(angle + 0.4)),
                 int(arrow_end_y - head_len * m.sin(angle + 0.4))),
            ])
            # Label
            force_font = pygame.font.SysFont("Consolas", 13, bold=True)
            force_text = force_font.render(
                f"→{nearest_pkg['id']} d={nearest_dist:.0f} {prox_status}",
                True, prox_color
            )
            text_bg = pygame.Surface(
                (force_text.get_width() + 6, force_text.get_height() + 2)
            )
            text_bg.fill((20, 25, 35))
            text_bg.set_alpha(220)
            label_x = int(end_x + ux * (arrow_len + 12))
            label_y = int(end_y + uy * (arrow_len + 12)) - 8
            screen.blit(text_bg, (label_x, label_y))
            screen.blit(force_text, (label_x + 3, label_y + 1))

    # Force feedback arrow (only show when holding package)
    if arm_controller.has_package and agent.sensor_log:
        latest = agent.sensor_log[-1]
        force = latest["force"]
        # Color code: green (firm grip), yellow (loose), red (slipping)
        if force > 1.2:
            arrow_color = (100, 255, 100)  # Green - firm
            grip_status = "FIRM"
        elif force > 0.7:
            arrow_color = (255, 220, 80)  # Yellow - loose
            grip_status = "LOOSE"
        else:
            arrow_color = (255, 80, 80)  # Red - slipping
            grip_status = "SLIP!"
        # Arrow length proportional to force
        arrow_len = max(20, min(80, force * 40))
        # Draw arrow pointing down (gripper direction)
        arrow_end_x = int(end_x)
        arrow_end_y = int(end_y + arrow_len)
        pygame.draw.line(
            screen, arrow_color,
            (int(end_x), int(end_y) + 12),
            (arrow_end_x, arrow_end_y),
            4,
        )
        # Arrow head
        pygame.draw.polygon(screen, arrow_color, [
            (arrow_end_x, arrow_end_y + 8),
            (arrow_end_x - 6, arrow_end_y - 2),
            (arrow_end_x + 6, arrow_end_y - 2),
        ])
        # Force label
        force_font = pygame.font.SysFont("Consolas", 14, bold=True)
        force_text = force_font.render(f"F={force:.2f}N {grip_status}", True, arrow_color)
        # Background for legibility
        text_bg = pygame.Surface((force_text.get_width() + 6, force_text.get_height() + 2))
        text_bg.fill((20, 25, 35))
        text_bg.set_alpha(220)
        screen.blit(text_bg, (int(end_x) + 12, int(end_y) + arrow_len - 18))
        screen.blit(force_text, (int(end_x) + 15, int(end_y) + arrow_len - 17))

    # Grip stability indicator (top-right corner)
    if arm_controller.has_package and agent.sensor_log:
        latest = agent.sensor_log[-1]
        force = latest["force"]
        # Background bar
        bar_x, bar_y = 30, HEIGHT - 130
        bar_w, bar_h = 250, 20
        pygame.draw.rect(screen, (40, 50, 60), (bar_x, bar_y, bar_w, bar_h), 1)
        # Fill based on force
        fill_pct = min(1.0, force / 2.0)
        fill_w = int(bar_w * fill_pct)
        if force > 1.2:
            bar_color = (100, 255, 100)
        elif force > 0.7:
            bar_color = (255, 220, 80)
        else:
            bar_color = (255, 80, 80)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h))
        # Label
        bar_font = pygame.font.SysFont("Consolas", 13)
        bar_label = bar_font.render(
            f"Grip Force: {force:.2f}N (target 1.0-1.8N)",
            True, (220, 220, 220)
        )
        screen.blit(bar_label, (bar_x, bar_y - 18))

    # HUD - Status
    state = arm_controller.get_state()
    status = (f"State: {agent.state} | Held: {'Yes' if state['has_package'] else 'No'} | "
              f"End: ({state['end_x']:.0f}, {state['end_y']:.0f}) | Frame: {frame_count}")
    screen.blit(font.render(status, True, (220, 220, 220)), (30, 25))

    stats = (f"Delivered: {agent.packages_delivered} | Cycles: {agent.cycle_count} | "
             f"Remaining: {sum(1 for p in packages if not p['grabbed'])}")
    screen.blit(font.render(stats, True, (180, 180, 180)), (30, 50))

    # Sensor Panel (RIGHT side)
    panel_x = 820
    panel_y = 100
    pygame.draw.rect(screen, (40, 50, 60), (panel_x - 10, panel_y - 30, 350, 580), 2)
    screen.blit(title_font.render("🔬 Sensor Fusion Panel", True, (255, 220, 100)),
                (panel_x, panel_y - 30))

    if agent.sensor_log:
        latest = agent.sensor_log[-1]
        y = panel_y + 10
        screen.blit(font.render("═══ RAW SENSORS ═══", True, (255, 180, 100)), (panel_x, y))
        y += 25

        enc = latest["encoders"]
        screen.blit(font.render(f"Encoder θ1:  {enc[0]:+7.3f} rad", True, (200, 200, 200)), (panel_x, y))
        y += 20
        screen.blit(font.render(f"Encoder θ2:  {enc[1]:+7.3f} rad", True, (200, 200, 200)), (panel_x, y))
        y += 20
        screen.blit(font.render(f"Encoder θ3:  {enc[2]:+7.3f} rad", True, (200, 200, 200)), (panel_x, y))
        y += 25

        gyro = latest["gyro"]
        screen.blit(font.render(f"Gyro ω1:    {gyro[0]:+7.2f} rad/s (drifts)", True, (255, 150, 150)), (panel_x, y))
        y += 20
        screen.blit(font.render(f"Gyro ω2:    {gyro[1]:+7.2f} rad/s", True, (255, 150, 150)), (panel_x, y))
        y += 25

        accel = latest["accel"]
        screen.blit(font.render(f"Accel x:    {accel[0]:+7.1f} m/s² (noisy)", True, (150, 255, 150)), (panel_x, y))
        y += 20
        screen.blit(font.render(f"Accel y:    {accel[1]:+7.1f} m/s²", True, (150, 255, 150)), (panel_x, y))
        y += 25

        force = latest["force"]
        force_color = (255, 100, 100) if force > 0.5 else (150, 150, 150)
        screen.blit(font.render(f"Force:      {force:+.3f} N", True, force_color), (panel_x, y))
        y += 30

        screen.blit(font.render("═══ FUSION OUTPUT ═══", True, (100, 220, 255)), (panel_x, y))
        y += 25
        sensors = agent.sensors
        screen.blit(font.render(f"Fused angle: {sensors.fused_angle:+7.3f} rad", True, (100, 220, 255)), (panel_x, y))
        y += 20
        screen.blit(font.render(f"Filter: α=0.98 gyro + 0.02 accel", True, (180, 180, 180)), (panel_x, y))
        y += 30

        if agent.fusion_log:
            screen.blit(font.render("═══ DECISION LOG ═══", True, (255, 220, 100)), (panel_x, y))
            y += 25
            for entry in agent.fusion_log[-6:]:
                line = f"[{entry['phase']}] F={entry['force']:.2f}"
                screen.blit(font.render(line, True, (200, 200, 200)), (panel_x, y))
                y += 20

    # Action log (LEFT side)
    if agent.action_log:
        log_y = 90
        screen.blit(font.render("═══ ACTIONS ═══", True, (180, 255, 180)), (30, log_y))
        log_y += 22
        for msg in agent.action_log[-6:]:
            screen.blit(font.render(msg, True, (220, 220, 220)), (30, log_y))
            log_y += 20

    # Title
    title = title_font.render(
        "Warehouse Robot v2 — Sensor Fusion + Agent Loop",
        True, (255, 255, 255),
    )
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT - 50))

    help_text = "Real-time sensor reading + complementary filter fusion"
    screen.blit(font.render(help_text, True, (140, 140, 140)),
                (WIDTH // 2 - help_text.__len__() * 4, HEIGHT - 25))

    return screen


def main():
    from arm_controller import ArmController
    from warehouse_robot import Arm
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

    frame_count = 0
    running = True
    while running and frame_count < 5000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        agent.step()
        frame = draw_frame(arm, arm_controller, agent, packages, drop_zone, frame_count)
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    print(f"\n=== Final Stats ===")
    print(f"Frames: {frame_count}")
    print(f"Packages delivered: {agent.packages_delivered}")
    print(f"Cycles: {agent.cycle_count}")
    print(f"Sensor readings: {len(agent.sensor_log)}")
    print(f"Fusion log entries: {len(agent.fusion_log)}")
    return agent, arm_controller, packages, drop_zone, arm


if __name__ == "__main__":
    main()
