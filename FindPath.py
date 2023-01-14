from collections import deque


class Graph:
    def __init__(self, sp=None, start=None):
        if not sp:
            self.sp = []
        else:
            self.sp = sp.copy()
        self.grid = []
        self.graph = {}
        self.start = self.goal = start
        self.cols = self.rows = 0
        self.make_grid()

    def make_grid(self):
        for i in range(len(self.sp)):
            line = []
            for j in range(len(self.sp[i])):
                line.append(1) if self.sp[i][j] == 'W' else line.append(0)
                if not self.start and self.sp[i][j] == 'q':
                    self.start = self.goal = (j, i)
            self.grid.append(line)
        self.cols, self.rows = len(self.grid[0]), len(self.grid)
        self.goal = self.start
        self.make_graph()

    def make_graph(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def get_next_nodes(self, x, y):
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(x + dx, y + dy) for dx, dy in ways if self.check_node(x + dx, y + dy)]

    def check_node(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows and not self.grid[y][x]:
            return True
        return False

    def bfs(self):
        queue = deque([self.start])
        visited = {self.start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == self.goal:
                break

            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return queue, visited

    def set_goal(self, goal):
        self.goal = goal

    def get_path(self):
        queue, visited = self.bfs()
        path_head, path_segment = self.goal, self.goal
        path_root = []
        while path_segment and path_segment in visited:
            if path_segment not in path_root:
                path_root.append(path_segment)
            path_segment = visited[path_segment]
        return path_root
