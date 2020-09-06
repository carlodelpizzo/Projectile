import pygame
from pygame.locals import *
from math import *
import random


def round_nearest_int(number):
    if number % 1 >= 0.5:
        number = int(number) + 1
    else:
        number = int(number)
    return number


def trunc_round(number, digits):
    if digits > 0:
        stepper = 10.0 * digits
    else:
        stepper = 1
    return round_nearest_int(stepper * number) / stepper


pygame.init()
# Initialize screen
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
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
main_font = pygame.font.SysFont(font_face, font_size)
stat_font = pygame.font.SysFont(font_face, stat_font_size)
pause_font = pygame.font.SysFont(font_face, font_size)
pause_font.set_bold(True)


class Launcher:

    def __init__(self):
        self.x = 0
        self.y = screen_height
        self.angle = 45.0
        self.power = 12
        self.x_power = (self.power * cos(radians(self.angle)))
        self.y_power = - (self.power * sin(radians(self.angle)))
        self.length = 60
        self.color = fg_color

    def draw(self):
        end_x = int(cos(radians(self.angle)) * self.length)
        end_y = int(screen_height - sin(radians(self.angle)) * self.length)
        pygame.draw.line(screen, self.color, (int(self.x), int(self.y)), (end_x, end_y), 3)

    def launch_ball(self):
        balls.append(Ball())
        balls[len(balls) - 1].dir = (self.x_power, self.y_power)

    def update(self, new_value, variable):
        if variable == 'angle' and self.angle != new_value:
            self.angle = trunc_round(new_value, 1)
            self.x_power = trunc_round(cos(radians(self.angle)) * self.power, 1)
            self.y_power = - trunc_round(sin(radians(self.angle)) * self.power, 1)
        elif variable == 'power' and self.x_power != new_value:
            self.power = new_value
            self.x_power = trunc_round(cos(radians(self.angle)) * self.power, 1)
            self.y_power = - trunc_round(sin(radians(self.angle)) * self.power, 1)


class Ball:

    def __init__(self):
        self.x = 0
        self.y = screen_height
        self.dir = (0, 0)
        self.radius = 7
        self.path = []
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.apex = False
        self.apex_y = screen_height * 2
        self.apex_x = 0
        self.t = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        # Log path
        self.path.append((self.x, self.y))
        # Log apex
        if self.dir[1] < 0 < self.dir[1] + g_constant / 2:
            if self.apex_y > self.y + self.dir[1]:
                self.apex = True
                self.apex_x = self.x + self.dir[0]
                self.apex_y = self.y + self.dir[1] + g_constant / 2
        self.bounce_y()
        self.bounce_x()
        self.x += self.dir[0]
        self.dir = (self.dir[0], self.dir[1] + g_constant / 2)
        self.y += self.dir[1]
        self.t += 1

    def bounce_y(self):
        if self.y > screen_height and self.dir[1] > 0:
            self.dir = (self.dir[0] * friction, -(self.dir[1] * friction))
        elif self.y < 0 and ceiling and self.dir[1] < 0:
            self.dir = (self.dir[0] * friction, -(self.dir[1] * friction))

    def bounce_x(self):
        if walls:
            if self.x < 0 and self.dir[0] < 0:
                self.dir = (-(self.dir[0] * friction), self.dir[1] * friction)
            elif self.x > screen_width and self.dir[0] > 0:
                self.dir = (-(self.dir[0] * friction), self.dir[1] * friction)

    def display_pos(self):
        pos = "(" + str(trunc_round(self.x / 10, 1)) + ", " + \
              str(trunc_round((screen_height - int(self.y)) / 10, 1)) + ")"
        pos = stat_font.render(pos, True, white)
        screen.blit(pos, (int(self.x + self.radius), int(self.y - (self.radius * 2))))

    def display_apex(self):
        if self.apex_y < screen_height:
            apex = "(" + str(trunc_round(self.apex_x / 10, 1)) + ", " + \
                       str(trunc_round((screen_height - self.apex_y) / 10, 1)) + ")"
            apex = stat_font.render(apex, True, white)
            screen.blit(apex, (int(self.apex_x + self.radius), int(self.apex_y - (self.radius * 2))))
            pygame.draw.circle(screen, self.color,
                               (int(self.apex_x), int(self.apex_y)), int(self.radius / 3))

    def resize(self, h):
        delta_h = h - screen_height
        for i in range(len(self.path)):
            self.path[i] = (self.path[i][0], self.path[i][1] + delta_h)
        if self.apex:
            self.apex_y += delta_h
        else:
            self.apex_y = h * 2
        self.y += delta_h


