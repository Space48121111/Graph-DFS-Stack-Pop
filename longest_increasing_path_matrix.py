from __future__ import annotations
from collections import defaultdict
from collections import deque
from functools import cache

input = ''' \
matrix = [[9,9,4],[6,6,8],[2,1,1]]
'''
input1 = ''' \
matrix = [[3,4,5],[3,2,6],[2,2,1]]
'''
'''
output = 4 [1, 2, 6, 9]
output1 = 4 [3, 4, 5, 6]

algorithm: depth first search cache call back recursively
can go left, right, up, down (-1, 0) (1, 0)...
not diagonally nor outside the boundary
constraints:
    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 200
    0 <== matrix[i][j] <= 2^31 - 1
brutal force: topological deque pop append

'''
class Solution:
    def max_path(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        @cache
        def dfs(x, y):
            nonlocal m, n
            max_p = 0
            for d_x, d_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                c_x, c_y = d_x + x, d_y + y
                if 0 <= c_x < m and 0 <= c_y < n:
                    if matrix[x][y] < matrix[c_x][c_y]:
                        max_p = max(max_p, dfs(c_x, c_y))
            return max_p + 1
        res = 0
        for i in range(m):
            for j in range(n):
                res = max(res, dfs(i, j))
        return res + 1 # include the first vertex starting the edges


class Solution1:
    def max_p(self, matrix: List[list[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        if not n:
            return 0
        dep = defaultdict(int)
        stack = defaultdict(list)
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x in range(m):
            for y in range(n):
                seen = False
                for d_x, d_y in dir:
                    c_x = x + d_x
                    c_y = y + d_y
                    if c_x < 0 or c_x >= m or c_y < 0 or c_y >= n:
                        continue
                    if matrix[x][y] > matrix[c_x][c_y]:
                        seen = True
                        dep[(x, y)] += 1
                        stack[(c_x, c_y)].append((x, y))
                if not seen:
                    dep[(x, y)] = 0
        q = deque([])
        for k, v in dep.items():
            if v == 0:
                a0, b0 = k
                q.append((a0, b0, 1))
        max_p = 0
        while q:
            print('Queue ', q)
            a, b, path = q.popleft() # first in first out
            max_p = max(max_p, path)
            for i, j in stack[(a, b)]:
                dep[(i, j)] -= 1
                if dep[(i, j)] == 0:
                    q.append((i, j, path + 1))
        return max_p + 1



s = Solution1()
print(s.max_p(input1))



# end
