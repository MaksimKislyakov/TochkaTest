#!/usr/bin/env python3
import sys
from collections import deque, defaultdict
from functools import lru_cache


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    static_adj = defaultdict(set)
    gateway_edges = set()
    nodes, gateways = set(), set()

    for u, v in edges:
        nodes.add(u); nodes.add(v)
        if u.isupper() and not v.isupper():
            gateway_edges.add((u, v)); gateways.add(u)
        elif v.isupper() and not u.isupper():
            gateway_edges.add((v, u)); gateways.add(v)
        else:
            static_adj[u].add(v); static_adj[v].add(u)

    def build_adj(rem):
        adj = {n: set(static_adj[n]) for n in nodes}
        for g, n in rem:
            adj[g].add(n); adj[n].add(g)
        return adj

    def find_target_and_path(adj, start):
        q = deque([start])
        dist = {start: 0}
        while q:
            cur = q.popleft()
            for nei in sorted(adj[cur]):
                if nei not in dist:
                    dist[nei] = dist[cur] + 1
                    q.append(nei)
        min_d, cands = None, []
        for g in gateways:
            if g in dist:
                d = dist[g]
                if min_d is None or d < min_d:
                    min_d, cands = d, [g]
                elif d == min_d:
                    cands.append(g)
        if min_d is None:
            return None, []
        target = min(cands)
        q = deque([start]); parent = {start: None}
        while q:
            cur = q.popleft()
            if cur == target:
                break
            for nei in sorted(adj[cur]):
                if nei not in parent:
                    parent[nei] = cur; q.append(nei)
        if target not in parent:
            return None, []
        path, cur = [], target
        while cur is not None:
            path.append(cur); cur = parent[cur]
        path.reverse()
        return target, path

    def virus_step(adj, virus_pos):
        target, path = find_target_and_path(adj, virus_pos)
        if not path:
            return None
        return path[1] if len(path) >= 2 else path[0]

    @lru_cache(maxsize=None)
    def can_win(rem_frozen, virus):
        rem = set(rem_frozen)
        adj = build_adj(rem)
        nxt = virus_step(adj, virus)
        if nxt is None:
            return True
        if not rem:
            return False
        for g, n in sorted(rem):
            new_rem = rem.copy(); new_rem.remove((g, n))
            adj2 = build_adj(new_rem)
            vnext = virus_step(adj2, virus)
            if vnext is None:
                return True
            if vnext.isupper():
                continue
            if can_win(frozenset(new_rem), vnext):
                return True
        return False

    res, rem, virus = [], set(gateway_edges), 'a'
    while True:
        adj = build_adj(rem)
        if virus_step(adj, virus) is None:
            break
        chosen = None
        for g, n in sorted(rem):
            new_rem = rem.copy(); new_rem.remove((g, n))
            adj2 = build_adj(new_rem)
            vnext = virus_step(adj2, virus)
            if vnext is None or (not vnext.isupper() and can_win(frozenset(new_rem), vnext)):
                chosen = (g, n)
                rem = new_rem
                res.append(f"{g}-{n}")
                break
        if not chosen:
            break
        adj_after = build_adj(rem)
        vstep = virus_step(adj_after, virus)
        if vstep is None or vstep.isupper():
            break
        virus = vstep

    return res


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            a, _, b = line.partition('-')
            edges.append((a, b))
    for e in solve(edges):
        print(e)


if __name__ == "__main__":
    main()
