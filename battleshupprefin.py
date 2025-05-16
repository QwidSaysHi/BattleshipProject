import pygame
import random
import sys
import numpy as np
import os
from algo_random import Bot
from algo_chess import ChessBot
from algo_diag import DiamondBot
from algo_zone import ZoneBot
from algo_search import SearchBot
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 680 
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // (GRID_SIZE + 2)
PADDING = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHIP_COLOR = (100, 100, 100)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Морской бой")

try:
    font_path = os.path.join('fonts', 'pusab.ttf')  
    font_small = pygame.font.Font(font_path, 32)
    font_medium = pygame.font.Font(font_path, 40)
    font_large = pygame.font.Font(font_path, 48)
except:
    font_small = pygame.font.SysFont('Arial', 24)
    font_medium = pygame.font.SysFont('Arial', 32)
    font_large = pygame.font.SysFont('Arial', 48)

board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0-пусто, 1-корабль, 2-попадание, 3-промах
hits = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0-нет попадания, 1-попадание, -1-уничтожен
ships = [] 
ships_to_place = [(4, 1), (3, 2), (2, 3), (1, 4)]  # (длина, количество)
shots = 0 
game_over = False  

class Ship:
    def __init__(self, length, x, y, horizontal):
        self.length = length
        self.coords = self._calculate_coords(x, y, horizontal)
        self.hits = 0
        self.destroyed = False
    
    def _calculate_coords(self, x, y, horizontal):
        coords = []
        for i in range(self.length):
            if horizontal:
                coords.append((x + i, y))
            else:
                coords.append((x, y + i))
        return coords
    
    def check_destroyed(self):
        return self.hits >= self.length

def init_game():
    global board, hits, ships, shots, game_over
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    hits = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    ships = []
    shots = 0
    game_over = False
    place_all_ships()

def place_all_ships():
    for ship_length, ship_count in ships_to_place:
        for _ in range(ship_count):
            place_ship(ship_length)

def place_ship(length):
    for _ in range(1000):  
        horizontal = random.choice([True, False])
        x = random.randint(0, GRID_SIZE - (length if horizontal else 1))
        y = random.randint(0, GRID_SIZE - (length if not horizontal else 1))
        
        if is_valid_position(x, y, length, horizontal):
            ship = Ship(length, x, y, horizontal)
            for cx, cy in ship.coords:
                board[cy][cx] = 1
            ships.append(ship)
            return True
    return False


def is_valid_position(x, y, length, horizontal):
    for i in range(length):
        nx = x + (i if horizontal else 0)
        ny = y + (i if not horizontal else 0)
        
        if nx >= GRID_SIZE or ny >= GRID_SIZE:
            return False
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if 0 <= nx + dx < GRID_SIZE and 0 <= ny + dy < GRID_SIZE:
                    if board[ny + dy][nx + dx] == 1:
                        return False
    return True

