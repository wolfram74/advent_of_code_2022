def load_tree_grid(tree_map):
    output = []
    for line in tree_map.readlines():
        output.append(
            [int(el) for el in list(line.rstrip())]
            )
        # print(output[-1])
    return output

def print_grid(grid):
    for line in grid:
        print(''.join([str(el) for el in line]))

def count_visibles(tree_grid):
    output = 0
    height, width = len(tree_grid), len(tree_grid[0])
    print(height, width)
    # it'd be very easy to double count some in the corners
    # there's no guarentee you'd encounter a height 9 tree in any interval
    # so it's unclear how big those "corners" are
    # maybe a matching grid full of 0s
    # progress down the rows/columns putting a 1 in the companion slot if it's taller than any seen before 
    # until a 9 is reached
    # assigning 1 instead of incrementing 1 guarentees no double counting
    visibility_map = [ [ 0 for el in range(width) ] for el in range(height) ]
    for row in range(height):
        tallest_front, tallest_back = -1, -1
        check_index = 0
        tree_line = tree_grid[row]
        while not (tallest_front, tallest_back) == (9,9):
            if tree_line[check_index] > tallest_front:
                visibility_map[row][check_index] = 1
                tallest_front = tree_line[check_index]
            if tree_line[-1-check_index] > tallest_back:
                visibility_map[row][-1-check_index] = 1
                tallest_back = tree_line[-1-check_index]
            print(tallest_front, tallest_back)
            check_index+=1
            if check_index > height-1:
                break

    for col in range(width):
        tallest_front, tallest_back = -1, -1
        check_index = 0
        tree_line = [row[col] for row in tree_grid]

        while not (tallest_front, tallest_back) == (9,9):

            if tree_line[check_index] > tallest_front:
                visibility_map[check_index][col] = 1
                tallest_front = tree_line[check_index]
            if tree_line[-1-check_index] > tallest_back:
                visibility_map[-1-check_index][col] = 1
                tallest_back = tree_line[-1-check_index]
            print(tallest_front, tallest_back)
            check_index+=1
            if check_index > height-1:
                break

    print_grid(visibility_map)
    for row in range(width):
        for col in range(height):
            output += visibility_map[row][col]
    print(output) #1541 is too low

def best_scenic_score(tree_grid):
    record = 0
    for row in range(len(tree_grid)):
        for col in range(len(tree_grid)):
            score = scenic_score_calculator(tree_grid, (row, col))
            if score > record:
                record = score
                print(record)
    print(record)

def scenic_score_calculator(tree_grid, location):
    left, right, up, down = 1,1,1,1
    row, col = location[0], location[1]
    tree_val = tree_grid[row][col]
    while col-left>0:
        if tree_grid[row][col-left] >= tree_val:
            break
        left+=1
    while col+right<98:
        if tree_grid[row][col+right] >= tree_val:
            break
        right+=1
    while row-up>0:
        if tree_grid[row-up][col] >= tree_val:
            break
        up+=1
    while row+down<98:
        if tree_grid[row+down][col] >= tree_val:
            break
        down+=1
    if col == 0:
        left = 0
    if col == 98:
        right = 0
    if row == 0:
        up = 0
    if row == 98:
        down = 0
    # print(left, right, up, down)
    return up*down*left*right

if __name__ == '__main__':
    with open('input.txt', 'r') as tree_map:

        tree_grid = load_tree_grid(tree_map)
        # count_visibles(tree_grid)
        print(4==scenic_score_calculator(tree_grid, (1,1)))
        print((2*1*7*11)==scenic_score_calculator(tree_grid, (1,2)))
        best_scenic_score(tree_grid)
