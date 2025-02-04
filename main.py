import pygame
import random
import time
import math
import sqlite3

pygame.init()

WIDTH, HEIGHT = 800, 600
FONT_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = ['Red', 'Green', 'Blue', 'White',
          'Black', 'Yellow', 'Gray']
FPS = 60
NUM_STARS = 100
EXPLOSION_TIME = 2

star_image = pygame.image.load("STAR.png")
star_rect = star_image.get_rect()


font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)


def display_text(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2,
                               y - text_surface.get_height() // 2))


def generate_numbers(length):
    return [str(random.randint(0, 9)) for _ in range(length)]


def generate_colors(length):
    return [random.choice(COLORS) for _ in range(length)]


def run_game():
    player_name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill(WHITE)
        display_text("Введите ник:", 48, BLACK, WIDTH // 2, HEIGHT // 2 - 50)
        display_text(player_name, 48, BLACK, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

    level = 1
    while level <= 10:
        length = level + 4
        sequence = generate_numbers(length)
        prompt_text = "Запомните: "
        screen.fill(WHITE)
        display_text(prompt_text,
                     font_size=74,
                     color=BLACK,
                     x = WIDTH // 2,
                     y = HEIGHT // 2 - 50)
        display_text(" ".join(sequence),
                     font_size=74,
                     color=BLACK,
                     x=WIDTH // 2,
                     y=HEIGHT // 2 + 50)

        pygame.display.flip()
        time.sleep(7)
        screen.fill(WHITE)
        user_input = ""
        input_active = True

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

            screen.fill(WHITE)
            display_text("Введите последовательность:",
                         small_font.get_height(),
                         BLACK,
                         WIDTH // 2,
                         HEIGHT // 2 - 50)

            display_text(user_input,
                         small_font.get_height(),
                         BLACK,
                         WIDTH // 2,
                         HEIGHT // 2 + 50)

            pygame.display.flip()

        if user_input != "".join(sequence):
            break

        level += 1
        draw_effect()

    if level == 11:
        end_run(player_name, level)

        con = sqlite3.connect("database_game")
        cur = con.cursor()
        cur.execute("""INSERT INTO WINNER(NICK, LEVEL_NUMBER) 
                            VALUES(?, ?)""",
                    (player_name, level - 1))
        con.commit()
        con.close()

    elif level < 11:
        end_run(player_name, level)


def add_MEMBER(player_name, level):
    con = sqlite3.connect("database_game")
    cur = con.cursor()
    cur.execute("""INSERT INTO MEMBERS(NICK, LEVEL_NUMBER) 
                                VALUES(?, ?)""",
                (player_name, level - 1))
    con.commit()
    con.close()


def end_run(player_name, level):
    screen.fill(WHITE)
    display_text("Игра окончена!",
                 small_font.get_height(),
                 BLACK,
                 WIDTH // 2,
                 HEIGHT // 2 - 50)

    display_text(f"Спасибо за участие!",
                 small_font.get_height(),
                 BLACK,
                 WIDTH // 2,
                 HEIGHT // 2)

    display_text("Нажмите ESC для выхода",
                 small_font.get_height(),
                 BLACK,
                 WIDTH // 2,
                 HEIGHT // 2 + 50)

    add_MEMBER(player_name, level)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                show_menu()
                return

        pygame.display.flip()


class Star:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(200, 400)
        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.lifetime = EXPLOSION_TIME

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.lifetime -= dt

    def draw(self, surface):
        if self.lifetime > 0:
            surface.blit(star_image, (self.x, self.y))


def draw_effect():
    star_rect.x = WIDTH // 2
    star_rect.y = HEIGHT // 2
    start_time = time.time()
    clock = pygame.time.Clock()
    stars = [Star() for _ in range(NUM_STARS)]
    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))
        screen.fill((0, 0, 0))

        for star in stars:
            star.update(dt)
            star.draw(screen)
        stars = [star for star in stars if star.lifetime > 0]
        pygame.display.flip()

        if time.time() - start_time > 2:
            break


def show_splash_screen():
    screen.fill(BLACK)
    title_text = font.render("Тренажер памяти", True, WHITE)
    instruction_text = font.render("Запомни последовательность", True, WHITE)
    screen.blit(title_text, (10, HEIGHT // 2 - FONT_SIZE))
    screen.blit(instruction_text, (10, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(3)


def show_menu():
    while True:
        screen.fill(BLACK)
        menu_texts = [
            "1. Таблица победителей(UP)",
            "2. Таблица участников(DOWN)",
            "3. Начать игру(SPACE)",
            "4. Выход(ESCAPE)"
        ]

        for i, text in enumerate(menu_texts):
            rendered_text = font.render(text, True, WHITE)
            screen.blit(rendered_text, (5, 100 + i * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_SPACE:
                    run_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


show_splash_screen()
show_menu()