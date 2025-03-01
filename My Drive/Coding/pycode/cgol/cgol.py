"""
Rules: 

    1) Underpopulation: If a live cell has fewer than two live neighbors, 
        it dies (as if by loneliness).
    
    2) Survival: If a live cell has two or three live neighbors, 
        it survives to the next generation.
    
    3) Overpopulation: If a live cell has more than three live neighbors, 
        it dies (as if by overcrowding).
    
    4) Reproduction: If a dead cell has exactly three live neighbors, 
        it becomes alive (as if by reproduction).
"""
import numpy as np
import matplotlib.pyplot as plt

# square grid
grid_size = 8
grid = np.zeros(shape=(grid_size, grid_size))

# initial state. This one has been tested and works
grid[4, 4] = 1
grid[3, 4] = 1
grid[3, 5] = 1
grid[5, 5] = 1
grid[6, 4] = 1

# adding edge problems to initial state. DOES NOT WORK YET
grid[0, 0] = 1
grid[0, 1] = 1
grid[1, 0] = 1
grid[2, 1] = 1
grid[0, 0] = 1


# each rule must be applied where the grid is 1, and the adjacent cells
print(grid)
# this gives the cells
y_coords_1, x_coords_1 = np.where(grid==1) # using yx 

yx_1 = np.stack((y_coords_1, x_coords_1), axis=-1)

grid_next_iteration = np.zeros_like(grid)
for y, x in yx_1:
    print(f'x: {x}, y: {y}')
    # min max logic below should assure that we're always inside the grid with the slicing. 
    grid_slice = grid[max(y-1, 0):min(y+2, grid_size), max(x-1, 0):min(x+2, grid_size)]
    # the point x, y is in the middle of the slice, obv
    print(grid_slice)
    # first three rules can be implemented based on sum of the slices
    n_neighbors = np.sum(grid_slice) - 1 # subtracting itself
    print(n_neighbors)

    if n_neighbors < 2: #loneliness
        grid_next_iteration[y, x] = 0
    elif n_neighbors == 2 or 3: #survival
        grid_next_iteration[y, x] = 1
    elif n_neighbors > 4: #overpopulation
        grid_next_iteration[y, x] = 0


print()
print("############ REPRODUCTION PART ############")
print()
# need to check the dead cells around the live ones
#print(x_coords_1, y_coords_1)
min_x = np.min(x_coords_1)
min_y = np.min(y_coords_1)
max_x = np.max(x_coords_1)
max_y = np.max(y_coords_1)
#print(min_x, max_x, min_y, max_y)

min_max_slice = grid[
    max(min_y-1, 0):min(max_y+2, grid_size),
    max(min_x-1, 0):min(max_x+2, grid_size),
]
slice_shape = min_max_slice.shape
print(slice_shape)
print(np.arange(min_x-1, max_x+1))
print(np.arange(min_y-1, max_y+1))
#min_max_slice = grid.take(indices=np.arange(min_x-1:max_x+2))

y_coords_0, x_coords_0 = np.where(min_max_slice==0)
yx_0 = np.stack((y_coords_0, x_coords_0), axis=-1)

print(yx_0)

print(f'Grid before reproduction: \n{grid} \n Windowed: \n{min_max_slice}')

for y, x in yx_0:
    print()
    print(f'x: {x}, y: {y}')
    grid_slice_0 = min_max_slice[
        max(y-1, 0):min(y+2, slice_shape[1]), 
        max(x-1, 0):min(x+2, slice_shape[0]),
    ]
    print(grid_slice_0)
    n_ones_neighboring = np.sum(grid_slice_0) # not subtracting on zero cell
    print('Neighbors', n_ones_neighboring)

    if n_ones_neighboring == 3:
        print(f'N Neighbors is 3 for x: {x}, y: {y}')
        print(print(y+min_y-1, x+min_x-1))
        quit()
        grid_next_iteration[y+min_y, x+min_x] = 1
    
    #TODO Figure out how whether I want periodic boundary or not
    #TODO Figure out why sums are zero for slices now



# I think one iteration works now as long as we're not on the edges.

print()
print(grid_next_iteration)
