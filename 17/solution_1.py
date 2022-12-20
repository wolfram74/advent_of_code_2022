
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])


class Rock():
    rock_shapes = [
        ((0,0), (1,0), (2,0), (3,0), ), #horizontal line
        ((0,1), (1,0), (1,1), (1,2), (2,1), ), # plus sign
        ((0,0), (1,0), (2,0), (2,1), (2,2),  ), # angle bracket
        ((0,0), (0,1), (0,2), (0,3), ), # vertical line
        ((0,0), (0,1), (1,0), (1,1), ), # box
    ]
    rock_heights = (1, 3, 3, 4, 2)
    def __init__(self, piece_num, height=3):
        self.ID = piece_num
        self.type = self.ID%5
        self.geometry = Rock.rock_shapes[self.type]
        self.height = Rock.rock_heights[self.type]
        #rock shapes are defined such that location is always bottom left of filled space, for the + this is a void space
        self.location = [2,height]

class Cave():
    def __init__(self, gas_pattern):
        self.gas_pattern = gas_pattern
        self.gas_map = {'<': (-1,0), '>':(1,0) }
        self.pattern_length = len(gas_pattern)
        self.round_number = 0
        # self.space = [['_' for i in range(7)]]
        self.space = []

    def empty(self, x, y):
        # print(x,y)
        if y>len(self.space)-1:
            return True
        if y <= 0 and len(self.space)==0:
            return y == 0
        # print('checking', self.space[y][x])
        return self.space[y][x] == '_'

    # def overlap_safe(self, rock, new_location):


    def scoot_rock(self, rock):
        #scooting
        direction = self.gas_pattern[self.round_number % self.pattern_length]
        delta = self.gas_map[direction]
        # print(delta, self.round_number)
        self.round_number += 1
        new_location = vector_add(rock.location, delta)
        # print(new_location)
        if not self.wall_safe(rock, new_location):
            return rock
        if not self.overlap_safe(rock, new_location):
            return rock

        rock.location = new_location
        return rock

    def wall_safe(self, rock, new_location):
        if new_location[0] < 0:
            return False
        right_edge = vector_add(new_location, rock.geometry[-1])
        if right_edge[0] > 6:
            return False
        return True

    # def hori_rock_safe(self, rock, new_location):
        
    #     return True

    def fall_rock(self, rock):
        new_location = vector_add(rock.location, (0, -1))
        if not self.overlap_safe(rock, new_location):
            return rock, False
        rock.location = new_location
        return rock, True

    def overlap_safe(self, rock, new_location):
        for piece in rock.geometry:
            x,y = vector_add(new_location, piece)
            # print((x,y))
            if not self.empty(x,y):
                # print('collision!')
                return False
        return True

    def add_rock(self, rock):
        line_deficit = rock.height+rock.location[1]-len(self.space)
        for add_line in range(line_deficit):
            self.space.append(['_' for i in range(7)])
        # inspect_cave(self)
        for piece in rock.geometry:
            x,y = vector_add(rock.location, piece)
            # print((x,y))
            if not self.empty(x,y):
                print((x,y), self.space[y][x])
                print('collision error!')
                inspect_cave(self)
            self.space[y][x] = '#'
        pass



def parse_file(file_name):
    directions = []
    with open(file_name, 'r') as text:
        for line in text.readlines():
            directions[:0] = line.rstrip()
            break
    directions = tuple(directions)
    # print(directions)
    return directions

def test_adding(gas_pattern):
    empty_cave = Cave(gas_pattern)
    ground_rock = Rock(1, 0)  #plus sign
    empty_cave.add_rock(ground_rock)
    print('cave1')
    inspect_cave(empty_cave)
    empty_cave2 = Cave(gas_pattern)
    ground_rock = Rock(0, 0) #flat
    # inspect_cave(empty_cave2)
    empty_cave2.add_rock(ground_rock)
    print('cave2')
    inspect_cave(empty_cave2)

    empty_cave = Cave(gas_pattern)
    ground_rock = Rock(0, 0)
    empty_cave.add_rock(ground_rock)
    ground_rock = Rock(1, 1)
    empty_cave.add_rock(ground_rock)
    inspect_cave(empty_cave)

def test_rock_collision(gas_pattern):
    empty_cave = Cave(gas_pattern)
    wall = Rock(3,0)
    wall.location = (5,0)
    empty_cave.add_rock(wall)
    inspect_cave(empty_cave)
    sqr_block = Rock(4, 1)
    for i in range(4):
        sqr_block = empty_cave.scoot_rock(sqr_block)
        print(sqr_block.location)

def limited_run_test(gas_pattern):
    empty_cave = Cave(gas_pattern)
    for i in range(4):
        floor = len(empty_cave.space)
        current_rock = Rock(i, height=floor+3)
        moving = True
        while moving:
            current_rock = empty_cave.scoot_rock(current_rock)
            current_rock, moving = empty_cave.fall_rock(current_rock)
            print(current_rock.location)
        empty_cave.add_rock(current_rock)
        inspect_cave(empty_cave)

'''
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+
'''


def scoot_testing(gas_pattern):
    empty_cave = Cave(gas_pattern)

    # functionality_building
    print(len(empty_cave.gas_pattern))
    inspect_cave(empty_cave)
    first_rock = Rock(0, 3)
    print(first_rock.location)
    first_rock = empty_cave.scoot_rock(first_rock)
    print(first_rock.location, empty_cave.round_number)


def solution(file_name):
    # loop: generate a rock at it's origin (2, max_Y+3)
    # scoot with gas if possible
    # fall/land
    # need a scoot number and a rock number, stop after rock number 2022
    gas_pattern = parse_file(file_name)
    
    # scoot_testing(gas_pattern)
    # test_adding(gas_pattern)
    # test_rock_collision(gas_pattern)
    # limited_run_test(gas_pattern)

    empty_cave = Cave(gas_pattern)
    for i in range(2022):
        floor = len(empty_cave.space)
        print(i, floor)
        current_rock = Rock(i, height=floor+3)
        moving = True
        while moving:
            current_rock = empty_cave.scoot_rock(current_rock)
            current_rock, moving = empty_cave.fall_rock(current_rock)
            # print(current_rock.location)
        empty_cave.add_rock(current_rock)
        # inspect_cave(empty_cave)
    floor = len(empty_cave.space)
    print(i, floor)
    return floor


def inspect_cave(cave):
    for index in range(len(cave.space)-1, -1, -1):
        print('%03d' % index, cave.space[index])

if __name__ == '__main__':
    
    if not solution('test_input.txt') == 3068:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 best 1896
