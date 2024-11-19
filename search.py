from grid import grid
from collections import deque
import time
from functions import clear_console, manhatten_distance

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
            self.grid.grid[self.grid.grid == '.'] = self.grid.fill_value
            self.display_grid(i, sleep_at_the_end=1)

    def display_grid(self, i, sleep_at_the_end = 0):
        clear_console()
        time.sleep(0.0001)
        print(f"{type(self).__name__} searching...")
        print("depth: ", i)
        print(self.grid)
        time.sleep(sleep_at_the_end)



    
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

    # goal = dfs(grid).search_goal()
    # print("goal index: ", goal)

    # goal = dfs_iterative_deepening(grid).search_goal()
    # print("goal index: ", goal)
