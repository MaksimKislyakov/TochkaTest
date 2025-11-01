#!/usr/bin/env python3
import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса.

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """

    # --- Построение графа ---
    graph = defaultdict(set)
    gateways = set()
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
        if u.isupper():
            gateways.add(u)
        if v.isupper():
            gateways.add(v)

    virus = 'a'  # начальная позиция вируса
    result = []

    # --- Основной цикл ---
    while True:
        # Находим ближайший шлюз и путь до него
        target, path = find_target_path(graph, gateways, virus)
        if not target:
            break  # вирус не может добраться ни до одного шлюза

        # Если вирус уже рядом со шлюзом — надо срочно изолировать этот шлюз
        for g in sorted(gateways):
            for n in sorted(graph[g]):
                if n == virus:
                    result.append(f"{g}-{n}")
                    graph[g].remove(n)
                    graph[n].remove(g)
                    break
            else:
                continue
            break
        else:
            # Иначе блокируем ближайшее возможное соединение шлюза
            next_node = path[1] if len(path) > 1 else virus
            # Проверим, какой шлюз соединён с узлом на пути
            candidates = []
            for g in gateways:
                for n in graph[g]:
                    if n == next_node:
                        candidates.append(f"{g}-{n}")
            if candidates:
                block = sorted(candidates)[0]
                g, n = block.split('-')
                graph[g].remove(n)
                graph[n].remove(g)
                result.append(block)
            else:
                # Если нет прямого соединения — выберем лексикографически минимальное из доступных
                all_edges = [f"{g}-{n}" for g in gateways for n in graph[g]]
                if not all_edges:
                    break
                block = sorted(all_edges)[0]
                g, n = block.split('-')
                graph[g].remove(n)
                graph[n].remove(g)
                result.append(block)

        # После отключения вирус делает ход
        target, path = find_target_path(graph, gateways, virus)
        if not target:
            break
        if len(path) >= 2:
            virus = path[1]
        else:
            break

    return result


def find_target_path(graph, gateways, start):
    """
    Находит ближайший шлюз и путь до него.

    Args:
        graph: граф сети (dict)
        gateways: множество шлюзов
        start: текущая позиция вируса

    Returns:
        (шлюз, путь_список)
    """
    visited = {start}
    q = deque([(start, [start])])
    found = []
    while q:
        node, path = q.popleft()
        if node in gateways:
            found.append((node, path))
            break
        for nei in sorted(graph[node]):
            if nei not in visited:
                visited.add(nei)
                q.append((nei, path + [nei]))
    if not found:
        return None, []
    found.sort(key=lambda x: (len(x[1]), x[0]))
    return found[0]


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
