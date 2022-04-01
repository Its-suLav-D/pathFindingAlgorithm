import pygame
import math 
from queue import PriorityQueue

# Width of the screen, How big the Screen is going to be 
WIDTH = 800

ROWS = 30
# Initialize the constructor 
pygame.init() 

# screen resolution 
res= (WIDTH,WIDTH)

# Set the display Screen 
WIN = pygame.display.set_mode(res)

# Title for the Game 
pygame.display.set_caption("Path Finding Visualizer")


# Colors that we will be using in our visualizer 
RED =  (224, 49, 49, 0.7)
GREEN = 70, 207, 59, 0.81
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255) 
BLACK = (0,0,0)
PURPLE = (33, 39, 227, 0.81) 
ORANGE = (225, 136, 18, 0.81)
GREY = (128,128,128)
LIGHT_BLUE =(18, 225, 205, 0.81)


# A particular Grid or Node in our Visualizer 
'''
    It needs to keep track of where it is in the grid, what is 
    its color, what are its neighbors, width, how wide the node 
    is going to be in our appplication, and all. 
'''
class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        # Keep Track of the Actual Position of the screen because when I draw node in pygame I can't just say draw it out at (5,5)
        # I need to draw actual cube, which will have its width and it will be sitting in some position 
        self.x = row * width 
        self.y = col* width
        self.color = WHITE 
        self.neighbors = [] 
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    # Visited 
    def is_closed(self):
        return self.color == RED 

    def is_open(self):
        return self.color == GREEN 

    def is_barrier(self):
        return self.color == BLACK 
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == LIGHT_BLUE

    def reset(self):
        self.color = WHITE 
    
    def make_closed(self):
        self.color = RED 

    def make_open(self):
        self.color = GREEN 
    
    def make_barrier(self):
        self.color = BLACK 

    def make_start(self):
        self.color = ORANGE 

    def make_end(self):
        self.color = LIGHT_BLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self,window):
        # Draw Cube
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self,grid):
        self.neighbors = []

        # DOWN 
        if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier(): # DOWN 
            node = grid[self.row+1][self.col]
            self.neighbors.append(node)
        
        # UP 
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): # UP
            node = grid[self.row-1][self.col]
            self.neighbors.append(node)

        # RIGHT 
        if self.col < self.total_rows -1 and not grid[self.row][self.col +1].is_barrier(): # RIGHT 
            node = grid[self.row][self.col+1]
            self.neighbors.append(node)
        # LEFT 
        if self.col > 0  and not grid[self.row][self.col-1].is_barrier(): # LEFT 
            node = grid[self.row][self.col-1]
            self.neighbors.append(node)
    

'''
    Calcualte the Manhattan Distance 
'''
def manhattan_distance(p1,p2):
    # p1 = (1,9)
    # Manhattan distance 
    x1,y1 = p1 
    x2,y2 = p2  
    return abs(x1-x2) + abs(y1-y2)


'''
 Reconstruct the Path 
'''

def reconstruct_path(came_from,current,draw):

    while current in came_from:
        current = came_from[current]
        current.make_path() 
        draw() 

'''
A Star Agorithm 
'''

def astar(draw,grid,start,end): 
    # Draw is a function 
    count = 0 
    # Get smallest ELement Of out it. Works like a Min-Heap 
    open_set = PriorityQueue()
    open_set.put((0,count,start))

    # Track of Visited Node 
    came_from = {}
    # Make Every G Score Infinity because we haven't yet Visited 
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = manhattan_distance(start.get_pos(),end.get_pos())

    # Priority Queue Doesn't have a Hash Function so, we need another data Stucture to do the task 
    open_set_hash = {start}  

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # 2 Represents the node
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # If this was true, than we found the shortest path, and basically need to reconstruct the path 
        if current == end: 
            reconstruct_path(came_from,end,draw)
            end.make_end()
            start.make_start()
            return True  

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] +1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current 
                g_score[neighbor] = temp_g_score 
                f_score[neighbor] = temp_g_score + manhattan_distance(neighbor.get_pos(), end.get_pos()) 
                if neighbor not in open_set_hash:
                    count+=1 
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() 
        
        draw()
        if current != start:
            current.make_closed()
        
    return False 
                

