import pygame
import sys
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PolyU MSc IRE - Embodied Robot Intelligence Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Microsoft YaHei", 22)
big_font = pygame.font.SysFont("Microsoft YaHei", 28)

class EmbodiedAgent:
    def __init__(self):
        self.x = 150
        self.y = 300
        self.velocity = [0, 0]
        self.gripper_state = "open"
        self.sensors = {"vision": "clear", "touch": "clear"}
        
    def perceive(self, obstacles, targets):
        # Vision sensor
        for obs in obstacles:
            if abs(self.x - obs.x) < 80 and abs(self.y - obs.y) < 80:
                self.sensors["vision"] = "obstacle ahead"
                break
        else:
            self.sensors["vision"] = "clear"
            
        # Touch sensor  
        for t in targets:
            if abs(self.x - t.x) < 50 and abs(self.y - t.y) < 50:
                self.sensors["touch"] = "target detected"
                break
        else:
            for obs in obstacles:
                if abs(self.x - obs.x) < 40 and abs(self.y - obs.y) < 40:
                    self.sensors["touch"] = "obstacle"
                    break
            else:
                self.sensors["touch"] = "clear"
        return self.sensors
    
    def llm_think(self, task):
        reason = ""
        if "obstacle" in self.sensors["touch"]:
            action = "move"
            self.velocity = [-100, 0]
            reason = "避開障礙物"
        elif "obstacle" in self.sensors["vision"]:
            action = "move"
            self.velocity = [0, -80]
            reason = "前方有障礙，轉向"
        elif "target" in self.sensors["touch"]:
            action = "close"
            self.gripper_state = "close"
            self.velocity = [0, 0]
            reason = "夾取目標物品"
        elif "pick" in task.lower() and "target" in self.sensors["vision"]:
            action = "approach"
            self.velocity = [80, 0]
            reason = "接近目標"
        else:
            action = "move"
            self.velocity = [100, 0]
            reason = "前進探索"
        return {"action": action, "reason": reason}
    
    def execute(self, command):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        # Boundary check
        self.x = max(30, min(WIDTH-30, self.x))
        self.y = max(80, min(HEIGHT-80, self.y))
        return command

# Game objects
agent = EmbodiedAgent()
obstacles = [pygame.Rect(400, 200, 70, 70), pygame.Rect(600, 400, 60, 60)]
targets = [pygame.Rect(700, 280, 50, 50)]
task = "pick up the green cube"

# State
running = True
last_perception = ""
last_think = ""
last_action = ""
history = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Perceive
                sensors = agent.perceive(obstacles, targets)
                last_perception = f"Vision: {sensors['vision']} | Touch: {sensors['touch']}"
                
                # Think
                cmd = agent.llm_think(task)
                last_think = f"LLM Think: {cmd['reason']}"
                
                # Act
                result = agent.execute(cmd)
                last_action = f"Action: {result['action']}"
                
                # Save history
                history.append((last_perception, last_think, last_action))
    
    # Draw
    screen.fill((25, 28, 38))
    
    # Title
    title = big_font.render("PolyU MSc IRE - Embodied Robot Intelligence Demo", True, (255, 255, 255))
    screen.blit(title, (20, 20))
    
    # Draw obstacles (red)
    for obs in obstacles:
        pygame.draw.rect(screen, (220, 60, 60), obs)
    
    # Draw targets (green)
    for t in targets:
        pygame.draw.rect(screen, (50, 220, 60), t)
    
    # Draw agent (blue circle)
    pygame.draw.circle(screen, (80, 180, 255), (int(agent.x), int(agent.y)), 30)
    
    # Gripper indicator
    gripper_color = (100, 255, 100) if agent.gripper_state == "open" else (255, 100, 100)
    pygame.draw.circle(screen, gripper_color, (int(agent.x), int(agent.y) + 40), 10)
    
    # Draw sensor rays
    pygame.draw.line(screen, (255, 255, 0), (agent.x, agent.y), (agent.x + 60, agent.y), 2)
    pygame.draw.line(screen, (255, 255, 0), (agent.x, agent.y), (agent.x, agent.y - 60), 2)
    
    # Display info
    p_text = font.render(last_perception or "Perception: Press SPACE", True, (255, 255, 100))
    t_text = font.render(last_think or "LLM Think: ...", True, (100, 200, 255))
    a_text = font.render(last_action or "Action: ...", True, (100, 255, 150))
    screen.blit(p_text, (20, 70))
    screen.blit(t_text, (20, 100))
    screen.blit(a_text, (20, 130))
    
    # Task display
    task_text = font.render(f"Task: {task}", True, (200, 200, 200))
    screen.blit(task_text, (20, HEIGHT - 40))
    
    # Instructions
    instr = font.render("按 SPACE 執行 Perception → Think → Action", True, (180, 180, 180))
    screen.blit(instr, (20, HEIGHT - 70))
    
    # Legend
    legend = font.render("🔵 Agent | 🔴 Obstacle | 🟢 Target", True, (150, 150, 150))
    screen.blit(legend, (WIDTH - 350, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()