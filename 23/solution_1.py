'''
big input has ~3k elves
list of elf objects
    possess x-y coords, elf id (index in list)
each round a present state of eleves is constructed, 
    a set with elve identified by x-y coord will do
planned moves are registered in a dict,
    registered move leads to an entry containing their ID
        if their planned 

output is area of rectangle they need - total number of elves
'''

class Elf:
    def __init__(self, point, ID):
        self.coords = point
        self.bounced = False
        self.moving = False
        self.ID = ID

def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def settify_elves(elves):
    return set([elf.coords for elf in elves])



directions = [
    (1,0), #east
    (-1,0), # west
    (0,1), # south
    (0,-1), # north
    (1,1),
    (-1,1),
    (1,-1),
    (-1,-1),
]
# movement queue starts N, S, W, E
search_queue = [
    [directions[3], directions[6], directions[7]],
    [directions[2], directions[4], directions[5]],
    [directions[1], directions[5], directions[7]],
    [directions[0], directions[4], directions[6]]
]

def hesitant_move(elf, current_location, interests):
    for move in interests:
        neighbor = vector_add(elf.coords, move)
        if neighbor in current_location:
            return elf.coords, False
    return vector_add(elf.coords, interests[0]), True



def parse_file(file_name):
    raw_coords=[]
    y_val = 0
    with open(file_name, 'r') as terrain:
        # print('----- reading', file_name )
        for line in terrain.readlines():
            # print(line.rstrip())
            for x_val in range(len(line.rstrip())):
                if line[x_val] == '.':
                    continue
                # print('found elf at ', x_val)
                raw_coords.append(
                    (x_val, y_val)
                    )
            y_val+=1
    output = []
    for index, coords in enumerate(raw_coords):
        output.append(Elf(coords, index))
    return output

def take_turn(elves, turn_number):
    current_location = set([elf.coords for elf in elves])

    # check for moving
    movers = 0
    for elf in elves:
        elf.moving = False
        elf.bounced = False
        for direction in directions:
            neighbor = vector_add(direction, elf.coords)
            if neighbor in current_location:
                elf.moving = True
                movers += 1
                # print('elf %d is uncomfortable' % elf.ID )
                break

    # generate new moves
    proposed_moves = {}
    for index, elf in enumerate(elves):
        if not elf.moving:
            continue
        for attempt in range(len(search_queue)):
            searches = search_queue[(attempt+turn_number)%4]
            new_move, success = hesitant_move(elf, current_location, searches)
            if new_move == (2,4):
                print(elf.coords, attempt)
            if success:
                # print(elf.ID, searches[0])
                break
        if new_move in proposed_moves:
            elf.bounced = True
            elves[proposed_moves[new_move]].bounced = True
            print(elf.ID, proposed_moves[new_move], 'bounced')
            continue
        proposed_moves[new_move] = elf.ID
    # print(current_location)
    # print(proposed_moves)
    print('%d elves are uncomfortable' % movers)
    # print(len(proposed_moves.keys()))

    # implement moves
    for move in proposed_moves.keys():
        elf_id = proposed_moves[move]
        print(elf_id, elves[elf_id].coords, move, )
        if elves[elf_id].bounced:
            continue
        elves[elf_id].coords = move


    return elves, movers

def bounding_box(elves):
    minY = 10**6
    maxY = -10**6
    minX = 10**6
    maxX = -10**6
    for elf in elves:
        x, y = elf.coords
        if x > maxX:
            maxX = x
        if x < minX:
            minX = x
        if y > maxY:
            maxY = y
        if y < minY:
            minY = y
    return maxX-minX+1, maxY-minY+1

def elf_survey(elves):
    print([elf.coords for elf in elves])
    # test_input2
    # turn 0: [(2, 1), (3, 1), (2, 2), (2, 4), (3, 4)]
    # turn 1: [(2, 0), (3, 0), (2, 2), (2, 4), (3, 3)]
    # turn 2: [(2, 1), (3, 1), (1, 2), (2, 5), (4, 3)]
    # turn 3: [(2, 0), (4, 1), (0, 2), (2, 5), (4, 3)]
    # turn 4: everyones happy, same as turn 3


def solution(file_name):
    elf_list = parse_file(file_name)
    # print(elf_list)
    elf_survey(elf_list)
    loop = 0
    movers = len(elf_list)
    # for loop in range(5):
    while movers:
        print(loop)
        elf_list, movers = take_turn(elf_list, loop)
        # print(movers)
        # search_queue.append(search_queue.pop(0))
        # print(search_queue[0], len(search_queue))
        loop += 1
        print(loop, movers)
    elf_survey(elf_list)
    width, height = bounding_box(elf_list)
    print(width, height, 'bounds', len(elf_list))
    return (width*height)-len(elf_list)



if __name__ == '__main__':
    
    if not solution('test_input2.txt') == 25:
        print('test failed, stopping')
        exit()
    if not solution('test_input.txt') == 110:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    exit()
    print(solution('input.txt'))
