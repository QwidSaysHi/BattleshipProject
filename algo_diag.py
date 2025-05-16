from algo_finish_search import find_next_target

class DiamondBot:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.shots = []
        self.hits = []
        self.last_hit = None
        self.pattern = self._generate_pattern()
        self.pattern_index = 0
    
    def _generate_pattern(self):
        """Генерирует паттерн стрельбы: диагонали -> меньшие диагонали -> шахматный порядок"""
        pattern = []
        
        # 1. Главные диагонали (полные)
        main_diag = [(i, i) for i in range(self.board_size)]
        anti_diag = [(i, self.board_size-1-i) for i in range(self.board_size)]
        pattern.extend(main_diag)
        pattern.extend([x for x in anti_diag if x not in main_diag])
        
        # 2. Меньшие диагонали через клетку (с шагом 2)
        # Диагонали, параллельные главной
        for offset in range(2, self.board_size, 2):
            # Верхний треугольник
            diag = [(i, i-offset) for i in range(offset, self.board_size) if i-offset >= 0]
            pattern.extend([x for x in diag if x not in pattern])
            
            # Нижний треугольник
            diag = [(i-offset, i) for i in range(offset, self.board_size) if i-offset >= 0]
            pattern.extend([x for x in diag if x not in pattern])
        
        # Диагонали, параллельные побочной
        for offset in range(2, self.board_size, 2):
            # Верхний треугольник
            diag = [(i, self.board_size-1-i+offset) for i in range(self.board_size-offset) 
                   if self.board_size-1-i+offset < self.board_size]
            pattern.extend([x for x in diag if x not in pattern])
            
            # Нижний треугольник
            diag = [(i+offset, self.board_size-1-i) for i in range(self.board_size-offset) 
                   if i+offset < self.board_size]
            pattern.extend([x for x in diag if x not in pattern])
        
        # 3. Шахматный порядок для оставшихся клеток
        for y in range(self.board_size):
            for x in range(self.board_size):
                if (x + y) % 2 == 0 and (x,y) not in pattern:
                    pattern.append((x,y))
        for y in range(self.board_size):
            for x in range(self.board_size):
                if (x + y) % 2 != 0 and (x,y) not in pattern:
                    pattern.append((x,y))
        
        return pattern
    
    def make_shot(self, board, hits):
        """Делает выстрел по заданному паттерну, при попадании использует rational_algorithm"""
        # Если есть незавершенное попадание, используем рациональный алгоритм
        if self.last_hit and any(hits[y][x] == 1 for y in range(self.board_size) for x in range(self.board_size)):
            x, y = find_next_target(self.last_hit, board, hits, self.shots)
            if x is not None and y is not None and 0 <= x < self.board_size and 0 <= y < self.board_size:
                self.shots.append((x, y))
                return x, y
        
        # Иначе стреляем по паттерну
        while self.pattern_index < len(self.pattern):
            x, y = self.pattern[self.pattern_index]
            self.pattern_index += 1
            if (x, y) not in self.shots and 0 <= x < self.board_size and 0 <= y < self.board_size:
                self.shots.append((x, y))
                return x, y
        
        # Если все клетки в паттерне проверены, стреляем в оставшиеся
        for y in range(self.board_size):
            for x in range(self.board_size):
                if (x, y) not in self.shots and 0 <= x < self.board_size and 0 <= y < self.board_size:
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