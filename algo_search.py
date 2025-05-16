from algo_finish_search import find_next_target
import random

class SearchBot:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.shots = []
        self.hits = []
        self.last_hit = None
        self.phase = 0  # 0=4-палубные, 1=2-палубные, 2=случайные
        self.pattern_index = 0
        self.patterns = self._generate_patterns()

    def _generate_patterns(self):
        """Генерирует паттерны для каждой фазы"""
        patterns = {}
        
        # Фаза 0: 9 выстрелов для 4-палубных (шаг 4)
        phase0 = []
        for i in range(0, 10, 4):
            for j in range(0, 10, 4):
                phase0.append((i, j))
        patterns[0] = phase0
        
        # Фаза 1: сетка 5x5 (между выстрелами фазы 0)
        phase1 = []
        for i in range(2, 10, 4):
            for j in range(2, 10, 4):
                phase1.append((i, j))
        patterns[1] = phase1
        
        return patterns

    def make_shot(self, board, hits):
        """Делает выстрел по оптимизированной стратегии"""
        # Если есть незавершенное попадание, используем рациональный алгоритм
        if self.last_hit and any(hits[y][x] == 1 for y in range(self.board_size) for x in range(self.board_size)):
            x, y = find_next_target(self.last_hit, board, hits, self.shots)
            if x is not None and y is not None and (x, y) not in self.shots:
                self.shots.append((x, y))
                return x, y

        # Фаза 0: 9 выстрелов для 4-палубных
        if self.phase == 0:
            while self.pattern_index < len(self.patterns[0]):
                x, y = self.patterns[0][self.pattern_index]
                self.pattern_index += 1
                if (x, y) not in self.shots:
                    self.shots.append((x, y))
                    return x, y
            self.phase = 1
            self.pattern_index = 0

        # Фаза 1: сетка 5x5 для 2-палубных
        if self.phase == 1:
            while self.pattern_index < len(self.patterns[1]):
                x, y = self.patterns[1][self.pattern_index]
                self.pattern_index += 1
                if (x, y) not in self.shots:
                    self.shots.append((x, y))
                    return x, y
            self.phase = 2

        # Фаза 2: случайные выстрелы
        available = [(x, y) for x in range(self.board_size) 
                    for y in range(self.board_size) 
                    if (x, y) not in self.shots]
        if available:
            x, y = random.choice(available)
            self.shots.append((x, y))
            return x, y

        return None, None

    def update(self, x, y, result, hits):
        """Обновляет состояние бота после выстрела"""
        if result == 'hit':
            self.hits.append((x, y))
            self.last_hit = (x, y)
        elif result == 'destroyed':
            self.last_hit = None