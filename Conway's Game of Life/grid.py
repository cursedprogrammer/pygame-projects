import random
GRID_W = 128
GRID_H = 72

NEIGHBORS = [(-1, -1), #top left
            (-1, 0),  #top center
            (-1, 1),  #top right
            (0, -1),  #left
            (0, 1),   #right
            (1, -1),  #bottom left
            (1, 0),   #bottom center
            (1, 1)]   #bottom right


def make_grid(width, height):
    grid = []
    grid.append([0 for x in range(width + 2)])
    for i in range(1, height):
        grid.append([])
        for j in range(width + 2):
            grid[i].append(0)
    grid.append([0 for x in range(width + 2)])
    return grid
    
def new_matrix(old_grid, new_grid):
    for y in range(1, len(old_grid)-1):        
        for x in range(1, len(old_grid[0])-1):
            new_grid[y][x] = count_cells(old_grid, (y, x))
            
           
def new_matrix2(old_grid, new_grid):
    for y in range(1, len(old_grid)-1):        
        for x in range(1, len(old_grid[0])-1):            
            if old_grid[y][x] == 1:
                sum = 0
                for z in NEIGHBORS:
                    if old_grid[y + z[0]][x + z[1]] == 1:
                        sum += 1
                if sum < 2 or sum > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            elif old_grid[y][x] == 0:
                sum = 0
                for z in NEIGHBORS:
                    if old_grid[y + z[0]][x + z[1]] == 1:
                        sum += 1
                if sum == 3:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
            
    
def count_cells(matrix, center_cell):
    if matrix[center_cell[0]][center_cell[1]] == 1:
        sum = 0
        for n in NEIGHBORS:
            if matrix[center_cell[0] + n[0]][center_cell[1] + n[1]] == 1:
                sum += 1
        if sum < 2 or sum > 3:
            return 0
        else:
            return 1
    elif matrix[center_cell[0]][center_cell[1]] == 0:
        sum = 0
        for n in NEIGHBORS:
            if matrix[center_cell[0] + n[0]][center_cell[1] + n[1]] == 1:
                sum += 1
        if sum == 3:
            return 1
        else:
            return 0
            
            
def random_seed(matrix):
    for row in matrix[1:-1]:
        for n in range(1, len(row)-1):
            row[n] = random.choice([0, 1])