def draw_grid():
    # Отрисовка игрового поля
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(
                (x + 1) * CELL_SIZE, 
                (y + 1) * CELL_SIZE + PADDING, 
                CELL_SIZE, 
                CELL_SIZE
            )
            
            # Цвет клетки в зависимости от состояния
            if board[y][x] == 3:  
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 8)
            elif board[y][x] == 2: 
                pygame.draw.rect(screen, ORANGE, rect)
            elif board[y][x] == 1:
                pygame.draw.rect(screen, SHIP_COLOR, rect)    
            elif hits[y][x] == -1: 
                pygame.draw.rect(screen, RED, rect)
            
            pygame.draw.rect(screen, BLACK, rect, 1) 

    # Подписи осей
    for i in range(GRID_SIZE):
        letter = chr(ord('A') + i)
        text = font_small.render(letter, True, BLACK)
        screen.blit(text, ((i + 1) * CELL_SIZE + CELL_SIZE // 3, PADDING + 10))
        
        number = str(i + 1)
        text = font_small.render(number, True, BLACK)
        screen.blit(text, (10, (i + 1) * CELL_SIZE + PADDING + CELL_SIZE // 3))

def draw_ui():
    shots_text = font_small.render(f"Выстрелы: {shots}", True, BLUE)
    screen.blit(shots_text, (SCREEN_WIDTH // 2 - shots_text.get_width() // 2, SCREEN_HEIGHT - 45))
    
    controls_text1 = font_small.render("R - Новая игра", True, BLACK)
    controls_text2 = font_small.render("T - Статистика", True, BLACK)
    screen.blit(controls_text1, (20, SCREEN_HEIGHT - 90))
    screen.blit(controls_text2, (SCREEN_WIDTH - controls_text2.get_width() - 20, SCREEN_HEIGHT - 90))
    
    if game_over:
        text1 = font_medium.render("Игра окончена!", True, RED)
        text2 = font_medium.render(f"Выстрелов: {shots}", True, RED)
        
        # Центрируем сообщение
        text_width = max(text1.get_width(), text2.get_width())
        text_height = text1.get_height() + text2.get_height()
        text_x = (SCREEN_WIDTH - text_width) // 2
        text_y = (SCREEN_HEIGHT - text_height) // 2
        
        # Фон
        pygame.draw.rect(screen, WHITE, (text_x - 20, text_y - 20, 
                                       text_width + 40, text_height + 40))
        pygame.draw.rect(screen, BLACK, (text_x - 20, text_y - 20, 
                                       text_width + 40, text_height + 40), 2)
        
        # Текст
        screen.blit(text1, (text_x, text_y))
        screen.blit(text2, (text_x, text_y + text1.get_height() + 10))

def handle_click(x, y):
    global shots, game_over
    
    if game_over or board[y][x] in (2, 3):
        return False
    
    if board[y][x] == 1:  
        board[y][x] = 2
        hits[y][x] = 1
        for ship in ships:
            if (x, y) in ship.coords:
                ship.hits += 1 
                
                if ship.check_destroyed():
                    ship.destroyed = True
                    mark_destroyed_ship(ship)
                
                game_over = all(s.destroyed for s in ships)
                break
    else: 
        board[y][x] = 3
        shots += 1

def mark_destroyed_ship(ship):
    for x, y in ship.coords:
        hits[y][x] = -1
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] == 0:
                    board[ny][nx] = 3

init_game()

running = True
input_active = False
input_text = ""

simulation_active = False
simulation_results = []
current_bot_class = None
shift_pressed = False

def run_simulation(bot_class, n_games):
    global simulation_results
    simulation_results = []
    

    for _ in range(n_games):
        if _%10000 == 0 and _ > 0:
            print(f"Игра: {_}")

        sim_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        sim_hits = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        sim_ships = []
        
        for ship_length, ship_count in ships_to_place:
            for _ in range(ship_count):
                placed = False
                for _ in range(1000): 
                    horizontal = random.choice([True, False])
                    x = random.randint(0, GRID_SIZE - (ship_length if horizontal else 1))
                    y = random.randint(0, GRID_SIZE - (ship_length if not horizontal else 1))
                    
                    if is_valid_position_sim(x, y, ship_length, horizontal, sim_board):
                        ship = Ship(ship_length, x, y, horizontal)
                        for cx, cy in ship.coords:
                            sim_board[cy][cx] = 1
                        sim_ships.append(ship)
                        placed = True
                        break
                if not placed:
                    print("Не удалось разместить все корабли")
                    return None
        bot = bot_class()
        shots_count = 0
        shots_sum = 0
        game_over = False
        dest_ship=0
        
        # print("===============")
        # printboard(sim_board)


        while not all(s.destroyed for s in sim_ships):
            # printboard(sim_board)

            x, y = bot.make_shot(sim_board, sim_hits)
            if x is None or y is None:  
                break
            
    
            if sim_board[y][x] == 1: 
                sim_board[y][x] = 2
                sim_hits[y][x] = 1

                test=0

                for ship in sim_ships:

                    test+=1
                    # print(f'test: {test}')
                
                    if (x, y) in ship.coords:
                        ship.hits += 1

                        if ship.check_destroyed():
                            ship.destroyed = True
                            dest_ship+=1
                            # print(dest_ship)
                            mark_destroyed_ship_sim(ship, sim_board, sim_hits)
                            bot.update(x, y, 'destroyed', sim_hits)
                        else:
                            bot.update(x, y, 'hit', sim_hits)

                        break
            if sim_board[y][x] == 0: 
                sim_board[y][x] = 3
                shots_count += 1     
                shots_sum += 1
            # if sim_board[y][x] == 3: 
            #     print("W")

            
        # print(sim_board)    
        # printboard(sim_board)
        simulation_results.append(shots_count)
    
    if simulation_results:
        results = np.array(simulation_results)

        print("\n=== Результаты симуляции ===")
        print(f"Количество игр: {n_games}")
        print(f"Минимальное количество ходов: {results.min()}")
        print(f"Максимальное количество ходов: {results.max()}")
        print(f"Среднее количество выстрелов: {results.mean():.2f}")
        print(f"Дисперсия: {results.var():.2f}")
        print(f"Стандартное отклонение: {results.std():.2f}")
        print(f"Доверительный интервал 99%: {results.mean():.2f} ± {2.576* results.std() / n_games :.2g}")
        print("===========================\n")

def printboard(board):
    print(" ")
    m = [" ", '#', 'x', '.']
    print("\n".join(["".join([m[y] for y in x]) for x in board]))

def is_valid_position_sim(x, y, length, horizontal, sim_board):
    for i in range(length):
        nx = x + (i if horizontal else 0)
        ny = y + (i if not horizontal else 0)
        
        if nx >= GRID_SIZE or ny >= GRID_SIZE:
            return False
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if 0 <= nx + dx < GRID_SIZE and 0 <= ny + dy < GRID_SIZE:
                    if sim_board[ny + dy][nx + dx] == 1:
                        return False
    return True

def mark_destroyed_ship_sim(ship, sim_board, sim_hits):
    for x, y in ship.coords:
        sim_hits[y][x] = -1
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                # print(dx,dy)
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if sim_board[ny][nx] == 0:
                        sim_board[ny][nx] = 3
                        sim_hits[ny][nx] = 100
                    # print(f'AA: {dx},{dy}')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_pressed = True
            elif event.key == pygame.K_r:  # Новая игра
                init_game()
            elif event.key == pygame.K_t:  # Статистика
                input_active = True
                input_text = ""
            elif input_active and event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif input_active and event.unicode.isdigit():
                input_text += event.unicode
            elif input_active and event.key == pygame.K_RETURN:
                if input_text.isdigit() and int(input_text) > 0:
                    n_games = int(input_text)
                    if current_bot_class:
                        run_simulation(current_bot_class, n_games)
                input_active = False
            elif event.key == pygame.K_1:  # Запуск random
                if shift_pressed:
                    current_bot_class = Bot
                    input_active = True
                    input_text = ""
                else:
                    bot = Bot()
                    while not game_over:
                        x, y = bot.make_shot(board, hits)
                        handle_click(x, y)
                        if board[y][x] == 2:
                            if any(ship.destroyed for ship in ships if (x, y) in ship.coords):
                                bot.update(x, y, 'destroyed', hits)
                            else:
                                bot.update(x, y, 'hit', hits)
                        pygame.time.delay(100)
                        screen.fill(WHITE)
                        draw_grid()
                        draw_ui()
                        pygame.display.flip()
            elif event.key == pygame.K_2:  # Запуск chess
                if shift_pressed:
                    current_bot_class = ChessBot
                    input_active = True
                    input_text = ""
                else:
                    bot = ChessBot()
                    while not game_over:
                        x, y = bot.make_shot(board, hits)
                        if x is None or y is None:
                            break
                        handle_click(x, y)
                        if board[y][x] == 2:
                            if any(ship.destroyed for ship in ships if (x, y) in ship.coords):
                                bot.update(x, y, 'destroyed', hits)
                            else:
                                bot.update(x, y, 'hit', hits)
                        pygame.time.delay(100)
                        screen.fill(WHITE)
                        draw_grid()
                        draw_ui()
                        pygame.display.flip()
            elif event.key == pygame.K_3:  # Запуск diamond
                if shift_pressed:
                    current_bot_class = DiamondBot
                    input_active = True
                    input_text = ""
                else:
                    bot = DiamondBot()
                    while not game_over:
                        x, y = bot.make_shot(board, hits)
                        if x is None or y is None:
                            break
                        handle_click(x, y)
                        if board[y][x] == 2:
                            if any(ship.destroyed for ship in ships if (x, y) in ship.coords):
                                bot.update(x, y, 'destroyed', hits)
                            else:
                                bot.update(x, y, 'hit', hits)
                        pygame.time.delay(100)
                        screen.fill(WHITE)
                        draw_grid()
                        draw_ui()
                        pygame.display.flip()
            elif event.key == pygame.K_4:  # Запуск zone
                if shift_pressed:
                    current_bot_class = ZoneBot
                    input_active = True
                    input_text = ""
                else:
                    bot = ZoneBot()
                    while not game_over:
                        x, y = bot.make_shot(board, hits)
                        if x is None or y is None:
                            break
                        handle_click(x, y)
                        if board[y][x] == 2:
                            if any(ship.destroyed for ship in ships if (x, y) in ship.coords):
                                bot.update(x, y, 'destroyed', hits)
                            else:
                                bot.update(x, y, 'hit', hits)
                        pygame.time.delay(100)
                        screen.fill(WHITE)
                        draw_grid()
                        draw_ui()
                        pygame.display.flip()
            elif event.key == pygame.K_5:  # Запуск search
                if shift_pressed:
                    current_bot_class = SearchBot
                    input_active = True
                    input_text = ""
                else:
                    bot = SearchBot()
                    while not game_over:
                        x, y = bot.make_shot(board, hits)
                        if x is None or y is None:
                            break
                        handle_click(x, y)
                        if board[y][x] == 2:
                            if any(ship.destroyed for ship in ships if (x, y) in ship.coords):
                                bot.update(x, y, 'destroyed', hits)
                            else:
                                bot.update(x, y, 'hit', hits)
                        pygame.time.delay(100)
                        screen.fill(WHITE)
                        draw_grid()
                        draw_ui()
                        pygame.display.flip()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            grid_x = (mouse_x // CELL_SIZE) - 1
            grid_y = ((mouse_y - PADDING) // CELL_SIZE) - 1
            
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                handle_click(grid_x, grid_y)

    screen.fill(WHITE)
    draw_grid()
    draw_ui()
    
    if input_active:
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//4, SCREEN_HEIGHT//2 - 30, 
                                       SCREEN_WIDTH//2, 60))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH//4, SCREEN_HEIGHT//2 - 30, 
                                       SCREEN_WIDTH//2, 60), 2)
        prompt = font_medium.render(f"N: {input_text}", True, BLACK)
        screen.blit(prompt, (SCREEN_WIDTH//4 + 10, SCREEN_HEIGHT//2 - 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()