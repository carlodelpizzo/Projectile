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
main_font = pygame.font.SysFont(font_face, font_size)
stat_font = pygame.font.SysFont(font_face, stat_font_size)
pause_font = pygame.font.SysFont(font_face, font_size)
pause_font.set_bold(True)


class Launcher:

    def __init__(self):
        self.x = 0
        self.y = screen_height
        self.angle = 80.0
        self.power = 15.5
        self.length = 60
        self.color = fg_color

    def draw(self):
        end_x = int(cos(radians(self.angle)) * self.length)
        end_y = screen_height - int(sin(radians(self.angle)) * self.length)
        pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 3)

    def launch_ball(self):
        x_comp = self.power * cos(radians(self.angle))
        y_comp = - self.power * sin(radians(self.angle))
        balls.append(Ball())
        balls[len(balls) - 1].dir = (x_comp, y_comp)


class Ball:

    def __init__(self):
        self.x = 0
        self.y = screen_height
        self.dir = (0, 0)
        self.radius = 7
        self.path = []
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.apex = screen_height

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        # Log path
        self.path.append((self.x, self.y))
        # Log apex
        if self.dir[1] < 0 and self.dir[1] + g_constant > 0:
            if self.apex > self.y + self.dir[1]:
                self.apex = self.y + self.dir[1]
        # If within screen top/bottom
        if screen_height >= self.y >= 0:
            self.x += self.dir[0]
            self.y += self.dir[1]
            self.dir = (self.dir[0], self.dir[1] + g_constant)
        # If outside screen top/bottom
        elif self.y > screen_height or self.y < 0:
            self.bounce_y()
        if bounce_x:
            if screen_width < self.x + self.dir[0] or self.x + self.dir[0] < 0:
                self.bounce_x()

    def bounce_y(self):
        if self.y > screen_height:
            self.dir = (self.dir[0] * friction, - abs(self.dir[1] * friction))
        else:
            self.dir = (self.dir[0] * friction, abs(self.dir[1] * friction))
        self.x += self.dir[0]
        self.y += self.dir[1]
        self.dir = (trunc_round(self.dir[0], 5), trunc_round(self.dir[1] + (g_constant * 2), 5))

    def bounce_x(self):
        self.dir = (- (self.dir[0] * friction), self.dir[1] * friction)

    def display_pos(self):
        pos = "(" + str(int(self.x)) + ", " + str(screen_height - int(self.y)) + ")"
        display_pos = stat_font.render(pos, True, white)
        screen.blit(display_pos, (int(self.x) + self.radius, int(self.y) - (self.radius * 2)))

    def display_apex(self):
        for i in range(len(self.path)):
            if self.apex == self.path[i][1]:
                apex_str = "(" + str(int(self.path[i][0])) + ", " + str(int(screen_height - self.path[i][1])) + ")"
                dis_apex = stat_font.render(apex_str, True, white)
                screen.blit(dis_apex, (int(self.path[i][0] + self.radius), int(self.path[i][1] - (self.radius * 2))))
                pygame.draw.circle(screen, self.color,
                                   (int(self.path[i][0]), int(self.path[i][1])), int(self.radius / 3))
                break


class Target:

    def __init__(self, x, y):
        self.pos = (x, y)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.y_alt = screen_height - self.y

    def draw(self):
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.y_alt = screen_height - self.y
        pygame.draw.line(screen, red, (self.x - 5, self.y - 5), (self.x + 5, self.y + 5), 1)
        pygame.draw.line(screen, red, (self.x - 5, self.y + 5), (self.x + 5, self.y - 5), 1)
        pygame.draw.circle(screen, bg_color, self.pos, 2)


def dis_dot_path(path, dot_color, radius):
    for i in range(len(path)):
        if i % 2 != 0:
            pygame.draw.circle(screen, dot_color, (int(path[i][0]), int(path[i][1])), radius)


def dis_line_path(path, line_color):
    for i in range(len(path) - 1):
        pygame.draw.line(screen, line_color, (int(path[i][0]), int(path[i][1])),
                         (int(path[i + 1][0]), int(path[i + 1][1])), 1)


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
            if pop_list[i] <= len(balls) - 1:
                balls.pop(pop_list[i])
    else:
        for dead_ball in balls:
            if dead_ball.x > screen_width + dead_ball.radius + 1:
                dead_ball.dir = (0, 0)


