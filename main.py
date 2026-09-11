import pygame
import math


pygame.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

balls = []
gravity = 0.49
radius = 25 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                balls.append({"x": mouse_x, "y": mouse_y, "velocity_y": 0, "velocity_x": 0})
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                balls.clear()        

    for ball in balls:
        ball["velocity_y"] += gravity
        ball["y"] += ball["velocity_y"]
        ball["x"] += ball["velocity_x"]

        if ball["y"] + radius >= 425:
            ball["y"] = 425 - radius
            ball["velocity_y"] = ball["velocity_y"] * -0.7
            if abs(ball["velocity_y"]) < 1:
                 ball["velocity_y"] = 0



    for i in range(len(balls)):
      for j in range(i + 1, len(balls)):
         ball1 = balls[i]
         ball2 = balls[j]

         dx = ball2["x"] - ball1["x"]
         dy = ball2["y"] - ball1["y"]
         distance = math.sqrt(dx**2 + dy**2)

         if distance < radius * 2 and distance > 0:
              overlap = radius * 2 - distance
              nx = dx / distance
              ny = dy / distance

              ball1["x"] -= nx * overlap / 2
              ball1["y"] -= ny * overlap / 2
              ball2["x"] += nx * overlap / 2
              ball2["y"] += ny * overlap / 2

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0,255,0), (0, 425, WIDTH, 175))
    for ball in balls:
        pygame.draw.circle(screen, (255,255, 0), (ball["x"], int(ball["y"])), radius)
    pygame.display.flip()
    clock.tick(75)

pygame.quit()