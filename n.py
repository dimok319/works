import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 450, 500
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Цвета
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики - СЛОЖНЫЙ УРОВЕНЬ')
screen.fill(BG_COLOR)


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.game_over = False
        self.winner = None
        # Отслеживаем все ходы для ограничения количества фигур
        self.all_x_moves = []  # Все ходы крестиков
        self.all_o_moves = []  # Все ходы ноликов
        self.max_figures = 3  # Максимум 3 фигуры каждого типа
        self.first_move_done = False  # Флаг первого хода

    def draw_lines(self):
        # Горизонтальные линии
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

        # Вертикальные линии
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

    def draw_figures(self):
        # Очищаем доску и рисуем только текущие фигуры
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 'O':
                    pygame.draw.circle(screen, CIRCLE_COLOR,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                        row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       CIRCLE_RADIUS, CIRCLE_WIDTH)
                elif self.board[row][col] == 'X':
                    pygame.draw.line(screen, CROSS_COLOR,
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                                      row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR,
                                     (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                                      row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

    def draw_status(self):
        status_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
        pygame.draw.rect(screen, LINE_COLOR, status_rect)

        font = pygame.font.SysFont('Arial', 20)

        if self.game_over:
            if self.winner:
                text = f"Победитель: {self.winner}!"
            else:
                text = "Ничья!"
        else:
            if not self.first_move_done:
                text = "Компьютер думает..."
            else:
                text = "Ваш ход (X) - СЛОЖНЫЙ УРОВЕНЬ"

        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (10, HEIGHT - 40))

        # Статистика фигур
        stats_text = f"Крестиков: {len(self.all_x_moves)}/3, Ноликов: {len(self.all_o_moves)}/3"
        stats_surface = font.render(stats_text, True, TEXT_COLOR)
        screen.blit(stats_surface, (10, HEIGHT - 20))

    def remove_oldest_figure(self, player):
        """Удаляет самую старую фигуру указанного игрока"""
        if player == 'X' and self.all_x_moves:
            oldest_row, oldest_col = self.all_x_moves.pop(0)
            self.board[oldest_row][oldest_col] = ' '
            print(f"Удален старый крестик с ({oldest_row}, {oldest_col})")

        elif player == 'O' and self.all_o_moves:
            oldest_row, oldest_col = self.all_o_moves.pop(0)
            self.board[oldest_row][oldest_col] = ' '
            print(f"Удален старый нолик с ({oldest_row}, {oldest_col})")

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ' and not self.game_over:
            # Проверяем, не превышен ли лимит фигур
            if player == 'X' and len(self.all_x_moves) >= self.max_figures:
                self.remove_oldest_figure('X')
            elif player == 'O' and len(self.all_o_moves) >= self.max_figures:
                self.remove_oldest_figure('O')

            # Добавляем новую фигуру
            self.board[row][col] = player

            # Сохраняем ход в историю
            if player == 'X':
                self.all_x_moves.append((row, col))
                print(f"Добавлен крестик на ({row}, {col}). Всего крестиков: {len(self.all_x_moves)}")
            else:
                self.all_o_moves.append((row, col))
                print(f"Добавлен нолик на ({row}, {col}). Всего ноликов: {len(self.all_o_moves)}")

            # Отмечаем, что первый ход сделан
            if not self.first_move_done:
                self.first_move_done = True

            self.check_winner()
            return True
        return False

    def check_winner(self):
        # Проверка строк
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                self.winner = row[0]
                self.game_over = True
                return

        # Проверка столбцов
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.winner = self.board[0][col]
                self.game_over = True
                return

        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[0][0]
            self.game_over = True
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winner = self.board[0][2]
            self.game_over = True
            return

    def evaluate_position(self, row, col, player):
        """Оценивает позицию для хода"""
        score = 0

        # Временно делаем ход
        temp_board = [row[:] for row in self.board]
        temp_board[row][col] = player

        # Проверяем выигрышные комбинации
        lines_to_check = [
            # Горизонтальные
            [(row, 0), (row, 1), (row, 2)],
            # Вертикальные
            [(0, col), (1, col), (2, col)],
            # Диагонали (если применимо)
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        for line in lines_to_check:
            values = [temp_board[r][c] for r, c in line]
            if values.count(player) == 2 and values.count(' ') == 1:
                score += 10  # Почти выигрышная позиция
            elif values.count(player) == 3:
                score += 100  # Победа!
            elif values.count(self.get_opponent(player)) == 2 and values.count(' ') == 1:
                score += 8  # Блокировка противника

        # Центр имеет большее значение
        if (row, col) == (1, 1):
            score += 3

        # Углы имеют среднее значение
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        if (row, col) in corners:
            score += 2

        return score

    def get_opponent(self, player):
        return 'X' if player == 'O' else 'O'

    def computer_first_move(self):
        """Первый ход компьютера"""
        # Для первого хода выбираем случайный угол или центр
        first_moves = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]
        valid_moves = [move for move in first_moves if self.board[move[0]][move[1]] == ' ']

        if valid_moves:
            row, col = random.choice(valid_moves)
            self.make_move(row, col, 'O')
            print(f"Компьютер сделал первый ход на ({row}, {col})")
            return True
        return False

    def computer_move(self):
        """Ход компьютера с максимальной сложностью"""
        if self.game_over:
            return False

        print("Компьютер думает...")
        available_moves = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    available_moves.append((i, j))

        if not available_moves:
            # Если нет свободных клеток, освобождаем свою самую старую фигуру
            if self.all_o_moves:
                oldest_row, oldest_col = self.all_o_moves[0]
                self.board[oldest_row][oldest_col] = ' '
                available_moves.append((oldest_row, oldest_col))
                print("Нет свободных клеток, компьютер освобождает свою старую фигуру")
            else:
                return False

        best_score = -1000
        best_moves = []

        # Оцениваем все возможные ходы
        for row, col in available_moves:
            # Оценка атаки (можем ли мы выиграть)
            attack_score = self.evaluate_position(row, col, 'O')

            # Оценка защиты (нужно ли блокировать игрока)
            defense_score = self.evaluate_position(row, col, 'X')

            # Общая оценка (приоритет атаке)
            total_score = attack_score * 2 + defense_score

            print(f"Ход ({row}, {col}): атака={attack_score}, защита={defense_score}, всего={total_score}")

            if total_score > best_score:
                best_score = total_score
                best_moves = [(row, col)]
            elif total_score == best_score:
                best_moves.append((row, col))

        # Выбираем лучший ход (случайно из лучших, если несколько)
        if best_moves:
            best_row, best_col = random.choice(best_moves)
            self.make_move(best_row, best_col, 'O')
            print(f"Компьютер пошел на ({best_row}, {best_col}) с оценкой {best_score}")
            return True

        return False

    def reset_game(self):
        self.__init__()


# Создаем игру
game = TicTacToe()
game.draw_lines()

print("Игра началась! СЛОЖНЫЙ УРОВЕНЬ")
print("Компьютер ходит первым!")
print("На поле не более 3 крестиков и 3 ноликов")

# Компьютер делает первый ход
pygame.time.delay(1000)  # Небольшая задержка для драматизма
game.computer_first_move()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over and game.first_move_done:
            mouseX, mouseY = event.pos

            if mouseY < HEIGHT - 50:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if game.make_move(clicked_row, clicked_col, 'X'):
                    # Перерисовываем поле
                    screen.fill(BG_COLOR)
                    game.draw_lines()
                    game.draw_figures()
                    game.draw_status()
                    pygame.display.update()

                    # Ход компьютера
                    if not game.game_over:
                        pygame.time.delay(800)
                        game.computer_move()
                        # Снова перерисовываем поле после хода компьютера
                        screen.fill(BG_COLOR)
                        game.draw_lines()
                        game.draw_figures()
                        game.draw_status()
                        pygame.display.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.reset_game()
                screen.fill(BG_COLOR)
                game.draw_lines()
                game.draw_figures()
                game.draw_status()
                pygame.display.update()
                # Компьютер снова делает первый ход после перезапуска
                pygame.time.delay(1000)
                game.computer_first_move()
                screen.fill(BG_COLOR)
                game.draw_lines()
                game.draw_figures()
                game.draw_status()
                pygame.display.update()

    # Обновляем экран
    game.draw_figures()
    game.draw_status()
    pygame.display.update()