import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
FONT_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = ['Red', 'Green', 'Blue', 'White',
          'Black', 'Yellow', 'Gray']

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

    screen.fill(WHITE)
    display_text("Игра окончена!",
                 small_font.get_height(),
                 BLACK,
                 WIDTH // 2,
                 HEIGHT // 2 - 50)

    display_text(f"Ваш ник: {player_name}",
                 small_font.get_height(),
                 BLACK,
                 WIDTH // 2,
                 HEIGHT // 2)

    display_text("Нажмите ESC для выхода",
                 small_font.get_height(),
                 BLACK,
                 WIDTH // 2,
                 HEIGHT // 2 + 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                show_menu()
                return

        pygame.display.flip()


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