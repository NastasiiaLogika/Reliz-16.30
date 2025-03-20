import pygame
import random
import string

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Генератор паролей")

# Цвета
DARK_GRAY = (50, 50, 50)
WHITE = (245, 245, 245)
FORESTGREEN = (0, 100, 0)
RED = (128, 0, 0)

# Шрифт
font = pygame.font.SysFont(None, 30)

# Функция для генерации пароля
def generate_password(length, use_uppercase, use_numbers, use_special_chars, mandatory_chars):
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    numbers = string.digits
    special_chars = string.punctuation

    characters = lowercase_chars
    if use_uppercase:
        characters += uppercase_chars
    if use_numbers:
        characters += numbers
    if use_special_chars:
        characters += special_chars


    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Убедимся, что обязательные символы присутствуют
    for char in mandatory_chars:
        if char not in password:
            password = password[:-1] + random.choice(characters)  # Заменим последний символ на обязательный

    return password

# Основная функция
def main():
    running = True
    password = ''
    length = 3
    use_uppercase = True
    use_numbers = True
    use_special_chars = True
    mandatory_chars = ''  # Переменная для обязательных символов
    input_active = False  # Флаг для активации ввода текста
    input_text = ''  # Храним введенный текст
    cursor_pos = len(input_text)  # Позиция курсора в тексте
    
    while running:
        screen.fill(DARK_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 20 <= mouse_x <= 70 and 100 <= mouse_y <= 130:
                    length = max(3, length - 1)
                elif 80 <= mouse_x <= 130 and 100 <= mouse_y <= 130:
                    length += 1  # Увеличиваем длину пароля на 1
                elif 20 <= mouse_x <= 40 and 150 <= mouse_y <= 170:
                    use_uppercase = not use_uppercase
                elif 20 <= mouse_x <= 40 and 190 <= mouse_y <= 210:
                    use_numbers = not use_numbers
                elif 20 <= mouse_x <= 40 and 230 <= mouse_y <= 250:
                    use_special_chars = not use_special_chars
                elif 20 <= mouse_x <= 480 and 300 <= mouse_y <= 330:
                    input_active = True  # Активируем поле для ввода
                elif 20 <= mouse_x <= 220 and 340 <= mouse_y <= 380:
                    password = generate_password(length, use_uppercase, use_numbers, use_special_chars, mandatory_chars)
                

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Удаляем последний символ
                elif event.key == pygame.K_RETURN:
                    mandatory_chars = input_text  # Устанавливаем введенный текст как обязательный
                    input_active = False  # Деактивируем поле ввода
                else:
                    input_text += event.unicode  # Добавляем введенный символ в текст

        # Отображение текста
        title_text = font.render("Генератор паролей", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))

        # Настройка длины пароля
        length_text = font.render(f"Длина пароля: {length}", True, WHITE)
        screen.blit(length_text, (20, 60))

        # Кнопки для изменения длины
        pygame.draw.rect(screen, FORESTGREEN, (20, 100, 50, 30))
        pygame.draw.rect(screen, FORESTGREEN, (80, 100, 50, 30))
        decrease_text = font.render("-", True, DARK_GRAY)
        increase_text = font.render("+", True, DARK_GRAY)
        screen.blit(decrease_text, (35, 105))
        screen.blit(increase_text, (95, 105))

        # Флаги включения символов
        pygame.draw.rect(screen, WHITE, (20, 150, 20, 20))
        pygame.draw.rect(screen, FORESTGREEN if use_uppercase else RED, (40, 150, 20, 20))
        uppercase_text = font.render("Прописные", True, WHITE)
        screen.blit(uppercase_text, (70, 150))

        pygame.draw.rect(screen, WHITE, (20, 190, 20, 20))
        pygame.draw.rect(screen, FORESTGREEN if use_numbers else RED, (40, 190, 20, 20))
        numbers_text = font.render("Цифры", True, WHITE)
        screen.blit(numbers_text, (70, 190))

        pygame.draw.rect(screen, WHITE, (20, 230, 20, 20))
        pygame.draw.rect(screen, FORESTGREEN if use_special_chars else RED, (40, 230, 20, 20))
        special_chars_text = font.render("Спецсимволы", True, WHITE)
        screen.blit(special_chars_text, (70, 230))


        # Запрос обязательных символов
        mandatory_text = font.render("Обязательные символы:", True, WHITE)
        screen.blit(mandatory_text, (20, 270))

        # Поле для ввода обязательных символов
        pygame.draw.rect(screen, WHITE, (20, 300, 460, 30))
        input_rect = pygame.draw.rect(screen, FORESTGREEN, (20, 300, 460, 30), 2)
        input_display_text = font.render(input_text, True, DARK_GRAY)
        screen.blit(input_display_text, (25, 305))

        # Генерация пароля
        pygame.draw.rect(screen, FORESTGREEN, (20, 340, 200, 40))
        generate_text = font.render("Сгенерировать", True, DARK_GRAY)
        screen.blit(generate_text, (20 + 100 - generate_text.get_width() // 2, 345))


        # Отображение пароля
        password_text = font.render(f"Пароль: {password}", True, WHITE)
        screen.blit(password_text, (20, 400))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

