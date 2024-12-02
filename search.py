from grid import grid
from collections import deque
from queue import PriorityQueue
import time
from functions import clear_console, manhatten_distance, euclidean_distance

class search:
    def __init__(self, grid):
        self.grid = grid

    def search_goal(self):
        pass

    def is_goal(self, node):
        if self.grid.grid[node] == self.grid.goal_value: 
                print("goal reached !")
                return True
        return False

    def get_children(self, node):
        children = []
        if node[0] > 0 and self.grid.grid[node[0]-1, \
                                          node[1]] != self.grid.obstacle_value:
            children.append((node[0]-1, node[1]))
        if node[0] < self.grid.shape[0]-1 and self.grid.grid[node[0]+1, \
                                            node[1]] != self.grid.obstacle_value:
            children.append((node[0]+1, node[1]))
        if node[1] > 0 and self.grid.grid[node[0], \
                                          node[1]-1] != self.grid.obstacle_value:
            children.append((node[0], node[1]-1))
        if node[1] < self.grid.shape[1]-1 and self.grid.grid[node[0], \
                                            node[1]+1] != self.grid.obstacle_value:
            children.append((node[0], node[1]+1))
        
        return children

    def fill_reached(self, reached):
        for node in reached:
            if node == self.grid.start_idx: continue
            self.grid.grid[node] = self.grid.path_value

    def display_grid(self):
        clear_console()
        time.sleep(0.0001)
        print(f"{type(self).__name__} searching...")
        print(self.grid)

        
class bfs(search):
    def search_goal(self):
        reached = []
        frontier = deque()
        frontier.append(self.grid.start_idx)
        while frontier:
            node = frontier.popleft()
            if self.is_goal(node): return node
            for child in self.get_children(node):
                # if self.is_goal(child): return child
                if child not in reached and child not in frontier:
                    # reached.append(child)
                    frontier.append(child)
            reached.append(node)
            self.fill_reached(reached)
            self.display_grid()
            print(f"frontier: {len(frontier)}\n", frontier)
            print(f"\nreached: {len(reached)}\n", reached)

class dfs(search):
    def search_goal(self):
        reached = []
        frontier = deque()
        frontier.append(self.grid.start_idx)
        while frontier:
            node = frontier.pop()
            if node in reached: continue
            if self.is_goal(node): return node
            for child in self.get_children(node):
                if child not in frontier and child not in reached:
                    #reached.append(child)
                    frontier.append(child)
            self.fill_reached([node])
            reached.append(node)
            self.display_grid()
            print(f"frontier: {len(frontier)}\n", frontier)
            print(f"reached: {len(reached)}\n", reached)
            
class dfs_iterative_deepening(search):
    def search_goal(self):
        for i in range(1, self.grid.shape[0] + self.grid.shape[1]):
            reached = []
            frontier = deque()
            frontier.append(self.grid.start_idx)
            while frontier:
                node = frontier.pop()
                if node in reached: continue
                if self.is_goal(node): return node
                for child in self.get_children(node):
                    if child not in frontier and \
                        manhatten_distance(child, self.grid.start_idx) <= i:
                        #reached.append(child)
                        frontier.append(child)
                self.fill_reached([node])
                reached.append(node)
                self.display_grid(i)
                print(f"frontier: {len(frontier)}\n", frontier)
                print(f"reached: {len(reached)}\n", reached)
            self.grid.clear_paths()
            self.display_grid(i, sleep_at_the_end=1)

    def display_grid(self, i, sleep_at_the_end = 0):
        clear_console()
        time.sleep(0.0001)
        print(f"{type(self).__name__} searching...")
        print("depth: ", i)
        print(self.grid)
        time.sleep(sleep_at_the_end)

class a_star(search):
    def __init__(self, grid, path_cost = manhatten_distance, \
                 goal_cost = manhatten_distance):
        super().__init__(grid)
        self.path_cost = path_cost
        self.goal_cost = goal_cost

    def search_goal(self):
        reached = []
        frontier = PriorityQueue()
        frontier.put((self.goal_cost(self.grid.start_idx, self.grid._goal_idx), \
                      self.grid.start_idx))
        while not frontier.empty():
            node = frontier.get()[1]
            print(node)
            if node in reached: continue
            if self.is_goal(node): return node
            for child in self.get_children(node):
                if child not in reached:
                    frontier.put((self.goal_cost(child, self.grid._goal_idx) + \
                                  self.goal_cost(child, self.grid.start_idx), \
                                    child))
            self.fill_reached([node])
            reached.append(node)
            self.display_grid()
            print(f"frontier: {frontier.qsize()}\n", frontier)
            print(f"reached: {len(reached)}\n", reached)

    def display_grid(self):
        clear_console()
        time.sleep(0.0001)
        print(f"{type(self).__name__} searching... \
        \nf = {self.path_cost.__name__}, g = {self.goal_cost.__name__}")
        print(self.grid)


    
if __name__ == "__main__":

    shape = (20, 20)
    fill_value = ' '
    start_value = 'S'
    goal_value = 'X'
    start_idx = (0, 0)
    goal_idx = (0, 16)
    grid = grid(shape, goal_idx, fill_value, start_value, goal_value, start_idx)
    grid.add_random_obstacles(150)
        
    goal = bfs(grid).search_goal()
    print("goal index: ", goal)

    grid.clear_paths()
    goal = dfs(grid).search_goal()
    print("goal index: ", goal)

    # goal = dfs_iterative_deepening(grid).search_goal()
    # print("goal index: ", goal)

    grid.clear_paths()
    goal = a_star(grid).search_goal()
    print("goal index: ", goal)

    # goal = a_star(grid, euclidean_distance, euclidean_distance).search_goal()
    # print("goal index: ", goal)
