def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def vector_diff(v1, v2):
    return tuple([el[0]-el[1] for el in zip(v1, v2)])

def units(v1):
    steps = int(sum([el**2 for el in v1])**.5)
    hat = tuple([int(el/steps) for el in v1])
    return hat, steps



def make_terrain(rock_scan):
    rock_lines = []
    max_X, min_X = -10**6, 10**6
    max_Y, min_Y = -10**6, 10**6
    for line in rock_scan.readlines():
        path = []
        vertices = line.split('->')
        for point in vertices:
            x,y = [int(el) for el in point.split(',')]
            vertex = (x,y)
            if x > max_X:
                max_X = x
            if x < min_X:
                min_X = x
            if y > max_Y:
                max_Y = y
            if y < min_Y:
                min_Y = y
            path.append(vertex)
        rock_lines.append(path)
    # print(min_X, max_X, max_X-min_X, 500-min_X)
    # print(min_Y, max_Y)
    width = max_X-min_X+1
    x_offset = min_X
    height = max_Y+1
    print(width, height, x_offset)
    return array_generator(rock_lines, width, height, x_offset), x_offset

def array_generator(rock_lines, width, height, x_offset):
    blanks = [['_' for x in range(width)] for y in range(height)]
    for path in rock_lines:
        for index, vert in enumerate(path[:-1]):
            shift = vector_diff(vert, path[index+1])
            draw = [vert[0]-x_offset, vert[1]]
            # print(vert, path[index+1], shift)
            # print(draw)
            blanks[draw[1]][draw[0]] = 'X'

            hat, scale = units(shift)
            for i in range(scale):
                draw = vector_diff(draw, hat)
                blanks[draw[1]][draw[0]] = 'X'
    return blanks

def draw_terrain(field):
    for line in field:
        print(''.join(line))

def drop_sand(field, x_offset):
    location = (500-x_offset, 0)
    searching = True
    while searching:
        test_1 = vector_add(location, (0,1))
        if field[test_1[1]][test_1[0]] == '_':
            location = test_1
            continue

        test_2 = vector_add(location, (-1,1))
        if field[test_2[1]][test_2[0]] == '_':
            location = test_2
            continue

        test_3 = vector_add(location, (1,1))
        if field[test_3[1]][test_3[0]] == '_':
            location = test_3
            continue
        field[location[1]][location[0]] = 'O'
        searching = False
    return field

if __name__ == '__main__':
    with open('input.txt', 'r') as rock_scan: # 
    # with open('test_input.txt', 'r') as rock_scan: # expect 24
        rock_map, x_offset = make_terrain(rock_scan)
        # draw_terrain(rock_map)
        sands = 0
        while True:
            try:
                rock_map = drop_sand(rock_map, x_offset)
                sands+=1
            except:
                break
        draw_terrain(rock_map)
        print(sands)

