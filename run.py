#!/usr/bin/env python3
# Python 3.12
import sys
import heapq


def solve(lines: list[str]) -> int:
    """
    Решает задачу о сортировке амфиподов в лабиринте.

    Args:
        lines: Список строк, представляющих лабиринт (включая стены и комнаты).

    Returns:
        Минимальная суммарная энергия, необходимая для достижения целевой конфигурации.
    """

    # --- Вспомогательные структуры ---
    hallway_positions = [0, 1, 3, 5, 7, 9, 10]
    room_positions = [2, 4, 6, 8]
    energy_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    room_for = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    # --- Парсинг входных данных ---
    rooms = []
    for line in lines[2:-1]:
        row = [c for c in line if c in "ABCD"]
        rooms.append(row)
    depth = len(rooms)
    rooms = list(map(list, zip(*rooms)))  # Транспонирование: по комнатам

    start_state = (tuple('.' * 11), tuple(tuple(r) for r in rooms))
    final_state = (
        tuple('.' * 11),
        tuple(tuple(x for _ in range(depth)) for x in "ABCD")
    )

    # --- Вспомогательные функции ---
    def is_path_clear(hall, a, b):
        if a < b:
            return all(c == '.' for c in hall[a + 1:b + 1])
        else:
            return all(c == '.' for c in hall[b:a])

    def move_to_room(hall, rooms, i):
        amph = hall[i]
        target = room_for[amph]
        room = rooms[target]
        if any(c != amph and c != '.' for c in room):
            return []
        room_pos = room_positions[target]
        if not is_path_clear(hall, i, room_pos):
            return []
        depth_index = max(d for d, c in enumerate(room) if c == '.')
        steps = abs(i - room_pos) + depth_index + 1
        new_hall = list(hall)
        new_rooms = [list(r) for r in rooms]
        new_hall[i] = '.'
        new_rooms[target][depth_index] = amph
        return [(tuple(new_hall), tuple(tuple(r) for r in new_rooms), steps * energy_cost[amph])]

    def move_to_hall(hall, rooms, room_idx):
        room = rooms[room_idx]
        room_label = "ABCD"[room_idx]
        for depth_index, amph in enumerate(room):
            if amph == '.':
                continue
            # Если все оставшиеся внизу амфиподы уже правильные — не выходим
            if amph == room_label and all(c == room_label for c in room[depth_index:]):
                return []
            room_pos = room_positions[room_idx]
            results = []
            for i in hallway_positions:
                if is_path_clear(hall, i, room_pos):
                    steps = abs(i - room_pos) + depth_index + 1
                    new_hall = list(hall)
                    new_rooms = [list(r) for r in rooms]
                    new_rooms[room_idx][depth_index] = '.'
                    new_hall[i] = amph
                    results.append(
                        (tuple(new_hall), tuple(tuple(r) for r in new_rooms), steps * energy_cost[amph])
                    )
            return results
        return []

    def neighbors(state):
        hall, rooms = state
        result = []
        # Ходы из коридора → в комнату
        for i, c in enumerate(hall):
            if c in "ABCD":
                result += move_to_room(hall, rooms, i)
        # Ходы из комнат → в коридор
        for j in range(4):
            result += move_to_hall(hall, rooms, j)
        return result

    # --- Алгоритм Дейкстры ---
    pq = [(0, start_state)]
    seen = {start_state: 0}
    while pq:
        cost, state = heapq.heappop(pq)
        if state == final_state:
            return cost
        if cost > seen[state]:
            continue
        for nstate, ncost in neighbors(state):
            total = cost + ncost
            if total < seen.get(nstate, 1e18):
                seen[nstate] = total
                heapq.heappush(pq, (total, nstate))

    return -1


def main():
    """Точка входа программы: считывает вход и выводит результат."""
    lines = [line.rstrip('\n') for line in sys.stdin if line.strip()]
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()