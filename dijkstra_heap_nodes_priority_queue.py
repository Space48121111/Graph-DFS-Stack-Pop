from __future__ import annotations
from typing import Generator
from heapq import heappop, heappush

txt = open('dijkstra_heap_nodes_priority_queue.txt', 'r')
input1 = txt.read()
input = '''\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''

'''

output = 40 not including the starting point for not entering -1
lowest risk; 1-1-2136511-15-1-13-2-3-21-1
output1 = 315 in a 5 * 5 expanded map
risk += 1  > 9 -> 1
8 ->
8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7

algorithm/brutal force:
dijkstra O(V + E * logV)
heap preprocessing
coords generator yield (x + 1, y) (x, y - 1)
heap nodes heapq priority queue

coord, risk = heapq.heappop(priority_q)
if end -> return risk
in coords and not seen
heapq.heappush(priority_q, candid, risk + coords[candid]) seen = True

'''
def dijkstra_heap(s: int) -> int:
    m = [list(map(int, line)) for line in s.splitlines()]
    height, width = len(m), len(m[0])

    for i in 1, 5:
        heap, seen = [(0, 0, 0)], {(0, 0)}
        while heap:
            risk, r, c = heappop(heap)
            if r == i * height - 1 and\
            c == i * height - 1:
                print(risk)
                break
            else:
                for r_, c_ in (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1):
                    if 0 <= r_ < i * height and\
                    0 <= c_ < i * height and\
                    (r_, c_) not in seen:
                        rd, rm = divmod(r_, height)
                        cd, cm = divmod(c_, width)

                        seen.add((r_, c_))
                        heappush(heap, (\
                        risk + (m[rm][cm] + rd + cd - 1) % 9 + 1,\
                        r_, c_
                        ))
                        # print('Heap ', heap)
                        # print('Risk', risk)

        return risk


def adjacent_coords_generator(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1
def heap_pop_push(s: int) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, val in enumerate(line):
            coords[(x, y)] = int(val)
    # print('Coords ', coords)
    end = max(coords)
    print('End ', end)
    priority_q = [(0, (0, 0))]
    seen = set()
    # seen = {(0, 0)}
    while priority_q:
        risk, coord = heappop(priority_q)
        if coord == end:
            return risk
            # print(risk)
            # break
        elif coord not in seen:
            for adj_coord in adjacent_coords_generator(*coord):
                if adj_coord in coords:
                # coords line by line
                    seen.add(coord)
                    heappush(priority_q,(\
                    risk + coords[adj_coord],\
                    adj_coord
                    ))
                    # print('Adj coord and risk ', adj_coord, risk)
                    # print('Heapq poppush', priority_q)

    raise AssertionError('Unreachable')
    return risk

print(dijkstra_heap(input))
print(heap_pop_push(input))
# output1: 472





# end
