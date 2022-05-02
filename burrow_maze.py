from __future__ import annotations
from typing import NamedTuple, Generator
import heapq

txt = open('burrow_maze.txt', 'r')
input1 = txt.read()
input = ''' \
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''
'''
input2 =
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
'''
'''
output = 12521 minimun energy to A-D slots
output2 = 44169 min
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

step 1: 40
#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########

rules: amber = 1, bronze = 10, copper = 100, desert = 1000
open spaces: no stop at room.neighbor
no hall to room except dst and no other.dst
stay at hall until step +1: into a room

algorithm/brutal force:
cost-based pathing graph: dijkstra's priority(min score) queue heap queue
depth-first with pruning
target1 = {a: (3, 2), b: (5, 2), c: (7, 2), d: (9, 2)}
target2 = {a: (3, 3), b: (5, 3), c: (7, 3), d: (9, 3)}
state a0, b0, c0, d0 memory slots/address id
map(x, y) type checker -immutable / dict + mutate/tuple
rows 1 2: dict[]
{'A': 0 B: 1 C: 2 D: 3} for c in 'ABCD': mapped = ord(c) - ord('A') print {c!r} {}
next_states:
if (a...d) not in line[3]:
    line[4] y--
open spaces = line[1][1:-2]
update: data structure dict --splat keys on **
seen = []
priority_queue = ()
while
    score, state = heappop()
    heappush()

