import numpy as np


def dijkstra(start, array):
    unvisited = np.ones(array.shape)
    dist = np.zeros_like(unvisited) + np.inf
    unvisited[start] = 0
    dist[start] = 0
    stack = [start]

    while stack:
        stack = sorted(stack, key=lambda x: dist[x], reverse=True)
        position = stack.pop()

        if unvisited[position]:
            unvisited[position] = 0

        for neighbor in neighbours(position):
            if unvisited[neighbor] and array[neighbor] != 1:
                if neighbor not in stack: stack.append(neighbor)
                if dist[position] + 1 < dist[neighbor]: dist[neighbor] = dist[position] + 1

    return dist


def neighbours(pos):
    i, j = pos
    if j % 2:
        res = [(i - 1, j), (i, j + 1), (i + 1, j + 1), (i + 1, j), (i + 1, j - 1), (i, j - 1)]
    else:
        res = [(i - 1, j), (i - 1, j + 1), (i, j + 1), (i + 1, j), (i, j - 1), (i - 1, j - 1)]

    final = []
    for i, j in res:
        if 0 <= i <= 8 and 0 <= j <= 11:
            final.append((i, j))

    return final