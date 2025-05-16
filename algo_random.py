import random
from algo_finish_search import find_next_target

class Bot:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.shots = []
        self.hits = []
        self.last_hit = None
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def make_shot(self, board, hits):
        """Делает выстрел, возвращает координаты (x, y)"""
        if self.last_hit and any(hits[y][x] == 1 for y in range(self.board_size) for x in range(self.board_size)):
            x, y = find_next_target(self.last_hit, board, hits, self.shots)
            if x is not None and y is not None:
                self.shots.append((x, y))
                return x, y
        
        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x, y) not in self.shots:
                self.shots.append((x, y))
                return x, y
    
    def update(self, x, y, result, hits):
        """Обновляет состояние бота после выстрела"""
        if result == 'hit':
            self.hits.append((x, y))
            self.last_hit = (x, y)
        elif result == 'destroyed':
            self.last_hit = None