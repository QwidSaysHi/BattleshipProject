from algo_finish_search import find_next_target

class ChessBot:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.shots = []
        self.hits = []
        self.last_hit = None
        self.chess_pattern = self._generate_chess_pattern()
        self.chess_index = 0
    
    def _generate_chess_pattern(self):
        """Генерирует координаты в шахматном порядке (сначала все черные клетки, затем белые)"""
        black_cells = []
        white_cells = []
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if (x + y) % 2 == 0:
                    black_cells.append((x, y))
                else:
                    white_cells.append((x, y))
        
        return black_cells + white_cells
    
    def make_shot(self, board, hits):
        """Делает выстрел в шахматном порядке, при попадании использует rational_algorithm"""
        if self.last_hit and any(hits[y][x] == 1 for y in range(self.board_size) for x in range(self.board_size)):
            x, y = find_next_target(self.last_hit, board, hits, self.shots)
            if x is not None and y is not None:
                self.shots.append((x, y))
                return x, y
        
        while self.chess_index < len(self.chess_pattern):
            x, y = self.chess_pattern[self.chess_index]
            self.chess_index += 1
            if (x, y) not in self.shots:
                self.shots.append((x, y))
                return x, y
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if (x, y) not in self.shots:
                    self.shots.append((x, y))
                    return x, y
        
        return None, None  # Все клетки проверены
    
    def update(self, x, y, result, hits):
        """Обновляет состояние бота после выстрела"""
        if result == 'hit':
            self.hits.append((x, y))
            self.last_hit = (x, y)
        elif result == 'destroyed':
            self.last_hit = None