class Target:

    def __init__(self, x, y):
        # self.pos = (x, y)
        self.x = x
        self.y = y
        self.y_alt = screen_height - self.y

    def draw(self):
        self.y_alt = screen_height - self.y
        pygame.draw.line(screen, red, (self.x - 5, self.y - 5), (self.x + 5, self.y + 5), 1)
        pygame.draw.line(screen, red, (self.x - 5, self.y + 5), (self.x + 5, self.y - 5), 1)
        pygame.draw.circle(screen, bg_color, (self.x, self.y), 2)


def dis_dot_path(path, dot_color, radius):
    for i in range(len(path)):
        if i % 2 != 0:
            pygame.draw.circle(screen, dot_color, (int(path[i][0]), int(path[i][1])), radius)


def dis_line_path(path, line_color, line_type):
    if line_type == 'dash':
        width = 2
    else:
        width = 1
    for i in range(len(path) - 1):
        if i % 3 != 0 and line_type == 'dash':
            continue
        pygame.draw.line(screen, line_color, (int(path[i][0]), int(path[i][1])),
                         (int(path[i + 1][0]), int(path[i + 1][1])), width)


# Create grid of unit = 10 pixels
def bg_grid():
    for i in range(0, round_nearest_int(screen_width / 10) + 1):
        if i % 10 == 0:
            pygame.draw.rect(screen, (grid_color[0] + 20, grid_color[1] + 20, grid_color[2] + 20),
                             (10 * i, 0, 2, screen_height))
        elif i % 5 == 0:
            pygame.draw.rect(screen, grid_color, (10 * i, 0, 2, screen_height))
        else:
            pygame.draw.rect(screen, grid_color, (10 * i, 0, 1, screen_height))
    for i in range(0, round_nearest_int(screen_height / 10) + 1):
        if i % 10 == 0:
            pygame.draw.rect(screen, (grid_color[0] + 20, grid_color[1] + 20, grid_color[2] + 20),
                             (0, screen_height - 10 * i, screen_width, 2))
        elif i % 5 == 0:
            pygame.draw.rect(screen, grid_color, (0, screen_height - 10 * i, screen_width, 2))
        else:
            pygame.draw.rect(screen, grid_color, (0, screen_height - 10 * i, screen_width, 1))


# Kill off screen balls
def murder_balls():
    pop_list = []
    for i in range(len(balls)):
        if balls[i].x > screen_width + balls[i].radius * 5:
            pop_list.append(i)
        elif balls[i].dir[0] == 0:
            pop_list.append(i)
    for i in range(len(pop_list)):
        if pop_list[i] <= len(balls) - 1:
            balls.pop(pop_list[i])


def display_info():
    stat_num = 0
    # Display player power
    if mouse_hold or pause:
        # Display player angle
        dis_player_angle = main_font.render("Angle: " + str(trunc_round(player.angle, 1)), True, white)
        screen.blit(dis_player_angle, (0, font_size * stat_num))
        stat_num += 1
    # Display Ball t
    for i in range(len(balls)):
        ball_t = balls[i].t
        ball_t = main_font.render("Ball " + str((i + 1)) + " t: " + str(ball_t), True, balls[i].color)
        screen.blit(ball_t, (0, font_size * stat_num))
        stat_num += 1
    # Display Ball apex
    # for i in range(len(balls)):
    #     if balls[i].apex_y < screen_height:
    #         apex_text = trunc_round(screen_height - balls[i].apex_y, 1)
    #         apex_text = main_font.render("Ball " + str((i + 1)) + " apex: " + str(apex_text), True, balls[i].color)
    #         screen.blit(apex_text, (0, font_size * stat_num))
    #         stat_num += 1
    # Display x vector component
    x_comp = player.x_power
    x_comp = main_font.render("X Comp: " + str(x_comp), True, white)
    screen.blit(x_comp, (0, font_size * stat_num))
    stat_num += 1
    # Display y vector component
    y_comp = player.y_power
    y_comp = main_font.render("Y Comp: " + str(y_comp), True, white)
    screen.blit(y_comp, (0, font_size * stat_num))
    stat_num += 1


