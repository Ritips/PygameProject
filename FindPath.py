from collections import deque


class Graph:
    def __init__(self, sp=None, start=None):  # sp - it is a level; start - position before movement
        if not sp:
            self.sp = []
        else:
            self.sp = sp.copy()
        self.grid = []
        self.graph = {}
        self.start = self.goal = start
        self.cols = self.rows = 0
        self.make_grid()

    def make_grid(self):  # function that makes sp which contains 1 or 0. 1 - object with collision; 0 - empty slot
        for i in range(len(self.sp)):
            line = []
            for j in range(len(self.sp[i])):
                line.append(1) if self.sp[i][j] == 'W' else line.append(0)
                if not self.start and self.sp[i][j] == 'q':
                    self.start = self.goal = (j, i)
            self.grid.append(line)
        self.cols, self.rows = len(self.grid[0]), len(self.grid)
        self.goal = self.start  # it was added because of queen
        self.make_graph()

    def make_graph(self):  # to make graph for searching path in future
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def get_next_nodes(self, x, y):  # check available cells from current cell
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(x + dx, y + dy) for dx, dy in ways if self.check_node(x + dx, y + dy)]

    def check_node(self, x, y):  # check if cell is empty or not
        if 0 <= x < self.cols and 0 <= y < self.rows and not self.grid[y][x]:
            return True
        return False

    def bfs(self):  # realisation of Dijkstra's algorithm
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

    def set_goal(self, goal):  # set the cell to get into
        if not self.grid[goal[1]][goal[0]]:
            self.goal = goal

    def get_path(self):  # return sp of cells that must be passed through to reach the destination
        queue, visited = self.bfs()
        path_head, path_segment = self.goal, self.goal
        path_root = []
        while path_segment and path_segment in visited:
            if path_segment not in path_root:
                path_root.append(path_segment)
            path_segment = visited[path_segment]
        return path_root

    def get_graph(self):
        return self.graph