move(a, b, c, d)
'''

pos = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
class State(NamedTuple):
    top: dict[int, int | None]
    row1: dict[int, int | None]
    row2: dict[int, int | None]
    def __hash__(self) -> int:
        return hash((tuple(self.top.items()), \
        tuple(self.row1.items()), \
        tuple(self.row2.items())))
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        else:
            return id(self) < id(other)
    @property
    def completed(self) -> bool:
        return (all(k == v for k, v in self.row1.items()) and \
         all(k == v for k, v in self.row2.items()))
    @classmethod
    def parse(cls, s: str) -> State:
        line = s.splitlines()
        return cls(dict.fromkeys((1, 3, 5, 7, 9), None), \
        {0: pos[line[2][3]], 1: pos[line[2][5]], \
        2: pos[line[2][7]], 3: pos[line[2][9]]}, \
        {0: pos[line[3][3]], 1: pos[line[3][5]], \
        2: pos[line[3][7]], 3: pos[line[3][9]]})

    def __repr__(self) -> str:
        return(f'State(\n' f'top={self.top!r},\n'
        f'row1={self.row1!r},\n' f'row2={self.row2!r}\n' f')')

def next_states(score: int, state: State) -> Generator[tuple[int, State], None, None]:
    for k, v in state.top.items():
        if v is None:
            continue

        tar_col = 2 + v * 2
        max_c = max(tar_col, k)
        min_c = min(tar_col, k)
        move_top = max_c - min_c
        if all(k2 <= min_c or k2 >= max_c or v2 is None \
        for k2, v2 in state.top.items()):
            if state.row2[v] is None:
                yield (score + (move_top + 2) * 10 ** v, \
                state._replace(top = {**state.top, k: None}, \
                row2 = {**state.row2, v: v}))
            elif state.row2[v] == v and state.row1[v] is None:
                yield (score + (move_top + 1) * 10 ** v, \
                state._replace(top = {**state.top, k: None}, \
                row1 = {**state.row1, v: v}))
    potential_tar = {k for k, v in state.top.items() if v is None}
    for i in range(4):
        if state.row1[i] == i and state.row2[i] == i:
            continue
        for tar in potential_tar:
            src_col = 2 + i * 2
            max_s = max(src_col, tar)
            min_s = min(src_col, tar)
            move_top_s = max_s - min_s
            if all(k2 <= min_s or k2 >= max_s or v2 is None \
            for k2, v2 in state.top.items()):
                    if state.row1[i] is not None:
                        yield (score + (move_top_s + 1) * 10 ** state.row1[i], \
                        state._replace(top = {**state.top, tar: state.row1[i]}, \
                        row1 = {**state.row1, i: None}))
                    elif state.row2[i] != i and state.row2[i] is not None:
                        yield (score + (move_top_s + 2) * 10 ** state.row2[i], \
                        state._replace(top = {**state.top, tar: state.row2[i]}, \
                        row2 = {**state.row2, i: None}))
def compute(s: str) -> int:
    initial = State.parse(s)
    seen = set()
    priority_q = [(0, initial)]
    while priority_q:
        score, state = heapq.heappop(priority_q)
        if state.completed:
            return score
        elif state in seen:
            continue
        else:
            seen.add(state)
        for tp in next_states(score, state):
            heapq.heappush(priority_q, tp)

    raise AssertionError('Unreachable!')


class State1(NamedTuple):
    top: dict[int, int | None]
    row1: dict[int, int | None]
    row2: dict[int, int | None]
    row3: dict[int, int | None]
    row4: dict[int, int | None]

    def __hash__(self) -> int:
        return hash((tuple(self.top.items()), \
        tuple(self.row1.items()), tuple(self.row2.items()), \
        tuple(self.row3.items()), tuple(self.row4.items())))
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, State1):
            return NotImplemented
        else:
            return id(self) < id(other)
    @property
    def completed(self) -> bool:
        return (all(k == v for k, v in self.row1.items()) and \
         all(k == v for k, v in self.row2.items()) and \
         all(k == v for k, v in self.row3.items()) and \
         all(k == v for k, v in self.row4.items()))
    @classmethod
    def parse1(cls, s: str) -> State1:
        line = s.splitlines()
        return cls(dict.fromkeys((0, 1, 3, 5, 7, 9, 10), None), \
        {0: pos[line[2][3]], 1: pos[line[2][5]], \
        2: pos[line[2][7]], 3: pos[line[2][9]]}, \
        {0: pos['D'], 1: pos['C'], 2: pos['B'], 3: pos['A']}, \
        {0: pos['D'], 1: pos['B'], 2: pos['A'], 3: pos['C']}, \
        {0: pos[line[3][3]], 1: pos[line[3][5]], \
        2: pos[line[3][7]], 3: pos[line[3][9]]})

    def __repr__(self) -> str:
        return(f'State(\n' f'top={self.top!r},\n'
        f'row1={self.row1!r},\n' f'row2={self.row2!r}\n'
        f'row3={self.row3!r},\n' f'row4={self.row4!r}\n' f')')

def next_states1(score: int, state: State1) -> Generator[tuple[int, State], None, None]:
    for k, v in state.top.items():
        if v is None:
            continue

        tar_col = 2 + v * 2
        max_c = max(tar_col, k)
        min_c = min(tar_col, k)
        move_top = max_c - min_c
        if all(k2 <= min_c or k2 >= max_c or v2 is None \
        for k2, v2 in state.top.items()):
            if state.row4[v] is None:
                yield (score + (move_top + 4) * 10 ** v, \
                state._replace(top = {**state.top, k: None}, \
                row4 = {**state.row4, v: v}))
            elif state.row4[v] == v and state.row3[v] is None:
                yield (score + (move_top + 3) * 10 ** v, \
                state._replace(top = {**state.top, k: None}, \
                row3 = {**state.row3, v: v}))
            elif state.row4[v] == v and state.row3[v] == v and state.row2[v] is None:
                yield (score + (move_top + 2) * 10 ** v, \
                state._replace(top = {**state.top, k: None}, \
                row2 = {**state.row2, v: v}))
            elif state.row4[v] == v and state.row3[v] == v and \
            state.row2[v] == v and state.row1[v] is None:
                yield (score + (move_top + 1) * 10 ** v, \
                state._replace(top = {**state.top, k: None}, \
                row1 = {**state.row1, v: v}))
    potential_tar = {k for k, v in state.top.items() if v is None}
    for i in range(4):
        if state.row1[i] == i and state.row2[i] == i and state.row3[i] == state.row4[i]:
            continue
        for tar in potential_tar:
            src_col = 2 + i * 2
            max_s = max(src_col, tar)
            min_s = min(src_col, tar)
            move_top_s = max_s - min_s
            if all(k2 <= min_s or k2 >= max_s or v2 is None \
            for k2, v2 in state.top.items()):
                    if state.row1[i] is not None and (state.row1[i] != i \
                    or state.row2[i] != i or state.row3[i] != i or state.row4[i] != i):
                        yield (score + (move_top_s + 1) * 10 ** state.row1[i], \
                        state._replace(top = {**state.top, tar: state.row1[i]}, \
                        row1 = {**state.row1, i: None}))
                    elif state.row1[i] is None and state.row2[i] is not None and \
                    (state.row2[i] != i or state.row3[i] != i or state.row4[i] != i):
                        yield (score + (move_top_s + 2) * 10 ** state.row2[i], \
                        state._replace(top = {**state.top, tar: state.row2[i]}, \
                        row2 = {**state.row2, i: None}))
                    elif state.row1[i] is None and state.row2[i] is None and \
                    state.row3[i] is not None and (state.row3[i] != i or state.row4[i] != i):
                        yield (score + (move_top_s + 3) * 10 ** state.row3[i], \
                        state._replace(top = {**state.top, tar: state.row3[i]}, \
                        row3 = {**state.row3, i: None}))
                    elif state.row1[i] is None and state.row2[i] is None and \
                    state.row3[i] is None and state.row4[i] is not None and state.row4[i] != i:
                        yield (score + (move_top_s + 4) * 10 ** state.row4[i], \
                        state._replace(top = {**state.top, tar: state.row4[i]}, \
                        row4 = {**state.row4, i: None}))
def compute1(s: str) -> int:
    initial = State1.parse1(s)
    seen = set()
    priority_q = [(0, initial)]
    while priority_q:
        score, state = heapq.heappop(priority_q)
        if state.completed:
            return score
        elif state in seen:
            continue
        else:
            seen.add(state)
        for tp in next_states1(score, state):
            heapq.heappush(priority_q, tp)

    raise AssertionError('Unreachable!')


print(compute(input))
print(compute1(input))














# end
