def find_next_target(last_hit, board, hits, shots):
    """Находит следующую цель для выстрела после попадания"""
    x, y = last_hit
    board_size = len(board)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < board_size and 0 <= ny < board_size:
            if hits[ny][nx] == 1:
                step = 1
                while True:
                    nx, ny = x + dx * step, y + dy * step
                    if 0 <= nx < board_size and 0 <= ny < board_size:
                        if (nx, ny) not in shots:
                            return nx, ny
                        if hits[ny][nx] != 1:
                            break
                        step += 1
                    else:
                        break
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < board_size and 0 <= ny < board_size:
            if (nx, ny) not in shots and hits[ny][nx] == 0:
                return nx, ny
    
    return None, None