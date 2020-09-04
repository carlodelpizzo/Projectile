import pygame
from pygame.locals import *
from math import *
import random


def truncate(number, digits):
    stepper = 10.0 * digits
    return trunc(stepper * number) / stepper


pygame.init()
# Initialize screen
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
# Title
pygame.display.set_caption("Projectile")
# Screen colors
bg_color = [0, 0, 0]
grid_color = [50, 50, 50]
fg_color = [50, 100, 200]
white = [255, 255, 255]
red = [255, 0, 0]
# Font
font_size = 25
stat_font_size = 17
font_face = "Helvetica"
font = pygame.font.SysFont(font_face, font_size)
stat_font = pygame.font.SysFont(font_face, stat_font_size)


class Launcher:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 80.0
        self.power = 15.5
        self.length = 60

    def draw(self):
        pygame.draw.circle(screen, fg_color, (0, screen_height), 7)
        end_x = int(cos(radians(self.angle)) * self.length)
        end_y = screen_height - int(sin(radians(self.angle)) * self.length)
        pygame.draw.line(screen, fg_color, (0, screen_height), (end_x, end_y), 3)

    def launch_ball(self):
        balls.append(Ball())
        x_comp = self.power * cos(radians(self.angle))
        y_comp = - self.power * sin(radians(self.angle))
        balls[len(balls) - 1].dir = (x_comp, y_comp)


