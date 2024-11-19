import numpy as np
import random

class grid:

    def __init__(self, shape, goal_idx, fill_value='-', start_value='s', goal_value='g', \
                 start_idx=(0,0), obstacle_value='#', path_value='.'):
        self.shape = shape
        self.grid = np.full(shape, fill_value)
        self.start_value = start_value
        self.goal_value = goal_value
        self.start_idx = start_idx
        self._goal_idx = goal_idx
        self.grid[start_idx] = self.start_value
        self.grid[goal_idx] = self.goal_value
        self.obstacle_value = obstacle_value
        self.path_value = path_value
        self.fill_value = fill_value

    def add_random_obstacles(self, n):
        i = 0
        while i < n:
            r = random.randint(0, self.shape[0]-1)
            c = random.randint(0, self.shape[1]-1)
            if (r, c) not in [self.start_idx, self._goal_idx]:
                self.grid[r, c] = self.obstacle_value
                i += 1

    def __repr__(self):
        res = "state :\n"
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res = res + f"{self.grid[i][j]}  "
            res = res + f"\n"
        return res


if __name__ == '__main__':

    shape = (10, 10)
    fill_value = '.'
    start_value = 'i'
    goal_value = 'x'
    start_idx = (0, 0)
    goal_idx = (8, 8)
    grid = grid(shape, goal_idx, fill_value, start_value, goal_value, start_idx)
    print(grid)
    grid.add_random_obstacles(40)
    print(grid)
