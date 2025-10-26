#!/usr/bin/env python3
import sys
import heapq


def solve(lines: list[str]) -> int:
    """
    Решает задачу о сортировке амфиподов в лабиринте (оба варианта: глубина 2 и 4).

    Args:
        lines: Список строк, представляющих лабиринт.

    Returns:
        Минимальная суммарная энергия, необходимая для достижения целевой конфигурации.
    """
    hallway_positions = [0, 1, 3, 5, 7, 9, 10]
    room_positions = [2, 4, 6, 8]
    energy_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    room_for = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    rooms = []
    for line in lines[2:-1]:
        rooms.append([c for c in line if c in "ABCD"])
    depth = len(rooms)
    rooms = tuple(zip(*rooms))
    start = ('.' * 11, rooms)
    goal = ('.' * 11, tuple(tuple(ch for _ in range(depth)) for ch in "ABCD"))

    def path_clear(hall, a, b):
        step = 1 if a < b else -1
        for pos in range(a + step, b + step, step):
            if hall[pos] != '.':
                return False
        return True

    def moves(state):
        hall, rooms = state
        # 1. Попробовать переместить из холла в комнаты (приоритет!)
        for i, amph in enumerate(hall):
            if amph not in "ABCD":
                continue
            target = room_for[amph]
            room = rooms[target]
            if any(c != amph and c != '.' for c in room):
                continue
            dest = room_positions[target]
            if not path_clear(hall, i, dest):
                continue
            depth_idx = max(d for d, c in enumerate(room) if c == '.')
            steps = abs(i - dest) + depth_idx + 1
            new_hall = hall[:i] + '.' + hall[i + 1:]
            new_rooms = list(map(list, rooms))
            new_rooms[target][depth_idx] = amph
            yield (new_hall, tuple(tuple(r) for r in new_rooms)), steps * energy_cost[amph]
            return  # После успешного входа других ходов не ищем

        # 2. Перемещения из комнат в холл
        for r_idx, room in enumerate(rooms):
            room_label = "ABCD"[r_idx]
            if all(c in ('.', room_label) for c in room):
                continue
            for depth_idx, amph in enumerate(room):
                if amph == '.':
                    continue
                src = room_positions[r_idx]
                for pos in hallway_positions:
                    if path_clear(hall, src, pos):
                        steps = abs(pos - src) + depth_idx + 1
                        new_hall = hall[:pos] + amph + hall[pos + 1:]
                        new_rooms = list(map(list, rooms))
                        new_rooms[r_idx][depth_idx] = '.'
                        yield (new_hall, tuple(tuple(r) for r in new_rooms)), steps * energy_cost[amph]
                break 
        return

    pq = [(0, start)]
    seen = {start: 0}
    while pq:
        cost, state = heapq.heappop(pq)
        if state == goal:
            return cost
        if cost > seen[state]:
            continue
        for nstate, step_cost in moves(state):
            total = cost + step_cost
            if total < seen.get(nstate, 10**12):
                seen[nstate] = total
                heapq.heappush(pq, (total, nstate))
    return -1


def main():
    lines = [line.rstrip('\n') for line in sys.stdin if line.strip()]
    print(solve(lines))


if __name__ == "__main__":
    main()