class Ball:

    def __init__(self):
        self.x = 0
        self.y = screen_height
        self.dir = (0, 0)
        self.g = 0
        self.radius = 7
        self.path = []
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.apex = screen_height

    def draw(self):
        pygame.draw.circle(screen, fg_color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.path.append((int(self.x), int(self.y)))
        if self.y + self.dir[1] + self.g <= screen_height - self.radius:
            self.x += self.dir[0]
            self.y += self.dir[1] + self.g
            self.g += g_constant
        else:
            self.bounce()
        if int(self.y) < self.apex:
            self.apex = int(self.y)

    def bounce(self):
        self.dir = (self.dir[0] * 0.98, - self.dir[1] * 0.98)
        self.g = 0
        self.y = screen_height - self.radius

    def display_pos(self):
        pos = "(" + str(int(self.x)) + ", " + str(screen_height - int(self.y)) + ")"
        display_pos = stat_font.render(pos, True, white)
        screen.blit(display_pos, (int(self.x) + self.radius, int(self.y) - (self.radius * 2)))

    def display_apex(self):
        for i in range(len(self.path)):
            if self.apex == self.path[i][1]:
                apex_str = "(" + str(self.path[i][0]) + ", " + str(screen_height - self.path[i][1]) + ")"
                dis_apex = stat_font.render(apex_str, True, white)
                screen.blit(dis_apex, (self.path[i][0] + self.radius, self.path[i][1] - (self.radius * 2)))
                pygame.draw.circle(screen, self.color, (self.path[i][0], self.path[i][1]), int(self.radius / 3))
                break


def dis_dot_path(path, dot_color, radius):
    for i in range(len(path)):
        if i % 2 != 0:
            pygame.draw.circle(screen, dot_color, (path[i][0], path[i][1]), int(radius / 3))


def dis_line_path(path, line_color):
    for i in range(len(path) - 1):
        pygame.draw.line(screen, line_color, (path[i][0], path[i][1]),
                         (path[i + 1][0], path[i + 1][1]), 1)


# Create grid of unit = 10 pixels
def bg_grid():
    for i in range(0, int(screen_width / 10)):
        pygame.draw.rect(screen, grid_color, (10 * i, 0, 1, screen_height))
    for i in range(0, int(screen_height / 10)):
        pygame.draw.rect(screen, grid_color, (0, 10 * i, screen_width, 1))


# Kill off screen balls
def murder_balls(kill_mode):
    if kill_mode:
        pop_list = []
        for i in range(len(balls)):
            if balls[i].x > screen_width + balls[i].radius + 1:
                pop_list.append(i)
        for i in range(len(pop_list)):
            if pop_list[i] <= len(balls):
                balls.pop(pop_list[i])
    else:
        for dead_ball in balls:
            if dead_ball.x > screen_width + dead_ball.radius + 1:
                dead_ball.dir = (0, 0)


def display_info():
    stat_num = 0
    # Display number of balls
    # num_balls = str(len(balls))
    # dis_num_balls = font.render("Balls: " + num_balls, True, white)
    # screen.blit(dis_num_balls, (0, font_size * stat_num))
    # stat_num += 1
    # Display power
    dis_launch_power = font.render("Power: " + str(player.power), True, white)
    screen.blit(dis_launch_power, (0, font_size * stat_num))
    stat_num += 1
    # Display player angle
    dis_player_angle = font.render("Angle: " + str(player.angle), True, white)
    screen.blit(dis_player_angle, (0, font_size * stat_num))
    stat_num += 1


# Update player angle and power based on mouse pos
def mouse_click():
    mouse_pos = pygame.mouse.get_pos()
    mouse_distance = sqrt(
        mouse_pos[0] * mouse_pos[0] + (screen_height - mouse_pos[1]) * (screen_height - mouse_pos[1]))
    player.angle = truncate(degrees(acos(mouse_pos[0] / mouse_distance)), 1)
    player.power = truncate(mouse_distance * 0.03, 1)


def sim_path(x_pwr_sim, y_pwr_sim):
    sim = Ball()
    sim.dir = (x_pwr_sim, y_pwr_sim)
    t = 0
    while sim.x < screen_width and t < 10000:
        sim.move()
        t += 1
    return sim.path


# Game data
player = Launcher()
balls = []
clock = pygame.time.Clock()
frame_rate = 60
g_constant = 9.8 / frame_rate

show_info = True
trace_type = 0
aim_down = False
aim_up = False
mouse_hold = False
running = True
pause = False
while running:
    # Reset screen
    screen.fill((0, 0, 0))
    bg_grid()

    # Event Loop
    for event in pygame.event.get():
        # Close Window
        if event.type == pygame.QUIT:
            running = False
            break

        keys = pygame.key.get_pressed()
        # Key down events
        if event.type == pygame.KEYDOWN:
            # Close Window
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_w]:
                running = False
                break
            # Pause game
            if keys[K_p] and not pause:
                pause = True
            elif keys[K_p] and pause:
                pause = False
            # Advance 1 frame
            if keys[K_n] and pause:
                for ball in balls:
                    ball.move()
            # Lower Power
            if (keys[K_LSHIFT] or keys[K_RSHIFT]) and keys[K_DOWN]:
                player.power -= 0.5
            # Raise Power
            if (keys[K_LSHIFT] or keys[K_RSHIFT]) and keys[K_UP]:
                player.power += 0.5
            # Lower launcher
            if keys[K_DOWN] and not aim_down and not (keys[K_LSHIFT] or keys[K_RSHIFT]):
                aim_down = True
            if keys[K_RIGHT]:
                player.angle -= 0.5
            # Raise launcher
            if keys[K_UP] and not aim_up and not (keys[K_LSHIFT] or keys[K_RSHIFT]):
                aim_up = True
            if keys[K_LEFT]:
                player.angle += 0.5
            # Launch launcher
            if keys[K_SPACE]:
                player.launch_ball()
            # Show info
            if keys[K_s] and not show_info:
                show_info = True
            elif keys[K_s] and show_info:
                show_info = False
            # Trace on/off
            if keys[K_t] and (0 <= trace_type <= 1):
                trace_type += 1
            elif keys[K_t] and trace_type >= 2:
                trace_type = 0
            # Kill ball
            if keys[K_k] and len(balls) != 0:
                balls.pop(len(balls) - 1)

        # Key up events
        if event.type == pygame.KEYUP:
            # Lower launcher
            if not keys[K_DOWN] and aim_down:
                aim_down = False
            # Raise launcher
            if not keys[K_UP] and aim_up:
                aim_up = False

        # Mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_hold:
            mouse_click()
            mouse_hold = True
        elif event.type == pygame.MOUSEBUTTONUP and mouse_hold:
            mouse_hold = False

    # Show stats and info
    if show_info:
        display_info()
    # Player updates
    if aim_up and player.angle < 90:
        player.angle += 0.5
    elif aim_down and player.angle > 0:
        player.angle -= 0.5
    if mouse_hold:
        mouse_click()
        x_p = player.power * cos(radians(player.angle))
        y_p = - player.power * sin(radians(player.angle))
        dis_line_path(sim_path(x_p, y_p), fg_color)
    player.draw()

    # Ball updates
    for ball in balls:
        if not pause:
            ball.move()
        ball.draw()
        if show_info:
            ball.display_pos()
            ball.display_apex()
        if trace_type == 1:
            dis_line_path(ball.path, ball.color)
        elif trace_type == 2:
            dis_dot_path(ball.path, ball.color, ball.radius)
    murder_balls(True)

    clock.tick(frame_rate)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