'''
 Depth First Search Algorithm
'''
            

def dfs(draw,start,end):
    visited = set() 
    stack=[start]

    # Track of Visited Node 
    came_from = {}
    while len(stack) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = stack.pop() 
        visited.add(current_node)

        if current_node == end:
            reconstruct_path(came_from, end,draw)
            end.make_end()
            start.make_start()
            return True 

        for neighbor in current_node.neighbors:
            if( neighbor not in visited) and (neighbor not in stack):
                came_from[neighbor] = current_node 
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if  current_node != start: 
            current_node.make_closed()

    return False 



'''
Breadth First Search ALgorithm 
'''

def bfs(draw,start,end): 
    visited = set()

    queue = [start] 
    came_from = {}
    while len(queue) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        current_node = queue.pop(0) 
        visited.add(current_node)

        if current_node == end: 
            reconstruct_path(came_from, end,draw)
            end.make_end()
            start.make_start()
            return True 

        for neighbor in current_node.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current_node 
                queue.append(neighbor)
                neighbor.make_open() 

        draw() 
        if current_node != start:
            current_node.make_closed() 
    
    return False 
        

''' 
 Need to complete the Dijstra Algorithm 
'''

def dijkstra(draw,grid,start,end):
    pass 

# Make the Grid 
def make_grid(rows,width): 
    grid = []
    # Gap Between Each rows 
    gap = width // rows 
    for i in range(rows): 
        grid.append([]) 
        for j in range(rows): 
            node = Node(i,j,gap,rows)
            grid[i].append(node)
    
    return grid  

# Draw Grid Lines
def draw_grid_line(window, rows,width): 
    gap = width // rows  
    for i in range(rows): 
        pygame.draw.line(window,GREY,(0,i* gap),(width,i*gap))
        for j in range(rows): 
            pygame.draw.line(window,GREY,(j*gap,0),(j*gap,width)) 

# Main Draw that will draw everything 
# Draw The Grid on the Screen 
def draw(window,grid,rows,width): 
    window.fill(WHITE)

    for row in grid: 
        for node in row:
            node.draw(window)

    # Draw Grid Line 
    draw_grid_line(window,rows,width)
    # Update the display of what we have 
    pygame.display.update() 

# Get Position of the Clicked Row and COl 
def get_clicked_pos(pos,rows,width): 
    print(pos,rows,width)
    gap = width // rows
    i,j = pos 
    # This is weird because of how pyGame gives us position
    row = i // gap 
    col = j // gap 
    print(col,row)
    return row, col 

def game_loop(window,width):

    grid = make_grid(ROWS,width)

    start = None 
    end = None 

    run = True 
   
    while run: 
        draw(window,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False 
            
            
            # LEFT PRESS 
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col] 
                if not start and node != end: 
                    start = node 
                    start.make_start()  
                elif not end and node != start: 
                    end = node 
                    node.make_end()  

                elif node != end and node != start: 
                    node.make_barrier() 
                
            # RIGHT PRESS 
            elif  pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]  
                node.reset()

                if node == start: 
                    start = None
                if node == end:
                    end = None  

            # Space press to start the game 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid) 
                    
                    bfs(lambda: draw(window,grid,ROWS,width), start,end)

                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid) 
                    
                    astar(lambda: draw(window,grid,ROWS,width),grid, start,end)

                
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid) 
                    
                    dfs(lambda: draw(window,grid,ROWS,width), start,end)

    pygame.quit() 

if __name__ == "__main__":
    game_loop(WIN,WIDTH)




    