def display_info():
    stat_num = 0
    # Display player power
    dis_launch_power = main_font.render("Power: " + str(trunc_round(player.power, 1)), True, white)
    screen.blit(dis_launch_power, (0, font_size * stat_num))
    stat_num += 1
    # Display player angle
    dis_player_angle = main_font.render("Angle: " + str(trunc_round(player.angle, 1)), True, white)
    screen.blit(dis_player_angle, (0, font_size * stat_num))
    stat_num += 1
    # Display x vector component
    x_comp = trunc_round(player.power * cos(radians(player.angle)), 1)
    dis_x_comp = main_font.render("X Comp: " + str(x_comp), True, white)
    screen.blit(dis_x_comp, (0, font_size * stat_num))
    stat_num += 1
    # Display y vector component
    y_comp = trunc_round(player.power * sin(radians(player.angle)), 1)
    dis_y_comp = main_font.render("Y Comp: " + str(y_comp), True, white)
    screen.blit(dis_y_comp, (0, font_size * stat_num))
    stat_num += 1


# Update player angle and power based on mouse pos
def mouse_click():
    mouse_pos = pygame.mouse.get_pos()
    mouse_distance = sqrt(
        mouse_pos[0] * mouse_pos[0] + (screen_height - mouse_pos[1]) * (screen_height - mouse_pos[1]))
    if mouse_left:
        player.angle = trunc_round(degrees(acos(mouse_pos[0] / mouse_distance)), 1)
        player.power = trunc_round(mouse_distance * 0.03, 1)
    if mouse_right:
        if not target_lock:
            if len(targets) >= 1:
                targets.pop(0)
        elif target_lock:
            if len(targets) == 0:
                targets.append(Target(mouse_pos[0], mouse_pos[1]))
            targets[0].pos = mouse_pos


def sim_path(x_pwr_sim, y_pwr_sim):
    sim = Ball()
    sim.color = fg_color
    sim.dir = (x_pwr_sim, y_pwr_sim)
    t = 0
    while sim.x < screen_width and t < 1000:
        sim.move()
        t += 1
    sim.display_apex()
    return sim.path


# Game data
player = Launcher()
balls = []
targets = []
clock = pygame.time.Clock()
frame_rate = 60
g_constant = 9.8 / frame_rate
friction = 0.98

show_info = True
trace_type = 1
aim_down = False
aim_up = False
target_lock = False
mouse_left = False
mouse_right = False
mouse_hold = False
running = True
pause = False
bounce_x = False
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
            # Lower Power
            if (keys[K_LSHIFT] or keys[K_RSHIFT]) and keys[K_DOWN]:
                player.power -= 0.1
            # Raise Power
            if (keys[K_LSHIFT] or keys[K_RSHIFT]) and keys[K_UP]:
                player.power += 0.1
            # Lower launcher
            if keys[K_DOWN] and not aim_down and not (keys[K_LSHIFT] or keys[K_RSHIFT]):
                aim_down = True
            if keys[K_RIGHT]:
                player.angle -= 0.1
            # Raise launcher
            if keys[K_UP] and not aim_up and not (keys[K_LSHIFT] or keys[K_RSHIFT]):
                aim_up = True
            if keys[K_LEFT]:
                # player.angle = truncate(player.angle + 0.1, 1)
                player.angle += 0.1
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

        # Key up events
        if event.type == pygame.KEYUP:
            # Lower launcher
            if not keys[K_DOWN] and aim_down:
                aim_down = False
            # Raise launcher
            if not keys[K_UP] and aim_up:
                aim_up = False

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

    # Show stats and info
    if show_info:
        display_info()
    if pause:
        # Show pause symbol
        pause_symbol = pause_font.render("| |", True, white)
        screen.blit(pause_symbol, (screen_width - 25, 0))
        # Show player trajectory
        x_p = player.power * cos(radians(player.angle))
        y_p = - player.power * sin(radians(player.angle))
        dis_line_path(sim_path(x_p, y_p), fg_color)
    # Player updates
    if aim_up and player.angle < 90:
        player.angle += 0.5
    elif aim_down and player.angle > 0:
        player.angle -= 0.5
    if mouse_hold:
        mouse_click()
        if not pause:
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
            dis_dot_path(ball.path, ball.color, 2)
    murder_balls(True)

    # Targets
    for target in targets:
        target.draw()

    clock.tick(frame_rate)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