def mouse_click():

    def hunt_y(y_vel, target_t):
        while True:
            if y_vel < 0:
                y_vel = -y_vel
            y_pos = 0
            y_dir = 0
            target_pos = screen_height - targets[0].y
            target_range = 10
            for i in range(0, int(target_t)):
                y_dir -= g_constant / 2
                y_pos += y_vel + y_dir
            if target_pos - 30 < y_pos < target_pos + target_range:
                player.y_power = - y_vel
                break
            elif y_pos > target_pos + target_range:
                y_vel -= 0.5
            elif y_pos < target_pos - target_range:
                y_vel += 0.5

    mouse_pos1 = pygame.mouse.get_pos()
    mouse_distance = sqrt(
        mouse_pos1[0] * mouse_pos1[0] + (screen_height - mouse_pos1[1]) * (screen_height - mouse_pos1[1]))
    if mouse_left:
        player.update(trunc_round((screen_height - mouse_pos1[1]) * 0.1, 1), 'power')
        player.update(trunc_round(degrees(acos(mouse_pos1[0] / mouse_distance)), 1), 'angle')
    elif mouse_right:
        if not target_lock:
            if len(targets) >= 1:
                targets.pop(0)
        elif target_lock:
            if len(targets) == 0:
                targets.append(Target(mouse_pos1[0], mouse_pos1[1]))
            targets[0].x = mouse_pos1[0]
            targets[0].y = mouse_pos1[1]
            player.angle = trunc_round(degrees(acos(mouse_pos1[0] / mouse_distance)), 1)
            t = targets[0].x / player.x_power
            hunt_y(player.y_power, t)


def sim_ball(x_pwr_sim, y_pwr_sim):
    sim = Ball()
    sim.dir = (x_pwr_sim, y_pwr_sim)
    t = 0
    while t < 1420:
        sim.move()
        t += 1
    return sim


# Game data
player = Launcher()
balls = []
targets = []
clock = pygame.time.Clock()
frame_rate = 60
g_constant = 98 / frame_rate
friction = 0.98

walls = False
ceiling = False
show_info = True
trace_type = 1  # 0 off, 1 solid path, 2 dot path
target_lock = False
mouse_left = False
mouse_right = False
mouse_hold = False
running = True
pause = False
fast = False
kill_mode = False
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
            if keys[K_SPACE] and not pause:
                pause = True
            elif keys[K_SPACE] and pause:
                pause = False
            # Advance 1 frame
            if keys[K_n] and pause:
                for ball in balls:
                    ball.move()
            # Lower launcher angle
            if keys[K_RIGHT]:
                player.update(player.angle - 0.1, 'angle')
            # Raise launcher angle
            elif keys[K_LEFT]:
                player.update(player.angle + 0.1, 'angle')
            # Lower launcher power
            if keys[K_DOWN]:
                player.update(player.x_power - 0.1, 'power')
            # Raise launcher power
            elif keys[K_UP]:
                player.update(player.x_power + 0.1, 'power')
            # Launch launcher
            if keys[K_l]:
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
            # Speed up
            if keys[K_f] and not fast:
                fast = True
            elif keys[K_f] and fast:
                fast = False

        # Key up events
        if event.type == pygame.KEYUP:
            pass

        # Mouse button events
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_hold:
            mouse_hold = True
            if event.button == 1:
                mouse_left = True
            elif event.button == 3 and not target_lock:
                mouse_right = True
                target_lock = True
            elif event.button == 3 and target_lock:
                mouse_right = True
                if targets[0].x - 10 < mouse_pos[0] < targets[0].x + 10:
                    if targets[0].y - 10 < mouse_pos[1] < targets[0].y + 10:
                        target_lock = False
            mouse_click()
        elif event.type == pygame.MOUSEBUTTONUP and mouse_hold:
            mouse_hold = False
            mouse_left = False
            mouse_right = False

        # Window resize
        if event.type == pygame.VIDEORESIZE:
            for ball in balls:
                ball.resize(event.h)
            for target in targets:
                target.y += event.h - screen_height
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
            player.y = screen_height

    trajectory = sim_ball(player.x_power, player.y_power)
    trajectory.color = fg_color
    # Show stats and info
    if show_info:
        display_info()
    if pause:
        # Show pause symbol
        pause_symbol = pause_font.render("| |", True, white)
        screen.blit(pause_symbol, (screen_width - 25, 0))
        # Show player trajectory
        dis_line_path(trajectory.path, fg_color, 'dash')
        trajectory.display_apex()
    # Player updates
    if mouse_hold:
        mouse_click()
        if not pause:
            dis_line_path(trajectory.path, fg_color, 'dash')
            if show_info:
                trajectory.display_apex()
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
            dis_line_path(ball.path, ball.color, 'solid')
        elif trace_type == 2:
            dis_dot_path(ball.path, ball.color, 2)
    if kill_mode:
        murder_balls()

    # Targets
    for target in targets:
        target.draw()

    if not fast:
        clock.tick(frame_rate)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
