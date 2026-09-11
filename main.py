import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ball_types = [
    {"gravity": 0.7, "bounce": -0.3, "radius": 35, "color": (100,50,50)}, #heavy ball
    {"gravity": 0.5, "bounce": -0.5, "radius": 25, "color": (50,100,50)}, #normal ball
    {"gravity": 0.3, "bounce": -0.7, "radius": 15, "color": (50,50,100)}, #light ball
]
balls = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                chosen_type = random.choice(ball_types)
                balls.append({"x": mouse_x, "y": mouse_y, "velocity_y": 0, "velocity_x": 0, "gravity": chosen_type["gravity"], "bounce": chosen_type["bounce"], "radius": chosen_type["radius"], "color": chosen_type["color"]})
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                balls.clear()        

    for ball in balls:
        ball["velocity_y"] += ball["gravity"]
        ball["y"] += ball["velocity_y"]
        ball["x"] += ball["velocity_x"]

        if ball["y"] + ball["radius"] >= 425:
            ball["y"] = 425 - ball["radius"]
            ball["velocity_y"] = ball["velocity_y"] * ball["bounce"]
            if abs(ball["velocity_y"]) < 1:
                 ball["velocity_y"] = 0

    for i in range(len(balls)):
      for j in range(i + 1, len(balls)):
         ball1 = balls[i]
         ball2 = balls[j]

         dx = ball2["x"] - ball1["x"]
         dy = ball2["y"] - ball1["y"]
         distance = math.sqrt(dx**2 + dy**2)

         if distance < ball1["radius"] + ball2["radius"] and distance > 0:
              overlap = ball1["radius"] + ball2["radius"] - distance
              nx = dx / distance
              ny = dy / distance

              ball1["x"] -= nx * overlap / 2
              ball1["y"] -= ny * overlap / 2
              ball2["x"] += nx * overlap / 2
              ball2["y"] += ny * overlap / 2

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0,255,0), (0, 425, WIDTH, 175))
    for ball in balls:
        pygame.draw.circle(screen, ball["color"], (ball["x"], int(ball["y"])), ball["radius"])
    pygame.display.flip()
    clock.tick(75)

pygame.quit()