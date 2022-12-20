'''
given a set of voxel coordinates, what is the total exposed area
is it safe to assume the blob is contiguous?
every cube starts with 6 faces
probably best to make a 3-d list and just do neighbor occupancy checks
void detection:
get the bounds of obsidian, suspect only positive numbers
second pass on blob generation, iterate over all space and if there's an existent blob nearby, add it to void list
'''
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

directions  = [
    (1,0,0),
    (-1,0,0),
    (0,1,0),
    (0,-1,0),
    (0,0,1),
    (0,0,-1),
]


def parse_file(file_name):
    blob = {}
    bounds = [0,0,0]
    with open(file_name, 'r') as vectors:
        for vector in vectors.readlines():
            location = tuple(int(el) for el in vector.rstrip().split(','))
            blob[location] = [True, 6]
            for ind, val in enumerate(location):
                compare = bounds[ind]
                if val < 0:
                    print('well carp')
                if val > compare:
                    bounds[ind] = val+1
            # print(location)
    return blob, bounds

def void_check(blob, bounds):
    print(bounds)
    enclosed_voids = 0
    voids = {}
    for x in range(bounds[0]):
        for y in range(bounds[1]):
            for z in range(bounds[2]):
                location = (x,y,z)
                if location in blob:
                    continue
                if is_enclosed(blob, location):
                    enclosed_voids += 1

    print(enclosed_voids)
    return enclosed_voids

def is_enclosed(blob, location):
    for direction in directions:
        check = vector_add(direction,location)
        if not check in blob:
            # print(location,check)
            return False
    # print(location)
    return True

def solution(file_name):
    blob, bounds = parse_file(file_name)
    tally = 0
    for vector in blob.keys():
        # print(vector)
        for direction in directions:
            check = vector_add(direction,vector)
            if check in blob:
                blob[vector][1] -= 1
        tally += blob[vector][1]
    tally -= 6*void_check(blob, bounds)
    return tally


if __name__ == '__main__':
    
    if not solution('test_input.txt') == 58:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
