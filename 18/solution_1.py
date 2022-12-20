'''
given a set of voxel coordinates, what is the total exposed area
is it safe to assume the blob is contiguous?
every cube starts with 6 faces
probably best to make a 3-d list and just do neighbor occupancy checks
'''
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])


def parse_file(file_name):
    blob = {}
    with open(file_name, 'r') as vectors:
        for vector in vectors.readlines():
            location = tuple(int(el) for el in vector.rstrip().split(','))
            blob[location] = [True, 6]
            # print(location)
    return blob


def solution(file_name):
    blob = parse_file(file_name)
    directions  = [
        (1,0,0),
        (-1,0,0),
        (0,1,0),
        (0,-1,0),
        (0,0,1),
        (0,0,-1),
    ]
    tally = 0
    for vector in blob.keys():
        print(vector)
        for direction in directions:
            check = vector_add(direction,vector)
            if check in blob:
                blob[vector][1] -= 1
        tally += blob[vector][1]
    return tally


if __name__ == '__main__':
    
    if not solution('test_input.txt') == 64:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 best 1896
