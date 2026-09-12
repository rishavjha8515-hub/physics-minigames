import pygame
import math
import random
import start

pygame.init()

WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 26)
messages = []
MESSAGE_LIFETIME = 2600

def show_message(text):
    """Replacement for print() - queues text to be drawn on the screen."""
    messages.append({"text": text, "until": pygame.time.get_ticks() + MESSAGE_LIFETIME})

ball_types = [
    {"gravity": 0.7, "bounce": -0.3, "radius": 35, "color": (100,50,50)}, #heavy ball
    {"gravity": 0.5, "bounce": -0.5, "radius": 25, "color": (50,100,50)}, #normal ball
    {"gravity": 0.3, "bounce": -0.7, "radius": 15, "color": (50,50,100)}, #light ball
]

#Please read this and get offended if you are a RCB fan or enjoy the scorecard if you are just a cricket fan.
wickets = [
    {"runs":1, "batsman": "Virat Kohli", "over": 0.3},
    {"runs":2, "batsman": "Mandeep Singh", "over": 1.2},
    {"runs":12, "batsman": "AB de Villiers", "over": 2.3},
    {"runs":24, "batsman": "Kedar Jadhav", "over": 4.1},
    {"runs":40, "batsman": "Chris Gayle", "over": 6.2},
    {"runs":40, "batsman": "Straut Binny", "over": 6.5},
    {"runs":42, "batsman": "Pawan Negi", "over": 7.3},
    {"runs":44, "batsman": "Samuel Badree", "over": 8.3},
    {"runs": 48, "batsman": "Tymal Mills", "over": 9.1},
    {"runs": 49, "batsman": "Yuzendra Chahal", "over": 9.4},
]

#Here are some suprises for you if you are an Rcb fan or Barcelona fan,please accept this gift from an srh/real madrid fan like me.Please laugh
milestones = [
    {"score": 28, "message": "Reminds me of 2-8 of Barcelona vs FC Bayern Munich in 2020 UCL quarterfinals"},
    {"score": 49, "message": "NOT AGAIN! we remember 49/10 vs kkr in 2017 IPL"},
    {"score": 70, "message": "IT HAS BEEN 13 YEARS SINCE 0-7 OF BARCA VS BAYERN"},
    {"score": 287, "message": "It hurts to get bashed at home by a rival"},
]

balls = []
score = 0
current_guess = None
last_gravity = None
next_type = random.choice(ball_types)
announced_milestones = []

time_limit = 49 #rcb's fav score to make this game more fun :).please be offended,i love to offend rcb fans(i am srh fan btw)
start_ticks = pygame.time.get_ticks() #time in milliseconds since the fun will start
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                balls.clear() 
                score = 0
                announced_milestones = []
            if event.key == pygame.K_t:
                current_guess = "faster"  
            if event.key == pygame.K_d:
                current_guess = "slower"

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if current_guess is not None and last_gravity is not None:
                 actually_gravity = next_type["gravity"] > last_gravity
                 guessed_faster = current_guess == "faster"
                 if guessed_faster == actually_gravity:
                     score += 10
                     show_message(f"Someone is getting smarter! Score: {score}")
                 else:
                     show_message(f"I didn't expect that! Score: {score}")   
            else:
                show_message(f"Did you press anything? Score: {score}") 

            balls.append({"x": mouse_x, "y": mouse_y, "velocity_y": 0, "velocity_x": 0, "gravity": next_type["gravity"], "bounce": next_type["bounce"], "radius": next_type["radius"], "color": next_type["color"]})

 ##Fun thing: if you throw 3-4 ball continously in the same direction,they will collide and start juggling on thier own.I will suggest you to try this.It was satisfying to watch
            last_gravity =  next_type["gravity"]
            next_type = random.choice(ball_types)
            current_guess = None

    for m in milestones:
        if score >= m["score"] and m["message"] not in announced_milestones:
            show_message(f"MILESTONE: {m['message']}")
            announced_milestones.append(m["message"])

    elasped_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = time_limit - elasped_seconds
    if time_left <= 0:
        running = False

             
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
    now = pygame.time.get_ticks()
    messages = [m for m in messages if m["until"] > now]
    for i, m in enumerate(messages[-6:]):
        text_surface = font.render(m["text"], True, (169,225,196))
        screen.blit(text_surface, (10, 10 + i * 26))

    score_surface = font.render(f"Score: {score}  Time left: {max(0, int(time_left))}", True, (255,255,0))
    screen.blit(score_surface, (10, HEIGHT - 20))
    pygame.display.flip()
    clock.tick(75)

pygame.quit()