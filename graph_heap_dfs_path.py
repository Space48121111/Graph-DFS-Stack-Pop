from __future__ import annotations
from collections import defaultdict

txt = open('graph_heap_dfs_path.txt', 'r')
input1 = txt.read()
input = '''\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''

'''
output = 10
output 1 = 36 visit one small cave twice
    start
    /   \
c--A-----b--d
    \   /
     end

lowercase: visit at most once
start - end
uppercase: multiple times
output -> all the paths with lowercase
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

dfs O(V + E):
brutal force:
path = []
visited = False
stack = ['start']
parsing edges from splitlines() and add
while stack:
    stack.pop()
    if val[-1] == 'end':
        return path
    for edges in path[-1]:
        if lowercase or not visited
            stack.append()

'''

def graph_dfs(s: str) -> int:
    edges = defaultdict(set)
    for line in s.splitlines():
        src, dst = line.split('-')
        edges[src].add(dst)
        edges[dst].add(src)
    stack =[('start', )]
    all_paths = set()
    while stack:
        path = stack.pop()
        if path[-1] == 'end':
            all_paths.add(path)
            continue
        for candid in edges[path[-1]]:
            if not candid.islower() or candid not in path:
                stack.append((*path, candid))
    return len(all_paths)

def graph_dfs_twice(s: str) -> int:
    edges = defaultdict(set)
    for line in s.splitlines():
        src, dst = line.split('-')
        edges[src].add(dst)
        edges[dst].add(src)
    stack =[(('start', ), False)]
    all_paths = set()
    while stack:
        path, double_cave = stack.pop()
        if path[-1] == 'end':
            all_paths.add(path)
            continue
        for candid in edges[path[-1]]:
            if candid == 'start':
                continue
            elif not candid.islower() or candid not in path:
                stack.append(((*path, candid), double_cave))
            elif not double_cave and path.count(candid) == 1:
                stack.append(((*path, candid), True))
    return len(all_paths)

print(graph_dfs(input))
print(graph_dfs_twice(input))


# end
